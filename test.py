#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from SMBController import SMBController

smbController = SMBController('<host>',
    '<username>', '<password>', '<domain>') 
smbController.cd('<path>')
smbController.uploadFile('<path>')
# ls
items = smbController.ls()
print([item.filename for item in items])
