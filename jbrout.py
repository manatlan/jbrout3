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
from jbapi import JBrout

__version__="0.2.1"

class jbrout:

    def getFolders(self):
        return self.api.getFolders()
    def getTags(self):
        return self.api.getTags()
    def getYears(self):
        ll=self.api.selectFromFolder("/",True)

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
        g=self.api.addFolder(folder)
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
        f=self.api.selectFolderNode(folder)
        f.remove()

    def albumComment(self,folder,value=None): # getter & setter
        f=self.api.selectFolderNode(folder)
        if value is None: # getter
            return f.comment
        else:             # setter
            return f.setComment(value)

    def albumExpand(self,folder,bool):
        f=self.api.selectFolderNode(folder)
        f.setExpand(bool)

    def catExpand(self,cat,bool):
        c=self.api.selectCatNode(cat)
        if c:
            c.setExpand(bool)

    def selectFromFolder(self,folder,all=False):
        return self.api.selectFromFolder(folder,all)
    def selectFromBasket(self):
        return self.api.selectFromBasket()
    def selectFromTags(self,tags):
        if tags:
            return self.api.selectFromTags(tags)
        else:
            return []

    def photoRebuildThumbnail(self,path):
        p=self.api.selectPhotoNode(path)
        p.rebuildThumbnail()

    def photoRotateRight(self,path):
        p=self.api.selectPhotoNode(path)
        p.rotate("R")

    def photoRotateLeft(self,path):
        p=self.api.selectPhotoNode(path)
        p.rotate("L")

    def photoComment(self,path,txt):
        p=self.api.selectPhotoNode(path)
        p.setComment(txt)

    def removeBasket(self):
        self.api.clearBasket()

    def photoBasket(self,path,bool):
        p=self.api.selectPhotoNode(path)
        if bool:
            p.addToBasket()
        else:
            p.removeFromBasket()



    def getYear(self,yyyy):
        return self.api.getYear(yyyy)
    def getYearMonth(self,yyyymm):
        return self.api.getYearMonth(yyyymm)

    def tagsAddTag(self,cat,txt):
        c=self.api.selectCatNode(cat)
        if c:
            return c.addTag(txt.strip())
    def tagsAddCat(self,cat,txt):
        c=self.api.selectCatNode(cat)
        if c:
            return c.addCatg(txt.strip())
    def tagsDelTag(self,txt):
        t=self.api.selectTagNode(txt)
        if t:
            t.remove()
            return True

    def tagsDelCat(self,txt):
        c=self.api.selectCatNode(cat)
        if c:
            c.remove()
            return True

    def tagMoveToCat(self,tag,cat):
        t1=self.api.selectTagNode(tag)
        c2=self.api.selectCatNode(cat)
        if t1 and c2:
            t1.moveToCatg(c2)
            return True

    def catMoveToCat(self,cat1,cat2):
        c1=self.api.selectCatNode(cat1)
        c2=self.api.selectCatNode(cat2)
        if c1 and c2:
            c1.moveToCatg(c2)
            return True

    def catRename(self,cat1,cat2):
        c1=self.api.selectCatNode(cat1)
        if c1:
            return c1.rename(cat2)

    def photoAddTags(self, path, tags):
        assert type(tags) == list
        p=self.api.selectPhotoNode(path)
        return p.addTags(tags)
    def photoDelTag(self, path, tag):
        p=self.api.selectPhotoNode(path)
        return p.delTag(tag)
    def photoClearTags(self,path):
        p=self.api.selectPhotoNode(path)
        return p.clearTags()


    def cfgGet(self,k,default=None):
        cfg=self.api.getConf()
        return cfg.get(k,default)

    def cfgSet(self,k,v):
        cfg=self.api.getConf()
        cfg[k]=v


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
            pic=self.api.selectPhotoNode(path)
            if idx is not None: send_info(idx,path,pic)
            return pic.getThumb()
        elif req.path.startswith("/image/"):
            path=req.path[7:]
            pic=self.api.selectPhotoNode(path)
            if idx is not None: send_info(idx,path,pic)
            return pic.getImage()

def main():
    cwd = os.path.dirname(__file__)
    wuy.PATH = cwd

    ## wuy.ChromeApp=wuy.ChromeAppCef    # to test with cefpython3

    #~ with JBrout(os.path.expanduser("~/.local/share/jbrout")) as api:  #copy of the original jbrout
    #~     index(api=api)
    #~ quit()

    with JBrout(os.path.join(cwd,"tempconf")) as api:
        index(api=api)

if __name__=="__main__":
    main()
