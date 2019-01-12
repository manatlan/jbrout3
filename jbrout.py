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

__version__="0.2.2"

class jbrout:
    """ RPC methods exposed in the front, see wuy.<method>() in js """

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

    def selectYear(self,yyyy):
        return self.api.selectYear(yyyy)

    def selectYearMonth(self,yyyymm):
        return self.api.selectYearMonth(yyyymm)


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

    def dir(self,path):
        np=lambda x: os.path.realpath(os.path.join(path,x))
        ll=[ dict(name="..",isdir=True, path=np("..")) ]
        try:
            l=[dict(name=i,isdir=os.path.isdir( np(i) ),path=np(i)) for i in os.listdir(path) if not i.startswith(".")]
            folders=[i for i in l if i["isdir"]]
            files=[i for i in l if not i["isdir"] and (os.path.splitext(i["name"])[1][1:].lower() in self.api.supportedFormats) ]
            folders.sort(key=lambda x: x["name"].lower())
            files.sort(key=lambda x: x["name"].lower())
            ll.extend( folders )
            ll.extend( files )
        except PermissionError:
            pass
        return ll

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
