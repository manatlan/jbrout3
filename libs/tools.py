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
MAJOR CHANGES :
  - unlike old tools, filedate is modified at each operation which
    modify picture
    (so tools for backup, like rsync should work)
  - always an exifdate, when no exif date : create exif date with
    filedate m_time
    (so destroyinfo leave exifdate in place)
  - use only jpegtran/exiftran tools (for LOSSLESS rotation)
  - api are the same than old one (but should change in the future)
  - thumbnail are created in python (pil+pyexiv2)
  - autorot only available on LINUX and Windows
  - addition of transfrom command (rotate is now depricated)
"""
import os
import sys
from . import pyexiv
import pyexiv2

import time
from datetime import datetime, timedelta
#~ from PIL import Image
import io
from PIL import Image
import string
import re
from subprocess import Popen, PIPE


def ed2cd(f):  # yyyy/mm/dd hh:ii:ss -> yyyymmddhhiiss
    if f:
        return f[:4] + f[5:7] + f[8:10] + f[11:13] + f[14:16] + f[17:19]
    else:
        return f

# the second argument provides a string when using this code to provide
# rotation to plugins
autoTrans = {
    1: ["none", "None"],
    2: ["flipHorizontal", "Flip Horizontal"],
    3: ["rotate180", "Rotate 180"],
    4: ["flipVertical", "Flip Vertical"],
    5: ["transpose", "Transpose"],
    6: ["rotate90", "Rotate Left"],
    7: ["transverse", "Transverse"],
    8: ["rotate270", "Rotate Right"]}

# videoFormats = ["avi", "mov"]  # not used yet (marc)

rawFormats = ["nef", "dng", "cr2"]
# "cr2" files are for canon RAW. Makes pyexiv2 crash 14/07/2009 works
# with exiv2 though
supportedFormats = ["jpg", "jpeg"] + rawFormats


class CommandException(Exception):
    def __init__(self, m):
        self.args = [m]

    def __str__(self):
        return self.args[0]


def decode(s, encodings=['ascii', 'utf8', 'latin1']):
    """ method to decode text (tag or comment) to unicode """
    if type(s) != unicode:
        for encoding in encodings:
            try:
                return s.decode(encoding)
            except UnicodeDecodeError:
                pass
        print( " *WARNING* : no valid decoding for string '%s'" % (str([s])) )
        return s.decode('utf8', 'replace')
    else:
        return s


# ###########################################################################
class _Command:
# ###########################################################################
    """ low-level access (wrapper) to external tools used in jbrout
    """
    isWin = (sys.platform[:3] == "win")
    __path = os.path.join(os.getcwd(), u"data", u"tools")

    err = ""
    if isWin:
        # set windows path
        _exiftran = None
        _jpegtran = os.path.join(__path, "jpegtran.exe")

        if not os.path.isfile(_jpegtran):
            err += "jpegtran is not present in 'tools'\n"

    else:
        # set "non windows" path (needs 'which')
        _exiftran = u"".join(os.popen("which exiftran").readlines()).strip()
        _jpegtran = None

        if not os.path.isfile(_exiftran):
            err += \
                "exiftran is not present, please install 'exiftran'(fbida)\n"

    if err:
        raise Exception(err)

    @staticmethod
    def _run(cmds):
        # ~ print cmds
        # to output easily (with strange chars)
        cmdline = str([" ".join(cmds)])
        try:
            cmds = [i.encode(sys.getfilesystemencoding()) for i in cmds]
        except:
            raise CommandException(cmdline + "\n encoding trouble")

        p = Popen(cmds, shell=False, stdout=PIPE, stderr=PIPE)
        # to avoid "IOError: [Errno 4] Interrupted system call"
        time.sleep(0.01)
        out = "".join([i.decode() for i in p.stdout.readlines()]).strip()
        outerr = "".join([i.decode() for i in p.stderr.readlines()]).strip()

        if "exiftran" in cmdline:
            if "processing" in outerr:
                # exiftran output process in stderr ;-(
                outerr = ""

        if outerr:
            raise CommandException(cmdline + "\n OUTPUT ERROR:" + outerr)
        else:
            #~ try:
                #~ out = out.decode("utf_8")  # retrieve information in UTF_8
            #~ except:
                #~ try:
                    #~ # retrieve information in the old encoding (Latin_1)
                    #~ out = out.decode("latin_1")
                #~ except UnicodeDecodeError:
                    #~ try:
                        #~ out = out.decode(sys.getfilesystemencoding())
                    #~ except UnicodeDecodeError:
                        #~ raise CommandException(cmdline + "\n decoding trouble")

            return out  # unicode


class PhotoCmd(object):

    file = property(lambda self: self.__file)
    exifdate = property(lambda self: self.__exifdate)
    filedate = property(lambda self: self.__filedate)
    readonly = property(lambda self: self.__readonly)
    isflash = property(lambda self: self.__isflash)
    resolution = property(lambda self: self.__resolution)
    comment = property(lambda self: self.__comment)
    rating = property(lambda self: self.__rating)
    tags = property(lambda self: self.__tags)
    isreal = property(lambda self: self.__isreal)

    # static
    format = "p%Y%m%d_%H%M%S"

    def debug(self, m):
        print(m)

    def __init__(self, file, needAutoRename=False, needAutoRotation=False):
        #~ assert type(file) == unicode
        assert os.path.isfile(file)

        self.__file = file
        self.__readonly = not os.access(self.__file, os.W_OK)

        # pre-read

        self.__info = pyexiv.Exiv2Metadata(self.__file)
        self.__info.readMetadata()

        if self.readonly:
            self.debug("*WARNING* File %s is READONLY" % file)
        else:
            #-----------------------------------------------------------
            # try to correct exif date if wrong
            #-----------------------------------------------------------
            # if no exifdate ---> put the filedate in exifdate
            # SO exifdate = filedate FOR ALL
            if "Exif.Photo.DateTimeOriginal" in self.__info.exifKeys():
                try:
                    # self.__info[
                    #    "Exif.Image.DateTime"].strftime("%Y%m%d%H%M%S")
                    self.__info[
                        "Exif.Photo.DateTimeOriginal"].strftime("%Y%m%d%H%M%S")
                    isDateExifOk = True
                # content of tag exif DateTimeOriginal is not a datetime
                except AttributeError:
                    isDateExifOk = False
            else:  # tag exif DateTimeOriginal not present
                isDateExifOk = False

            if not isDateExifOk:
                self.debug(
                    "*WARNING* File %s had wrong exif date -> corrected"
                    % file)

                fd = datetime.fromtimestamp(os.stat(file).st_mtime)
                # mark exif made by jbrout
                self.__info["Exif.Image.Make"] = "jBrout"
                self.__info["Exif.Image.DateTime"] = fd
                self.__info["Exif.Photo.DateTimeOriginal"] = fd
                self.__info["Exif.Photo.DateTimeDigitized"] = fd
                self.__info.writeMetadata()

            # exifdate = self.__info["Exif.Image.DateTime"]
            exifdate = self.__info["Exif.Photo.DateTimeOriginal"]

            #-----------------------------------------------------------
            # try to autorot, if wanted
            #-----------------------------------------------------------
            if needAutoRotation:
                self.transform("auto")

            #-----------------------------------------------------------
            # try to autorename, if wanted
            #-----------------------------------------------------------
            if needAutoRename:
                folder = os.path.dirname(file)
                nameShouldBe = exifdate.strftime(PhotoCmd.format)
                newname = nameShouldBe + u'.' + file.split('.')[-1].lower()

                if not os.path.isfile(os.path.join(folder, newname)):
                    # there is no files which already have this name
                    # we can simply rename it
                    newfile = os.path.join(folder, newname)

                    os.rename(file, newfile)
                    self.__file = newfile
                else:
                    # there is a file, in the same folder which already got
                    # the same name

                    if nameShouldBe != \
                            os.path.basename(file)[:len(nameShouldBe)]:
                        while os.path.isfile(os.path.join(folder, newname)):
                            newname = PhotoCmd.giveMeANewName(newname)

                        newfile = os.path.join(folder, newname)

                        os.rename(file, newfile)
                        self.__file = newfile
                        # self.debug("*WARNING* File %s to be renamed -> %s"
                        #    % (file, newfile) )

        self.__refresh()

    def __refresh(self):
        self.__info = pyexiv.Exiv2Metadata(self.__file)
        self.__info.readMetadata()

        if "Exif.Image.Make" in self.__info.exifKeys():
            # except if a cam maker is named jBrout (currently, it
            # doesn't exist ;-)
            self.__isreal = (self.__info["Exif.Image.Make"] != "jBrout")
        else:
            # can only be here after a destroyInfo() or file has no exif data
            self.__isreal = False

        if "Exif.Photo.DateTimeOriginal" in self.__info.exifKeys():
            # self.__exifdate =
            #    self.__info["Exif.Image.DateTime"].strftime("%Y%m%d%H%M%S")
            self.__exifdate = \
                self.__info[
                    "Exif.Photo.DateTimeOriginal"].strftime("%Y%m%d%H%M%S")
        elif "Exif.Image.DateTime" in self.__info.exifKeys():
            self.__exifdate = \
                self.__info["Exif.Image.DateTime"].strftime("%Y%m%d%H%M%S")
        else:
            # can only be here after a destroyInfo() or if file has no
            # exif info
            self.__exifdate = ""

        self.__filedate = self.__exifdate

        #~ try:
            #~ w, h = Image.open(self.__file).size
        #~ except IOError:
            #~ w, h = 0, 0  # XXX not recognized yetwith exiv2
        w,h = self.__info.getDimensions()
        self.__resolution = "%d x %d" % (w, h)  # REAL SIZE !

        if "Exif.Photo.Flash" in self.__info.exifKeys():
            v = self.__info.interpretedExifValue("Exif.Photo.Flash")
            if v:
                if v[:2].lower() in ["fi", "ye"]:  # fired, yes, ...
                    self.__isflash = "Yes"
                else:
                    self.__isflash = "No"
            else:
                self.__isflash = ""
        else:
            self.__isflash = ""

        #~ self.__comment = decode(self.__info.getComment())
        self.__comment = self.__info.getComment()

        if "Xmp.xmp.Rating" in self.__info.xmpKeys():
            # First, XMP
            r = int(self.__info["Xmp.xmp.Rating"])
            if r < 0:
                r = 0
            elif r > 5:
                r = 5
            self.__rating = r
            if not "Exif.Image.RatingPercent" in self.__info.exifKeys() \
                    or not "Exif.Image.Rating" in self.__info.exifKeys() or \
                    self.__info["Exif.Image.Rating"] != r:
                self.__info["Exif.Image.Rating"] = self.__rating
                if r >= 5:
                    r = 99
                elif r > 1:
                    r = (r - 1) * 25
                elif r <= 0:
                    r = 0
                # short, but libexiv2 should convert this
                self.__info["Exif.Image.RatingPercent"] = r
                self.__info.writeMetadata()
        elif "Exif.Image.RatingPercent" in self.__info.exifKeys():
            # Then EXIF, RatingPercent key first
            r = int(self.__info["Exif.Image.RatingPercent"])
            if r >= 99:
                r = 5
            elif r > 1:
                r = 1 + r / 25
            elif r <= 0:
                r = 0
            self.__rating = r
            if not "Xmp.xmp.Rating" in self.__info.xmpKeys() or \
                    self.__info["Xmp.xmp.Rating"] != self.__rating:
                self.__info["Xmp.xmp.Rating"] = self.__rating
                self.__info.writeMetadata()
        elif "Exif.Image.Rating" in self.__info.exifKeys():
            # Fallback to Rating if RatingPercent is not available
            r = int(self.__info["Exif.Image.Rating"])
            if r < 0:
                r = 0
            elif r > 5:
                r = 5
            self.__rating = r
            if not "Xmp.xmp.Rating" in self.__info.xmpKeys() or \
                    self.__info["Xmp.xmp.Rating"] != self.__rating:
                self.__info["Xmp.xmp.Rating"] = self.__rating
                self.__info.writeMetadata()
        else:
            # dont touch if no rating tag was set before
            self.__rating = None

        #~ self.__tags = [decode(i) for i in self.__info.getTags()]
        self.__tags = [i for i in self.__info.getTags()]

    def __saveTB(self, f):  # not used
        self.__info.dumpThumbnailToFile(f)

    def __getThumbnail(self):
        return self.getThumbnail()
    ####################################" NEW
    def getThumbnail(self): #NEW
        try:
            return self.__info.getThumbnailData()
        except IOError:  # Cannot access image thumbnail
            return None
    ####################################"

    def showAll(self):
        for key in self.__info.exifKeys():
            # tuple to avoid unicode error in print
            print( key, (self.__info[key],) )
        for key in self.__info.iptcKeys():
            # tuple to avoid unicode error in print
            print( key, (self.__info[key],) )

    def __repr__(self):
        return """file : %s
