#!/usr/bin/python3
# # -*- coding: utf-8 -*-
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
from libs.db import DBPhotos,DBTags
from libs.pyexiv import Exiv2Metadata
from libs.common import xpathquoter
import os,json

# This file is the bridge between OLD APIS (see "libs/")
# and the new frontend !
# theses apis will be merged in libs, at the end ;-)

class Conf(dict):
    def __init__(self,file):
        self.file=file
        if os.path.isfile(self.file):
            with open(self.file,"r") as fid:
                default=json.load(fid)
        else:
            default=dict(
                normalizeName = True,
                normalizeNameFormat = "p%Y%m%d_%H%M%S",
                autorotAtImport = False,

                #~ thumbsize = 86,          #TODO: to localStorage !
                #~ orderAscending = 0,      #TODO: to localStorage !
                synchronizeXmp = False,
                #~ orderBy = "Date",        #TODO: to localStorage !
            )

        dict.__init__(self,default)

    def save(self):
        with open(self.file,"w+") as fid:
            json.dump(self,fid, indent=4)
##############################################################################
##############################################################################
##############################################################################
def _photonodes2json(ll): # WARN: very expensive ; adding attributs takes time ! (x2 per attribut)
    return [dict(path=i.file,date=i.date) for i in ll]


class JBrout(object):
    db=None
    tags=None
    conf=None

    def __init__(self,confPath):
        if os.path.isdir(confPath):
            print("USE CONF in",confPath)
            self.db = DBPhotos(os.path.join(confPath,"db.xml"))
            self.tags = DBTags(os.path.join(confPath,"tags.xml"))
            self.conf = Conf(os.path.join(confPath,"conf.json"))
            self.db.setNormalizeName(self.conf["normalizeName"])
            self.db.setNormalizeNameFormat(str(self.conf["normalizeNameFormat"]))
            self.db.setAutorotAtImport(self.conf["autorotAtImport"])
        else:
            print("ERROR: can't find path to conf:",confPath)
            os._exit(-1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.save()
        self.tags.save()
        self.conf.save()
        print("JBrout : db saved !")


    def addFolder(self,folder): # in development ;-)
        importedTags={}
        for i in self.db.add(folder,importedTags):
            if type(i)==dict:
                last=i
            else:
                yield i
        last["importedTags"]=list(importedTags.keys())
        last["nbImportedTags"]=self.tags.updateImportedTags(last["importedTags"])
        yield last


    def getConf(self):
        return self.conf

    def getTags(self):
        def tol(f):
            ll=[]
            for c in f.getCatgs():
                ll.append( dict(
                    name=c.name,
                    children=tol(c),
                    type="cat",
                    expand=c.expand,
                ))
            for t in f.getTags():
                ll.append( dict(
                    name=t.name,
                    children=[],
                    type="tag",
                ))
            return ll
        return [ dict(name="Tags",type="cat",expand=True,children=tol( self.tags.getRootTag() )) ]

    def getFolders(self):
        def tol(f):
            ll=[]
            if f:
                for i in f.getFolders():
                    ll.append( dict(
                        path=i.file,
                        expand=i.expand,
                        items=len(i.getPhotos()),
                        folders=tol(i),
                    ))
            return ll
        return tol( self.db.getRootFolder() )


    def selectPhotoNode(self,path): # -> 1 PhotoNode
        d=os.path.dirname(path)
        b=os.path.basename(path)
        ll= self.db.select('''//folder[@name="%s"]/photo[@name="%s"]''' % (d,b))
        return ll[0]

    def selectFolderNode(self,path):  # -> 1 FolderNode
        ll=self.db.selectf('''//folder[@name="%s"]''' % path)
        return ll[0]

    def selectCatNode(self,cat):
        return self.tags.selectCat(cat)

    def selectTagNode(self,tag):
        return self.tags.selectTag(tag)

    def selectFromFolder(self,path,all=False):
        kind = "descendant::photo" if all else "photo"
        ll= self.db.select('''//folder[@name="%s"]/%s''' % (path,kind))
        return _photonodes2json(ll)

    def getYear(self,year):
        xpath = """//photo[substring(@date, 1,4)="%s"]""" % str(year)
        ll= self.db.select(xpath)
        return _photonodes2json(ll)
    def getYearMonth(self,yyyymm):
        xpath = """//photo[substring(@date, 1,6)="%s"]""" % str(yyyymm)
        ll= self.db.select(xpath)
        return _photonodes2json(ll)

    def selectFromTags(self,tags):
        xpath = " or ".join(['t=%s' % xpathquoter(t) for t in tags])
        ll= self.db.select("""//photo[%s]""" % xpath)
        return _photonodes2json(ll)

    def selectFromBasket(self):
        ll= self.db.getBasket()
        return _photonodes2json(ll)

    def clearBasket(self):
        self.db.clearBasket()





if __name__=="__main__":
    api=JBrout("/home/manatlan/.local/share/ijbrout/")   #copy of the original jbrout
    #~ print(api.addFolder("/home/manatlan/Bureau/Cal2018"))
    #~ print(api.addFolder("/home/manatlan/Bureau/CAL2016"))
    #~ quit()

    x=api.selectTagNode("marco")
    print(x)
    x=api.selectCatNode("potes obernai")
    print(x)
    #~ ll=JBrout.db.select('''//folder[@name="%s"]/%s''' % ("/nas/data/photos","descendant::photo"))
    #~ ll=api.selectFromFolder("/",True)
    #~ print( {i["date"][:4] for i in ll} )

