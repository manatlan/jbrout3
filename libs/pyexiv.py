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
pyexiv2 wrapper
===============

map old methods/objects from pyexiv2(<2), to work with versions 1 & 2

"""
import sys
import logging
logging.basicConfig(level=logging.INFO)

import pyexiv2



###############################################################################
class Exiv2Metadata(object):
###############################################################################
    def __init__(self, md):
        self._md = pyexiv2.ImageMetadata(md)

    #============================================== V 0.1 api
    def readMetadata(self):
        return self._md.read()

    def writeMetadata(self):
        # set CharacterSet as UTF8
        self._md["Iptc.Envelope.CharacterSet"] = ['\x1b%G', ]
        return self._md.write()

    def __getitem__(self, k):
        v = self._md[k]
        if hasattr(v, "value"):
            return v.value
        elif hasattr(v, "values"):
            return tuple(v.values)
        else:
            raise

    def __setitem__(self, k, v):
        self._md[k] = v

    def __delitem__(self, k):
        del self._md[k]

    def getComment(self):
        return self._md.comment

    def setComment(self, v):
        self._md.comment = v

    def clearComment(self):
        self._md.comment = None

    def getThumbnailData(self):
        return bytes(self._md.exif_thumbnail.data)
        #~ l = [i.data for i in self._md.previews]
        #~ if l:
            #~ return [None, l[0]]
        #~ else:
            #~ return []

    def setThumbnailData(self, o):
        self._md.exif_thumbnail.data = o

    def deleteThumbnail(self):
        self._md.exif_thumbnail.erase()

    def exifKeys(self):
        return self._md.exif_keys

    def iptcKeys(self):
        return self._md.iptc_keys

    def tagDetails(self, k):  # see viewexif plugin
        md = self._md[k]
        if hasattr(md, "label"):
            lbl = getattr(md, "label")
        elif hasattr(md, "title"):
            lbl = getattr(md, "title")
        return [lbl, md.description, ]

    def interpretedExifValue(self, k):  # see viewexif plugin
        return self._md[k].human_value
    #==============================================

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- new apis
    def xmpKeys(self):
        return self._md.xmp_keys

    def getTags(self):
        """ return a list of merged tags (xmp+iptc) (list of str)"""
        # Authoritative reference
        # http://www.iptc.org/std/Iptc4xmpCore/1.0/documentation\
        # /Iptc4xmpCore_1.0-doc-CpanelsUserGuide_13.pdf
        # however
        # http://metadataworkinggroup.com/pdf/mwg_guidance.pdf page 35:
        # # IPTC Keywords is mapped to XMP (dc:subject)
        # It seems that the latter is true ... at least according to
        # http://trac.yorba.org/wiki/PhotoTags

        li = []
        if "Iptc.Application2.Keywords" in self._md.iptc_keys:
            # digikam patch
            li = [str(i.strip("\x00"))
                  for i in self._md["Iptc.Application2.Keywords"].value]
            # assume UTF8
        lk = []
        if "Xmp.iptc.Keywords" in self._md.xmp_keys:
            for xel in self._md["Xmp.iptc.Keywords"].value:
                lk.extend([x.strip() for x in xel.split(",")])
            # assume UTF8
        lx = []
        if "Xmp.dc.subject" in self._md.xmp_keys:
            for xel in self._md["Xmp.dc.subject"].value:
                lx.extend([x.strip() for x in xel.split(",")])

        ll = list(set(li + lx + lk))
        ll.sort()
        _keys = ['Iptc.Application2.Keywords', 'Xmp.iptc.Keywords',
                 'Xmp.dc.subject']
        for key in _keys:
            if key in self._md:
                logging.debug("%s = %s" % (key, self._md[key]))
        return ll

    def setTags(self, l):
        for i in l:
            assert type(i) == unicode

        if l:
            self._md["Iptc.Application2.Keywords"] = \
                [i.encode("utf_8") for i in l]
            self._md["Xmp.dc.subject"] = l
        else:
            del self._md["Iptc.Application2.Keywords"]
            del self._md["Xmp.dc.subject"]

    def getDimensions(self):
        return self._md.dimensions

    def clearTags(self):
        if "Iptc.Application2.Keywords" in self._md.iptc_keys:
            del self._md["Iptc.Application2.Keywords"]
        if "Xmp.dc.subject" in self._md.xmp_keys:
            del self._md["Xmp.dc.subject"]
        if 'Xmp.iptc.Keywords' in self._md.xmp_keys:
            del self._md['Xmp.iptc.Keywords']

    def copyToFile(self, destFilename, exif=True, iptc=True, xmp=True,
                   comment=True):
        dest = pyexiv2.ImageMetadata(destFilename)
        dest.read()
        self._md.copy(dest, exif, iptc, xmp, comment)
        dest.write()

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

###############################################################################
if __name__ == "__main__":
    #~ t = Image("/home/manatlan/Documents/python/tests_libs_python" +
              #~ "/TestJPG/p20030830_130202 (copie).jpg")
    #~ t.readMetadata()

    ##----
    # aa=t._image["Xmp.dc.subject"].raw_value[0]
    # import chardet; print chardet.detect(aa) # it's latin1 encoded as utf8
    # print aa.decode("utf_8").encode("latin1")
    ##----

    # t.setThumbnailData("")

    #~ L = t.getTags()
    #~ print( "===>", L )

    # t=Image("/home/manatlan/Desktop/fotaux/autorot/jpg/p20090319_061423.jpg")
    # t.readMetadata()
    # t.deleteThumbnail()
    # t.writeMetadata()

    import glob
    for i in glob.glob("/home/manatlan/Desktop/fotaux/autorot/*.jpg"):
        x=Exiv2Metadata(i)
        x.readMetadata()
        print(x.getTags())
        print(x.getComment())
        with open("aeff.jpg","wb") as fid:
            fid.write( x.getThumbnailData() )