readonly : %s
isflash : %s
resolution : %s
filedate : %s
exifdate : %s
thumb : %d
isreal : %s""" % (self.__file,
                  self.__readonly,
                  self.__isflash,
                  self.__resolution,
                  self.__filedate,
                  self.__exifdate,
                  len(self.__getThumbnail()),
                  self.__isreal,)

    def redate(self, w, d, h, m, s):
        """
        redate jpeg file from offset : weeks, days, hours, minutes, seconds
        """

        #TODO:attention au fichier sans EXIF ici !!!!

        # fd = self.__info["Exif.Image.DateTime"]
        fd = self.__info["Exif.Photo.DateTimeOriginal"]
        fd += timedelta(weeks=w, days=d, hours=h, minutes=m, seconds=s)
        return self.setDate(fd)

    def setDate(self, fd):
        """
        set absolute date of jpeg file.
        """
        if self.__readonly:
            return False
        self.__info["Exif.Image.DateTime"] = fd
        self.__info["Exif.Photo.DateTimeOriginal"] = fd
        self.__info["Exif.Photo.DateTimeDigitized"] = fd

        self.__maj()
        return True

    def clear(self):
        if self.__readonly:
            return False
        self.__info.clearTags()
        self.__maj()
        return True

    def sub(self, t):
        #~ assert type(t) == unicode
        if self.__readonly:
            return False
        if t in self.__tags:
            self.__tags.remove(t)
            self.__majTags()
            return True
        else:
            return False

    def add(self, t):
        assert type(t) == unicode
        if self.__readonly:
            return False
        if t in self.__tags:
            return False
        else:
            self.__tags.append(t)
            self.__majTags()
            return True

    def addTags(self, tags):  # *new*
        """ add a list of tags to the file, return False if it can't """
        if self.__readonly:
            return False
        isModified = False
        for t in tags:
            #~ assert type(t) == unicode
            if t not in self.__tags:
                isModified = True
                self.__tags.append(t)

        if isModified:
            self.__majTags()
        return True

    def subTags(self, tags):  # *new*
        """ sub a list of tags to the file, return False if it can't """
        if self.__readonly:
            return False

        isModified = False
        for t in tags:
            assert type(t) == unicode
            if t in self.__tags:
                isModified = True
                self.__tags.remove(t)

        if isModified:
            self.__majTags()
        return True

    def destroyInfo(self):
        """ destroy ALL info (exif/iptc)
        """
        if self.__readonly:
            return False

        # delete EXIF and IPTC tags :
        l = self.__info.exifKeys() + \
            self.__info.iptcKeys() + self.__info.xmpKeys()
        for i in l:
            try:
                del self.__info[i]
            except KeyError:  # 'tag not set'
                # the tag seems not to be here, so
                # we don't need to clear it, no ?
                pass

        self.__info.deleteThumbnail()  # seems not needed !
        self.__info.clearComment()

        self.__maj()  # so, ONLY CASE where self.exifdate == ""
        return True

    def copyInfoTo(self, file2):
        """ copy exif/iptc to "file2", return dest photonode
        """
        assert type(file2) == unicode
        assert os.path.isfile(file2)

        self.__info.copyToFile(file2)

        return PhotoCmd(file2)

    def rebuildExifTB(self):
        if self.__readonly:
            return False

        try:
            im = Image.open(self.__file)
            im.thumbnail((160, 160), Image.ANTIALIAS)
        except Exception as m:
            print( "*WARNING* can't load this file : ", (self.__file,), m )
            im = None

        if im:
            file1 = io.BytesIO()
            im.save(file1, "JPEG")
            buf = file1.getvalue()
            file1.close()
            self.__info.setThumbnailData(buf)

            self.__maj()
            return True
        else:
            return False

    def __majTags(self):
        self.__info.setTags(self.__tags)
        self.__maj()

    def __maj(self):
        try:
            # TODO Why do we catch this exception? Shouldn't it just fail?
            self.__info.writeMetadata()
        except IOError:
            pass
        self.__refresh()

    def addComment(self, c):
    # /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
        #~ assert type(c) == unicode
        c = c.strip()
        if c == "":
            self.__info.clearComment()
        else:
            self.__info.setComment(c.encode("utf_8"))

        self.__maj()
        return True

    def addRating(self, r):
    # /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
        assert type(r) == int
        # short, but libexiv2 should convert this
        self.__info["Exif.Image.Rating"] = r
        # short, but libexiv2 should convert this
        self.__info["Xmp.xmp.Rating"] = r
        if r >= 5:
            r = 99
        elif r > 1:
            r = (r - 1) * 25
        elif r <= 0:
            r = 0
        # short, but libexiv2 should convert this
        self.__info["Exif.Image.RatingPercent"] = r
        self.__maj()  # save it
        return True

    def rotate(self, sens):
    # /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
        """
        rotate LOSSLESS the picture 'file', and its internal
        thumbnail according 'sens' (R/L)
        """
        if sens == "R":
            deg = "90"
            opt = "-9"
        else:
            deg = "270"
            opt = "-2"

        if _Command.isWin:
            _Command._run([_Command._jpegtran,
                          '-rotate', deg, '-copy', 'all',
                          self.__file, self.__file])
            # rebuild the exif thumb, because jpegtran doesn't do it on windows
            self.rebuildExifTB()
        else:
            # exiftran rotate internal exif thumb
            _Command._run([_Command._exiftran, opt, '-i', self.__file])

        self.__refresh()

    def transform(self, sens):
    # /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
        """ LOSSLESS transformation of the picture 'file', and its internal
        thumbnail according 'sens'
         """
        if sens == "auto":
            if 'Exif.Image.Orientation' in self.__info.exifKeys():
                exifSens = int(self.__info['Exif.Image.Orientation'])
                if exifSens not in autoTrans.keys():
                    exifSens = 1
                sens = autoTrans[exifSens][0]
            else:
                sens = autoTrans[1][0]
        if sens == "rotate90":
            jpegtranOpt = ["-rotate", "90"]
            exiftranOpt = "-9"
        elif sens == "rotate180":
            jpegtranOpt = ["-rotate", "180"]
            exiftranOpt = "-1"
        elif sens == "rotate270":
            jpegtranOpt = ["-rotate", "270"]
            exiftranOpt = "-2"
        elif sens == "flipHorizontal":
            jpegtranOpt = ["-flip", "horizontal"]
            exiftranOpt = "-F"
        elif sens == "flipVertical":
            jpegtranOpt = ["-flip", "vertical"]
            exiftranOpt = "-f"
        elif sens == "transpose":
            jpegtranOpt = ["-transpose"]
            exiftranOpt = "-t"
        elif sens == "transverse":
            jpegtranOpt = ["-transverse"]
            exiftranOpt = "-T"

        if not(sens == "none"):
            if _Command.isWin:
                _Command._run([_Command._jpegtran] + jpegtranOpt +
                              ['-copy', 'all', self.__file, self.__file])
                # rebuild the exif thumb and reset the orientation tag,
                # because jpegtran doesn't do it on windows
                self.rebuildExifTB()
                self.__info['Exif.Image.Orientation'] = 1
                self.__maj()
            else:
                # exiftran rotate internal exif thumb
                _Command._run([_Command._exiftran, exiftranOpt,
                              '-i', self.__file])

            self.__refresh()

     # ~ def rotates(self):           # NO ROTATE LOSS LESS ;-(
        # ~ im = Image.open(self.__file)
        # ~ im = im.transpose(Image.ROTATE_90)
        # ~ im.save(self.__file)

    def isThumbOk(self):
        #  1 : thumb seems good with original (same orientation)
        #  0 : not same orientation
        # -1 : no thumb
        isThumbOk = None

        im = Image.open(self.__file)
        im.verify()
        w, h = im.size
        isImageHorizon = w > h

        t = self.__getThumbnail()
        if t:
            f = StringIO.StringIO()
            f.write(t)
            f.seek(0)
            tw, th = Image.open(f).size
            isTImageHorizon = tw > th

            if isImageHorizon == isTImageHorizon:
                isThumbOk = 1
            else:
                isThumbOk = 0
        else:
            isThumbOk = -1

        assert (self.__info["Exif.Image.DateTime"] ==
                self.__info["Exif.Photo.DateTimeOriginal"] ==
                self.__info["Exif.Photo.DateTimeDigitized"])

        return isThumbOk

    # @staticmethod
    # def normalizeName(file):
    #    """
    #    normalize name (only real exif pictures !!!!)
    #    """
    #    assert type(file) == unicode
    #    p = PhotoCmd(file)
    #    p.__rename()
    #    return p.file

    @staticmethod
    def setNormalizeNameFormat(format):
        PhotoCmd.format = format

    @staticmethod
    def giveMeANewName(name):
        n, ext = os.path.splitext(name)
        mo = re.match("(.*)\((\d+)\)$", n)
        if mo:
            n = mo.group(1)
            num = int(mo.group(2)) + 1
        else:
            num = 1

        return u"%s(%d)%s" % (n, num, ext)


    # @staticmethod
    # def prepareFile(file, needRename, needAutoRot):
    #    """
    #    prepare file, rotating/autorotating according exif tags
    #    (same things as normalizename + autorot, in one action)
    #    only called at IMPORT/REFRESH albums
    #    """
    #    assert type(file) == unicode
    #
    #
    #    if needAutoRot:
    #        if _Command.isWin:
    #            # do nothing
    #            # -> because no gpl tools which rotate well (img+thumb)
    #            #    automatically according exif
    #            #    if you provide me one, i'll integrate here
    #            pass
    #        else:
    #            _Command._run( [_Command._exiftran, '-ai', file] )
    #
    #    if needRename:
    #        return PhotoCmd.normalizeName(file)
    #    else:
    #        return file

if __name__ == "__main__":

    # ~ f = u"images_exemples/IMG_3320.JPG"
    # ~ help(pyexiv2)
    # ~ i = PhotoCmd(f)
    # ~ i.showAll()
    # ~ i.showExiv()
    # ~ print i.file
    # ~ i.autorotate()
    # ~ i.rename()
    # ~ i.destroyInfo()
    # ~ print len(i.getThumbnail())
    # ~ print i["Exif.Image.DateTime"]
    # ~ print i["Exif.Image.DateTime"]
    # ~ print i.control()
    # ~ print i
    pass
