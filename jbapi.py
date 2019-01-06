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

# This file is the bridge between OLD APIS (seel "libs/")
# and the new frontend !

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

class JBrout:
    db=None
    tags=None
    conf=None

def init(confPath):
    if os.path.isdir(confPath):
        print("USE CONF in",confPath)
        JBrout.db = DBPhotos(os.path.join(confPath,"db.xml"))
        JBrout.tags = DBTags(os.path.join(confPath,"tags.xml"))
        JBrout.conf = Conf(os.path.join(confPath,"conf.json"))
        JBrout.db.setNormalizeName(JBrout.conf["normalizeName"])
        JBrout.db.setNormalizeNameFormat(str(JBrout.conf["normalizeNameFormat"]))
        JBrout.db.setAutorotAtImport(JBrout.conf["autorotAtImport"])
    else:
        print("ERROR: can't find path to conf:",confPath)
        os._exit(-1)

def addFolder(folder): # in development ;-)
    importedTags={}
    for i in JBrout.db.add(folder,importedTags):
        if type(i)==dict:
            last=i
        else:
            yield i
    last["importedTags"]=list(importedTags.keys())
    last["nbImportedTags"]=JBrout.tags.updateImportedTags(last["importedTags"])
    yield last

def save():
    JBrout.db.save()
    JBrout.tags.save()
    JBrout.conf.save()

def getConf():
    return JBrout.conf

##############################################################################
##############################################################################
##############################################################################
def getTags():
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
    return [ dict(name="Tags",type="cat",expand=True,children=tol( JBrout.tags.getRootTag() )) ]

def getFolders():
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
    return tol( JBrout.db.getRootFolder() )



def _photonodes2json(ll): #TODO: very expensive ! each attributs takes time ! (x2 per attribut)
    return [dict(path=i.file,date=i.date) for i in ll]

def selectPhotoNode(path): # -> 1 PhotoNode
    d=os.path.dirname(path)
    b=os.path.basename(path)
    ll= JBrout.db.select('''//folder[@name="%s"]/photo[@name="%s"]''' % (d,b))
    return ll[0]

def selectFolderNode(path):  # -> 1 FolderNode
    ll=JBrout.db.selectf('''//folder[@name="%s"]''' % path)
    return ll[0]

def selectFromFolder(path,all=False):
    kind = "descendant::photo" if all else "photo"
    ll= JBrout.db.select('''//folder[@name="%s"]/%s''' % (path,kind))
    return _photonodes2json(ll)

def getYear(year):
    xpath = """//photo[substring(@date, 1,4)="%s"]""" % str(year)
    ll= JBrout.db.select(xpath)
    return _photonodes2json(ll)
def getYearMonth(yyyymm):
    xpath = """//photo[substring(@date, 1,6)="%s"]""" % str(yyyymm)
    ll= JBrout.db.select(xpath)
    return _photonodes2json(ll)

def selectFromTags(tags):
    xpath = " or ".join(['t=%s' % xpathquoter(t) for t in tags])
    ll= JBrout.db.select("""//photo[%s]""" % xpath)
    return _photonodes2json(ll)

def selectFromBasket():
    ll= JBrout.db.getBasket()
    return _photonodes2json(ll)

def catExpand(cat,bool):
    c=JBrout.tags.selectCat(cat)
    if c:
        c.setExpand(bool)

def clearBasket():
    JBrout.db.clearBasket()

def tagsAddCat(cat,newCat):
    c=JBrout.tags.selectCat(cat)
    if c:
        return c.addCatg(newCat.strip())

def tagsAddTag(cat,newTag):
    c=JBrout.tags.selectCat(cat)
    if c:
        return c.addTag(newTag.strip())

def tagsDelTag(tag):
    c=JBrout.tags.selectTag(tag)
    if c:
        c.remove()
        return True

def tagsDelCat(cat):
    c=JBrout.tags.selectCat(cat)
    if c:
        c.remove()
        return True

def tagMoveToCat(tag,cat):
    c1=JBrout.tags.selectTag(tag)
    c2=JBrout.tags.selectCat(cat)
    if c1 and c2:
        c1.moveToCatg(c2)
        return True

def catMoveToCat(cat1,cat2):
    c1=JBrout.tags.selectCat(cat1)
    c2=JBrout.tags.selectCat(cat2)
    if c1 and c2:
        c1.moveToCatg(c2)
        return True

def catRename(cat1,cat2):
    c1=JBrout.tags.selectCat(cat1)
    if c1:
        return c1.rename(cat2)




if __name__=="__main__":
    #~ print(addFolder("/home/manatlan/Bureau/Cal2018"))
    #~ print(addFolder("/home/manatlan/Bureau/CAL2016"))
    #~ quit()
    init("/home/manatlan/.local/share/ijbrout/")   #copy of the original jbrout
    x=getYears()

    print(x)
    quit()
    x=JBrout.tags.selectTag("marco")
    print(x)
    x=JBrout.tags.selectCat("potes obernai")
    print(x)
    #~ ll=JBrout.db.select('''//folder[@name="%s"]/%s''' % ("/nas/data/photos","descendant::photo"))
    #~ ll=selectFromFolder("/",True)
    #~ print( {i["date"][:4] for i in ll} )
    print( getYears() )
    #~ print(getInfo(ll[0]["path"]))
    quit()

    print(JBrout.db)
    ll=JBrout.db.getRootFolder().getPhotos()
    print(ll.xpath)
    ll=JBrout.db.getRootFolder().getAllPhotos()
    print(ll.xpath)
    print(ll[1].getInfo())
    print(len(ll[1].getImage()))
    print(ll[1].getThumb())
    print(ll[1].rebuildThumbnail())
    print(ll[1].getThumb())
    print(ll[1].rotate("R"))
    print(ll[1].resolution)
    print(ll[1].comment)
    print(ll[1].date)
    print(ll[1].addToBasket())
    print(JBrout.tags.getAllTags())
    print(JBrout.conf)

    r= JBrout.db.getRootFolder()

    def tol(f):
        ll=[]
        for i in f.getFolders():
            ll.append( dict(
                name=i.name,
                path=i.file,
                expand=i.expand,
                items=len(i.getPhotos()),
                folders=tol(i),
            ))
        return ll
    print( tol(r) )

    print(JBrout.conf["normalizeNameFormat"])
