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
    JBrout.db = DBPhotos(os.path.join(confPath,"db.xml"))
    JBrout.tags = DBTags(os.path.join(confPath,"tags.xml"))
    JBrout.conf = Conf(os.path.join(confPath,"conf.json"))
    JBrout.db.setNormalizeName(JBrout.conf["normalizeName"])
    JBrout.db.setNormalizeNameFormat(str(JBrout.conf["normalizeNameFormat"]))
    JBrout.db.setAutorotAtImport(JBrout.conf["autorotAtImport"])

def addFolder(folder): # in development ;-)
    importedTags={}
    x=JBrout.db.add(folder,importedTags)
    print(list(x))  # important !
    print("importedTags",importedTags)
    nbNewTags = JBrout.tags.updateImportedTags(list(importedTags.keys()))
    print("nbNewTags",nbNewTags)

def save():
    JBrout.db.save()
    JBrout.tags.save()
    JBrout.conf.save()


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
            ))
        for t in f.getTags():
            ll.append( dict(
                name=t.name,
                children=[],
            ))
        return ll
    return tol( JBrout.tags.getRootTag() )

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
    return [dict(path=i.file,tags=i.tags,date=i.date,comment=i.comment,rating=i.rating,resolution=i.resolution) for i in ll]

def selectFromFolder(path,all=False):
    kind = "descendant::photo" if all else "photo"
    ll= JBrout.db.select('''//folder[@name="%s"]/%s''' % (path,kind))
    return _photonodes2json(ll)

def selectFromBasket():
    ll= JBrout.db.getBasket()
    return _photonodes2json(ll)

def selectFromTags(tags):
    xpath = " or ".join(['t=%s' % xpathquoter(t) for t in tags])
    ll= JBrout.db.select("""//photo[%s]""" % xpath)
    return _photonodes2json(ll)


def getThumb(path): # -> bytes (jpeg/thumbnail)
    t=Exiv2Metadata(path)
    t.readMetadata()
    return t.getThumbnailData()

def getImage(path): #-> bytes (jpeg/image)
    with open(path,"rb") as fid:
        return fid.read()

if __name__=="__main__":
    init("./temp_conf/")
    print(addFolder("/home/manatlan/Bureau/Cal2018"))
    print(addFolder("/home/manatlan/Bureau/CAL2016"))
    quit()
    init("/home/manatlan/.local/share/ijbrout/")   #copy of the original jbrout
    #~ ll=JBrout.db.select('''//folder[@name="%s"]/%s''' % ("/nas/data/photos","descendant::photo"))
    ll=selectFromFolder("/nas/data/photos",True)
    print(len(ll))
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
