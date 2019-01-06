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


__version__="0.2.1"

class jbrout:

    def getFolders(self):
        return api.getFolders()
    def getTags(self):
        return api.getTags()
    def getYears(self):
        ll=api.selectFromFolder("/",True)

        if ll:
            ma = 11111111
            mi = 99999999
            for i in ll:
                a = int(i["date"][:8])
                ma = max(a, ma)
                mi = min(a, mi)
        f=lambda yyyymmdd: yyyymmdd[0:4]+"-"+yyyymmdd[4:6]+"-"+yyyymmdd[6:8]
        return dict(years=sorted(list({i["date"][:4] for i in ll} )), min=f(str(mi)),max=f(str(ma)))

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
        f=api.selectFolderNode(folder)
        f.remove()

    def albumComment(self,path,value=None): # getter & setter
        f=api.selectFolderNode(path)
        if value is None: # getter
            return f.comment
        else:             # setter
            return f.setComment(value)

    def albumExpand(self,folder,bool):
        f=api.selectFolderNode(folder)
        f.setExpand(bool)

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
        p=api.selectPhotoNode(path)
        p.rebuildThumbnail()

    def photoRotateRight(self,path):
        p=api.selectPhotoNode(path)
        p.rotate("R")

    def photoRotateLeft(self,path):
        p=api.selectPhotoNode(path)
        p.rotate("L")

    def photoComment(self,path,txt):
        p=api.selectPhotoNode(path)
        p.setComment(txt)

    def removeBasket(self):
        api.clearBasket()

    def photoBasket(self,path,bool):
        p=api.selectPhotoNode(path)
        if bool:
            p.addToBasket()
        else:
            p.removeFromBasket()



    def getYear(self,yyyy):
        return api.getYear(yyyy)
    def getYearMonth(self,yyyymm):
        return api.getYearMonth(yyyymm)

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

    def catRename(self,cat1,cat2):
        return api.catRename(cat1,cat2)


    def photoAddTags(self, path, tags):
        assert type(tags) == list
        p=api.selectPhotoNode(path)
        return p.addTags(tags)
    def photoDelTag(self, path, tag):
        p=api.selectPhotoNode(path)
        return p.delTag(tag)
    def photoClearTags(self,path):
        p=api.selectPhotoNode(path)
        return p.clearTags()


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
        v=vbuild.render( os.path.join(path,"web/*.vue") )

        # and inject them in your template
        return content.replace("<!-- HERE -->",str(v))

    def request(self,req):  #override to hook others web requests

        def send_info(idx,path,i):
            info=dict(tags=i.tags,comment=i.comment,rating=i.rating,resolution=i.resolution,real=i.real)
            self.emit("set-info",idx,path,info)

        idx=req.query.get("idx",None)
        if req.path.startswith("/thumb/"):
            path=req.path[7:]
            pic=api.selectPhotoNode(path)
            if idx is not None: send_info(idx,path,pic)
            return pic.getThumb()
        elif req.path.startswith("/image/"):
            path=req.path[7:]
            pic=api.selectPhotoNode(path)
            if idx is not None: send_info(idx,path,pic)
            return pic.getImage()

def main():
    cwd = os.path.dirname(__file__)
    wuy.PATH = cwd

    ## wuy.ChromeApp=wuy.ChromeAppCef    # to test with cefpython3

    #~ api.init(os.path.expanduser("~/.local/share/jbrout"))  #copy of the original jbrout
    #~ index()
    #~ quit()

    api.init(os.path.join(cwd,"tempconf"))
    index()
    api.save()

if __name__=="__main__":
    main()
