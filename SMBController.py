#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import platform
from smb.SMBConnection import SMBConnection
from pathlib import Path
from pathlib import PureWindowsPath

class SMBController:
    def __init__(self, host,
            username, password, domain):
        self.host = host

        self.service_name = None
        self.path = None

        self._username = username
        self._password = password
        self._domain = domain

    def cd(self, destPath):
        # resolve service name and path
        p = PureWindowsPath(destPath)
        self.service_name = p.parts[0]
        self.path = destPath[len(self.service_name):]

    def createConnection(self):
        return SMBConnection(
            self._username,
            self._password,
            platform.uname().node,
            self.host, domain = self._domain, use_ntlm_v2 = True)

    def ls(self, destPath = None):

        # change directory to destPath
        if destPath != None:
            self.cd(destPath)

        if self.service_name is None or self.path is None:
            raise Exception('The path is not specified.')

        connection = self.createConnection()
        # connect to samba
        isConnected = connection.connect(self.host, 139)
        if isConnected is False:
            raise Exception("connect failed")

        items = connection.listPath(
                    self.service_name,
                    self.path)

        connection.close()
        return items

    def uploadFile(self, filePath, destPath = None):

        # change directory to destPath
        if destPath != None:
            self.cd(destPath)

        if self.service_name is None or self.path is None:
            raise Exception('The upload path is not specified.')

        # check file info
        srcPath = Path(filePath)
        if srcPath.is_file() is False:
            raise Exception('specified path is not file')

        srcFileSize = os.path.getsize(srcPath)

        # remote file path
        storePath = PureWindowsPath(Path(self.path), Path(srcPath.name))

        # connect to samba
        connection = self.createConnection()
        isConnected = connection.connect(self.host, 139)
        if isConnected is False:
            raise Exception("connect failed")

        # do upload
        with open(filePath, 'rb') as file:
            numBytes = connection.storeFile(
                    self.service_name,
                    str(storePath), file)

            print(srcPath.name, numBytes, ' bytes uploaded')

        connection.close()

        if srcFileSize != numBytes:
            raise Exception('upload file error file size:', srcFileSize,
                    ' uploaded size:', numBytes)
