#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
# ###########################################################################
# #
# #    Copyright (C) 2005-2019 manatlan manatlan[at]gmail(dot)com
# #
# # This program is free software; you can redistribute it and/or modify
# # it under the terms of the GNU General Public License as published
# # by the Free Software Foundation; version 2 only.
# #
# # This program is distributed in the hope that it will be useful,
# # but WITHOUT ANY WARRANTY; without even the implied warranty of
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# # GNU General Public License for more details.
# #
# ###########################################################################


"""
    This file is just for dev test (server mode)
    it will disappear in the future (when 1.0)
"""
import os,sys
import guy,vbuild
from jbapi import JBrout
from jbrout import jbrout,index

def main():
    cwd = os.path.dirname(__file__)

    #~ with api.init(os.path.expanduser("~/.local/share/jbrout")):  #copy of the original jbrout
    with JBrout(os.path.join(cwd,"tempconf")) as api:
        w=index(api=api)
        w.serve()

if __name__=="__main__":
    main()
