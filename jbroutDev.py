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
import wuy,vbuild
import jbapi as api
from jbrout import jbrout

class index(wuy.Server,jbrout):
    """
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
    """

    def _render(self,path): #here is the magic
        # load your template (from web folder)
        with open( os.path.join(path,"web","index.html") ) as fid:
            content=fid.read()

        # load all vue/sfc components
        v=vbuild.render( path+"web/*.vue" )

        # and inject them in your template
        return content.replace("<!-- HERE -->",str(v))

    """
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
    """

    def request(self,req):  #override to hook others web requests
        idx=req.query.get("idx",None)
        if req.path.startswith("/thumb/"):
            path=req.path[7:]
            if idx is not None: self.emit("set-info",idx,path,api.getInfo(path))
            return api.getThumb(path)
        elif req.path.startswith("/image/"):
            path=req.path[7:]
            if idx is not None: self.emit("set-info",idx,path,api.getInfo(path))
            return api.getImage(path)

    """
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
    """


if __name__=="__main__":
    try:
        os.chdir(os.path.split(sys.argv[0])[0])
    except:
        pass

    #~ api.init(os.path.expanduser("~/.local/share/jbrout"))  #copy of the original jbrout
    api.init("./tempconf")
    index(log=True)
    api.save()



