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

import os,sys
import wuy,vbuild
import jbapi as api
#~ import jbfake as api


__version__="0.0.1"

class index(wuy.Window):
#~ class index(wuy.Server):

    size=(1074,800)

    def _render(self,path): #here is the magic
        # load your template (from web folder)
        with open( os.path.join(path,"web","index.html") ) as fid:
            content=fid.read()

        # load all vue/sfc components
        v=vbuild.render( path+"web/*.vue" )

        # and inject them in your template
        return content.replace("<!-- HERE -->",str(v))

    def request(self,req):  #override to hook others web requests
        if req.path.startswith("/thumb/"):
            path=req.path[7:]
            return api.getThumb(path)
        elif req.path.startswith("/image/"):
            path=req.path[7:]
            return api.getImage(path)

    def getFolders(self):
        return api.getFolders()
    def getTags(self):
        return api.getTags()

    def addFolder(self):    #TODO: make async/yield here ! (for big folders)
        import easygui  # until we found another way (in a cefpython instance ; it should be possible to make it client-side!)
        folder=easygui.diropenbox(msg="Select folder/album to add", title="jbrout")
        if folder:
            api.addFolder(folder)
            return True
        return False

    def getInfo(self,path):
        return api.getInfo(path)

    def selectFromFolder(self,path,all=False):
        return api.selectFromFolder(path,all)
    def selectFromBasket(self):
        return api.selectFromBasket()
    def selectFromTags(self,tags):
        return api.selectFromTags(tags)


if __name__=="__main__":
    try:
        os.chdir(os.path.split(sys.argv[0])[0])
    except:
        pass

    #~ api.init("/home/manatlan/.local/share/ijbrout/")   #copy of the original jbrout
    #~ index(log=False)

    api.init("./tempconf")
    index(log=True) #log to False, speedify a lot ;-), but when debugguing, it's hard ;-)
    api.save()


