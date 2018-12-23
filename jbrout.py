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

import os,sys,asyncio
import wuy,vbuild
import jbapi as api
#~ import jbfake as api


__version__="0.0.1"

class jbrout:

    def getFolders(self):
        return api.getFolders()
    def getTags(self):
        return api.getTags()

    async def addFolder(self):    #TODO: make async/yield here ! (for big folders)
        import easygui  # until we found another way (in a cefpython instance ; it should be possible to make it client-side!)
        folder=easygui.diropenbox(msg="Select folder/album to add", title="jbrout")
        if folder:
            return await self.refreshFolder(folder)

    async def refreshFolder(self,folder):
        g=api.addFolder(folder)
        nb=next(g)
        self.emit("set-working","0/%s"%nb)
        last=None
        for i in g:
            await asyncio.sleep(0.00001)
            if type(i)==dict:
                self.emit("set-working",None)
                last=i
            else:
                self.emit("set-working","%s/%s"%(i+1,nb))
        return last

    def removeFolder(self,folder):
        api.removeFolder(folder)
    def albumExpand(self,folder,bool):
        api.albumExpand(folder,bool)
    def catExpand(self,cat,bool):
        api.catExpand(cat,bool)

    def selectFromFolder(self,path,all=False):
        return api.selectFromFolder(path,all)
    def selectFromBasket(self):
        return api.selectFromBasket()
    def selectFromTags(self,tags):
        if tags:
            return api.selectFromTags(tags)
        else:
            return []

    def photoRebuildThumbnail(self,path):
        p=api.selectPhoto(path)
        p.rebuildThumbnail()

    def photoRotateRight(self,path):
        p=api.selectPhoto(path)
        p.rotate("R")

    def photoRotateLeft(self,path):
        p=api.selectPhoto(path)
        p.rotate("L")

    def removeBasket(self):
        api.clearBasket()

    def photoBasket(self,path,bool):
        p=api.selectPhoto(path)
        if bool:
            p.addToBasket()
        else:
            p.removeFromBasket()

    def getYears(self):
        return api.getYears()
    def getYear(self,year):
        return api.getYear(year)

    def tagsAddTag(self,cat,txt):
        return api.tagsAddTag(cat,txt)
    def tagsAddCat(self,cat,txt):
        return api.tagsAddCat(cat,txt)
    def tagsDelTag(self,txt):
        return api.tagsDelTag(txt)
    def tagsDelCat(self,txt):
        return api.tagsDelCat(txt)

    def tagMoveToCat(self,tag,cat):
        return api.tagMoveToCat(tag,cat)

    def catMoveToCat(self,cat1,cat2):
        return api.catMoveToCat(cat1,cat2)


    def photoAddTags(self, path, tags):
        api.photoAddTags(path,tags)
    def photoDelTag(self, path, tag):
        api.photoDelTag(path,tag)
    def photoClearTags(self,path):
        api.photoClearTags(path)

    def cfgGet(self,k,default=None):
        cfg=api.getConf()
        return cfg.get(k,default)

    def cfgSet(self,k,v):
        cfg=api.getConf()
        cfg[k]=v
        cfg.save()


class index(wuy.Window,jbrout):
    """ wuy tech class (with tech stuff) """
    size=(1024,780)

    def _render(self,path): #here is the magic
        # load your template (from web folder)
        with open( os.path.join(path,"web","index.html") ) as fid:
            content=fid.read()

        # load all vue/sfc components
        v=vbuild.render( path+"web/*.vue" )

        # and inject them in your template
        return content.replace("<!-- HERE -->",str(v))

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


if __name__=="__main__":
    try:
        os.chdir(os.path.split(sys.argv[0])[0])
    except:
        pass

    #~ api.init(os.path.expanduser("~/.local/share/jbrout"))  #copy of the original jbrout
    #~ index(log=False)
    #~ quit()

    api.init("./tempconf")
    #~ index(log=True) #log to False, speedify a lot ;-), but when debugguing, it's hard ;-)
    index(log=False) #log to False, speedify a lot ;-), but when debugguing, it's hard ;-)
    api.save()


