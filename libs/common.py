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
import os
import sys
import urllib

from subprocess import call, Popen
from datetime import datetime


def _(m):
    return m


def cd2rd(f):  # yyyymmddhhiiss -> dd/mm/yyyy hh:ii:ss
    if f:
        if len(f) == 14:
            return f[6:8] + "/" + f[4:6] + "/" + f[:4] + " " + f[8:10] + \
                ":" + f[10:12] + ":" + f[12:14]
        else:
            return f[6:8] + "/" + f[4:6] + "/" + f[:4]
    else:
        return f


def cd2d(f):  # yyyymmddhhiiss -> datetime
    return datetime(int(f[:4]), int(f[4:6]), int(f[6:8]), int(f[8:10]),
                    int(f[10:12]), int(f[12:14]))


def ed2d(f):  # yyyy:mm:dd hh:ii:ss -> datetime (output from exif lib)
    return datetime(int(f[:4]), int(f[5:7]), int(f[8:10]), int(f[11:13]),
                    int(f[14:16]), int(f[17:19]))


def ed2cd(f):  # yyyy/mm/dd hh:ii:ss -> yyyymmddhhiiss
    if f:
        return f[:4] + f[5:7] + f[8:10] + f[11:13] + f[14:16] + f[17:19]
    else:
        return f


def format_file_size_for_display(file_size):
    KILOBYTE_FACTOR = 1024.0
    MEGABYTE_FACTOR = 1024.0 ** 2
    GIGABYTE_FACTOR = 1024.0 ** 3

    if file_size < KILOBYTE_FACTOR:
        return _('%u bytes') % file_size
    if file_size < MEGABYTE_FACTOR:
        return _('%.1f KB') % (file_size / KILOBYTE_FACTOR)
    if file_size < GIGABYTE_FACTOR:
        return _('%.1f MB') % (file_size / MEGABYTE_FACTOR)
    return _('%.1f GB') % (file_size / GIGABYTE_FACTOR)


def runWith(l, file, wait=True):
    """ try command in the list 'l' with the file 'file' """
    assert type(file) == unicode
    for c in l:
        try:
            if wait:
                call([c, file])
            else:
                Popen([c, file])
        except OSError:
            pass
        else:
            return True
    return False


def caseFreeCmp(a, b):
    if a.upper() < b.upper():
        return -1
    elif a.upper() > b.upper():
        return 1
    else:
        if a < b:
            return 1
        elif a > b:
            return -1
        else:
            return 0


def openURL(url):
    """ open the url in the current browser (don't wait the browser)"""
    if sys.platform[:3].lower() == "win":
        os.startfile(url)
    else:
        runWith(["gnome-open", "mozilla-firefox", "firefox", "konqueror",
                 "epiphany", "galeon"], unicode(url), False)


def xpathquoter(s):
    """
        make string correct for xpath in attributes
        return correct quote/simplequote around according content of s
        with concat() function if needed
        more info : http://article.gmane.org\
                    /gmane.comp.python.lxml.devel/4040/match=escape+xpath
    """
    quote = '"' in s
    squote = "'" in s
    if quote and squote:
        return "concat(%s)" % """,'"',""".join(
            [xpathquoter(i) for i in s.split('"')])
    elif squote:
        return '"%s"' % s
    else:
        return "'%s'" % s


def get_file_path_from_dnd_dropped_uri(uri):
    if sys.platform[:3].lower() == "win":
        if uri.startswith('file:///'):
            uri = uri[8:]  # 8 is len('file:///')
        elif uri.startswith('file:\\\\\\'):
            uri = uri[8:]  # 8 is len('file:///')
    else:
        if uri.startswith('file:///'):  # nautilus, rox
            uri = uri[7:]  # 7 is len('file://')
        elif uri.startswith('file:'):  # xffm
            uri = uri[5:]  # 5 is len('file:')
    path = urllib.url2pathname(uri)  # escape special chars
    path = path.strip('\r\n\x00')  # remove \r\n and NULL
    return unicode(path)


def dnd_args_to_dir_list(args):
    context, x, y, selection, info, time = args
    uri = selection.data.strip()
    uri_splitted = uri.split()
    list = []
    uri = selection.data.strip()
    uri_splitted = uri.split()  # we may have more than one file dropped
    for uri in uri_splitted:
        path = get_file_path_from_dnd_dropped_uri(uri)
        if os.path.isdir(path):
            list.append(path)
    return list

import unicodedata


def removeAccentedChars(s):
    """ unicode -> unicode """
    return unicodedata.normalize('NFKD', s).\
        encode('ascii', 'ignore').decode("ascii")


if __name__ == "__main__":
    # ~ print JBrout.home
    # ~ JBrout.conf["jo"] = "hack"
    # ~ print JBrout.conf["jo"]
    # ~ JBrout.conf.save()
    # ~ runWith(["StaRT","geany"],u"toto",False)
    # ~ pass
    assert removeAccentedChars(u"aaàöÜ") == u"aaaoU"
