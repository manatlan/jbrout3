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
from jbapi import JBrout
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
        v=vbuild.render( os.path.join(path,"web/*.vue") )

        # and inject them in your template
        return content.replace("<!-- HERE -->",str(v))

    """
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
    """

    def request(self,req):  #override to hook others web requests

        def getPic(path,idx):
            i=self.api.selectPhotoNode(path)
            if idx is not None:
                info=dict(
                    tags=i.tags,
                    comment=i.comment,
                    rating=i.rating,
                    resolution=i.resolution,
                    real=i.real
                )
                self.emit("set-info",idx,path,info)
            return i

        idx=req.query.get("idx",None)
        if req.path.startswith("/thumb/"):
            return getPic(req.path[7:],idx).getThumb()
        elif req.path.startswith("/image/"):
            return getPic(req.path[7:],idx).getImage()

    """
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
        IF YOU CHANGE THINGS HERE, DONT FORGET TO REPORT TO jbrout.py:index !
    """

def main():
    cwd = os.path.dirname(__file__)
    wuy.PATH = cwd

    #~ with api.init(os.path.expanduser("~/.local/share/jbrout")):  #copy of the original jbrout
    with JBrout(os.path.join(cwd,"tempconf")) as api:
        index(api=api)        

if __name__=="__main__":
    main()
