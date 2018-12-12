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

#~ import pygtk
#~ pygtk.require('2.0')
#~ import gtk
import os
#~ import gobject
import re
import unicodedata
# ~ from __main__ import _
#~ from libs.gladeapp import GladeApp
from subprocess import Popen, PIPE

class Pb:
    def fill(self,*a,**k):
        pass
class Gdk():
    COLORSPACE_RGB=""
    def pixbuf_new_from_file(self,*a,**k):
        return
    def Pixbuf(self,*a,**k):
        return Pb()
class Gtk():
    gdk=Gdk()

gtk=Gtk()


def colorToString(color):
    """
    Converts a gtk.gdk color to a string
    (fix for windows not having the to_string member function)"""
    return "#%x%x%x" % (color.red, color.blue, color.green)


#~ class WinKeyTag(GladeApp):
    #~ glade = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                         #~ 'data', 'jbrout.glade')
    #~ window = "WinKeyTag"

    #~ def init(self, title, t, l):
        #~ self.liste = [] + l
        #~ self.lblTitre.set_label(title)

        #~ l = gtk.ListStore(str, str)
        #~ self.lTags.set_model(l)

        #~ self.feed(l, t)
        #~ self.text.set_text(t)

        #~ cell_renderer = gtk.CellRendererText()
        #~ column = gtk.TreeViewColumn("tags", cell_renderer, text=0)
        #~ self.lTags.append_column(column)

        #~ cell_renderer = gtk.CellRendererText()
        #~ column = gtk.TreeViewColumn("info", cell_renderer, text=1)  # catg
        #~ self.lTags.append_column(column)

        #~ self.main_widget.show_all()
        #~ self.main_widget.set_focus(self.text)
        #~ self.text.set_position(len(t))
        #~ self.main_widget.set_title("Tag")

    #~ # def feed(self, l, s): # filter with begginning of 't'
    #~ #    l.clear()
    #~ #    s = unicode(s).lower()
    #~ #    for t, c in self.liste:
    #~ #        if t.lower().startswith(s):
    #~ #            l.append( (t, "(%s)"%c) )

    #~ def feed(self, l, s):  # filter with begginning of 't'
        #~ l.clear()
        #~ s = unicode(s).upper()
        #~ s = unicodedata.normalize('NFD', s)
        #~ s = s.encode('ascii', 'ignore')

        #~ use_regexp = 0
        #~ if s.find("*") > -1 or s.endswith("$"):
            #~ # Convert s into a regexp
            #~ use_regexp = 1
            #~ s = re.escape(s)
            #~ s = s.replace("\*", ".*")
            #~ if s.endswith("\$"):
                #~ s = s[0:len(s) - 2] + "$"

        #~ for t, c in self.liste:
            #~ u = unicode(t).upper()
            #~ u = unicodedata.normalize('NFD', u)
            #~ u = u.encode('ascii', 'ignore')
            #~ if use_regexp:
                #~ if re.match(s, u.upper()):
                    #~ l.append((t, "(%s)" % c))
            #~ else:
                #~ if u.upper().startswith(s):
                    #~ l.append((t, "(%s)" % c))

        #~ # ~ for t, c in self.liste:
            #~ # ~ u = unicode(t).upper()
            #~ # ~ u = unicodedata.normalize('NFD', u)
            #~ # ~ u = u.encode('ascii', 'ignore')
            #~ # ~ if u.upper().startswith(s):
                #~ # ~ l.append( (t, "(%s)"%c) )

    #~ def on_text_changed(self, w):
        #~ t = w.get_text().strip()
        #~ l = self.lTags.get_model()
        #~ self.feed(l, t)

    #~ def on_text_key_press_event(self, w, b):
        #~ key = gtk.gdk.keyval_name(b.keyval).lower()
        #~ if key == "escape":
            #~ self.quit()
        #~ elif key == "return":
            #~ l = self.lTags.get_model()
            #~ if len(l) == 1:
                #~ self.quit(unicode(l[0][0], "utf_8"))

    #~ def on_lTags_row_activated(self, w, p, tvc):
        #~ l = w.get_model()
        #~ self.quit(unicode(l.get(l.get_iter(p), 0)[0], "utf_8"))

    #~ def on_WinKeyTag_delete_event(self, *args):
        #~ self.quit()

    #~ def on_lTags_key_press_event(self, w, e):
        #~ key = gtk.gdk.keyval_name(e.keyval).lower()
        #~ if key == "backspace":
            #~ self.main_widget.set_focus(self.text)
            #~ self.text.set_position(len(self.text.get_text()))
        #~ elif key == "escape":
            #~ self.quit()


#~ class AlbumCommenter(gtk.Entry):
    #~ def __init__(self, canModify=True):
        #~ gtk.Entry.__init__(self)
        #~ self.connect("activate", self.save)
        #~ self.hide()

        #~ self.set_editable(canModify)

    #~ def set(self, nodeFolder):

        #~ self.show()
        #~ self.set_text(nodeFolder.comment)
        #~ self.__nf = nodeFolder

    #~ def save(self, e):
        #~ if self.__nf:
            #~ self.__nf.setComment(self.get_text().decode("utf_8"))


#~ def InputBox(parent, label, data, title=_("Jbrout Input")):
    #~ dialog = gtk.Dialog(title, parent, 0,
                        #~ (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK,
                         #~ gtk.RESPONSE_OK))
    #~ dialog.set_default_response(gtk.RESPONSE_OK)

    #~ hbox = gtk.HBox(False, 8)
    #~ hbox.set_border_width(8)
    #~ dialog.vbox.pack_start(hbox, False, False, 0)

    #~ stock = gtk.image_new_from_stock(gtk.STOCK_DIALOG_QUESTION,
                                     #~ gtk.ICON_SIZE_DIALOG)
    #~ hbox.pack_start(stock, False, False, 0)

    #~ table = gtk.Table(2, 2)
    #~ table.set_row_spacings(4)
    #~ table.set_col_spacings(4)
    #~ hbox.pack_start(table, True, True, 0)

    #~ label = gtk.Label(label)
    #~ label.set_use_underline(True)
    #~ label.set_line_wrap(True)
    #~ table.attach(label, 0, 2, 0, 1)
    #~ local_entry1 = gtk.Entry()
    #~ local_entry1.set_text(data)
    #~ local_entry1.connect("activate",
                         #~ lambda w: dialog.response(gtk.RESPONSE_OK))
    #~ table.attach(local_entry1, 0, 2, 1, 2)
    #~ label.set_mnemonic_widget(local_entry1)

    #~ dialog.show_all()

    #~ response = dialog.run()

    #~ if response == gtk.RESPONSE_OK:
        #~ ret = local_entry1.get_text().decode("utf_8")
    #~ else:
        #~ ret = None
    #~ dialog.destroy()

    #~ return ret


#~ def MessageBox(parent, data, title=_("Jbrout Message")):
    #~ dialog = gtk.Dialog(title, parent, 0,
                        #~ (gtk.STOCK_OK, gtk.RESPONSE_OK))
    #~ dialog.set_default_response(gtk.RESPONSE_OK)

    #~ hbox = gtk.HBox(False, 8)
    #~ hbox.set_border_width(8)
    #~ dialog.vbox.pack_start(hbox, False, False, 0)

    #~ stock = gtk.image_new_from_stock(gtk.STOCK_DIALOG_INFO,
                                     #~ gtk.ICON_SIZE_DIALOG)
    #~ hbox.pack_start(stock, False, False, 0)

    #~ table = gtk.Table(2, 2)
    #~ table.set_row_spacings(4)
    #~ table.set_col_spacings(4)
    #~ hbox.pack_start(table, True, True, 0)

    #~ label = gtk.Label(data)
    #~ label.set_selectable(True)
    #~ label.set_line_wrap(True)
    #~ table.attach(label, 0, 2, 0, 1)

    #~ dialog.show_all()

    #~ dialog.run()

    #~ dialog.destroy()


#~ def MessageBoxScrolled(parent, data, title=_("Jbrout Message")):
    #~ dialog = gtk.Dialog(title, parent, 0,
                        #~ (gtk.STOCK_OK, gtk.RESPONSE_OK))
    #~ dialog.set_default_response(gtk.RESPONSE_OK)
    #~ dialog.set_default_size(800, 300)

    #~ hbox = gtk.HBox(False, 8)
    #~ hbox.set_border_width(8)
    #~ dialog.vbox.pack_start(hbox, True, True, 0)

    #~ stock = gtk.image_new_from_stock(gtk.STOCK_DIALOG_INFO,
                                     #~ gtk.ICON_SIZE_DIALOG)
    #~ hbox.pack_start(stock, False, False, 0)

    #~ table = gtk.Table(2, 2)
    #~ table.set_row_spacings(4)
    #~ table.set_col_spacings(4)
    #~ hbox.pack_start(table, True, True, 0)

    #~ sw = gtk.ScrolledWindow()
    #~ tbuf = gtk.TextBuffer()
    #~ tbuf.set_text(data)
    #~ text = gtk.TextView(tbuf)
    #~ text.set_editable(False)
    #~ sw.add(text)
    #~ table.attach(sw, 0, 2, 0, 1)

    #~ dialog.show_all()

    #~ dialog.run()

    #~ dialog.destroy()


#~ def InputQuestion(parent, label, title=_("Jbrout Question"),
                  #~ buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                           #~ gtk.STOCK_OK, gtk.RESPONSE_OK)):

    #~ dialog = gtk.Dialog(title, parent, 0, buttons)
    #~ dialog.set_default_response(gtk.RESPONSE_OK)
    #~ dialog.set_has_separator(False)

    #~ hbox = gtk.HBox(False, 8)
    #~ hbox.set_border_width(8)
    #~ dialog.vbox.pack_start(hbox, False, False, 0)

    #~ stock = gtk.image_new_from_stock(gtk.STOCK_DIALOG_QUESTION,
                                     #~ gtk.ICON_SIZE_DIALOG)
    #~ hbox.pack_start(stock, False, False, 0)

    #~ table = gtk.Table(2, 2)
    #~ table.set_row_spacings(4)
    #~ table.set_col_spacings(4)
    #~ hbox.pack_start(table, True, True, 0)

    #~ label = gtk.Label(label)
    #~ label.set_use_underline(True)
    #~ label.set_line_wrap(True)
    #~ table.attach(label, 0, 2, 0, 1)
    #~ # ~ local_entry1 = gtk.Entry()
    #~ # ~ local_entry1.set_text(data)
    #~ # ~ table.attach(local_entry1, 0, 2, 1, 2)
    #~ # ~ label.set_mnemonic_widget(local_entry1)

    #~ dialog.show_all()

    #~ response = dialog.run()

    #~ ret = response == gtk.RESPONSE_OK
    #~ dialog.destroy()

    #~ return ret

##############################################################################
##############################################################################
##############################################################################

from . import pyexiv
#~ import pyexiv2


def rgb(r, g, b, a=00):
    return r * 256 * 256 * 256 + \
        g * 256 * 256 + \
        b * 256 + \
        a


class Img(object):
    def __init__(self, file=None, thumb=None, im=None):
        if file:
            try:
                im = gtk.gdk.pixbuf_new_from_file(file)
            except IOError:
                raise IOError()  # "Img() : file not found"
        elif thumb:
            extension = thumb.split('.')[-1].lower()
            try:
                # ~ fid = open(thumb, 'rb')
                # ~ jo = exif.process_file(fid)
                # ~ fid.close()
                # ~ data = jo["JPEGThumbnail"]

                img = pyexiv.Exiv2Metadata(thumb)
                img.readMetadata()
                # XXX external call while pyexiv can't handle it
                if extension == 'nef':
                    data = Popen(["exiftool", "-b", "-PreviewImage",
                                  "%s" % thumb], stdout=PIPE).communicate()[0]
                else:
                    thumbnailData = img.getThumbnailData()
                    if len(thumbnailData) > 0:
                        data = thumbnailData[1]
                    else:
                        raise KeyError

                loader = gtk.gdk.PixbufLoader('jpeg')

                loader.write(data, len(data))
                im = loader.get_pixbuf()
                loader.close()
            except IOError:
                raise IOError()  # "Img() : file not found"
            except KeyError:
                raise KeyError()  # "Img() : no exif inside"
        elif im:
            pass
        else:
            raise Exception()  # "Img() : bad call"

        self.__im = im

    def __getWidth(self):
        return self.__im.get_width()
    width = property(__getWidth)

    def __getHeight(self):
        return self.__im.get_height()
    height = property(__getHeight)

    def __getPixbuf(self):
        return self.__im
    pixbuf = property(__getPixbuf)

    # ~ def getStreamJpeg(self, quality=70):
        # ~ f = StringIO()
        # ~ self.__im.save(f, "jpeg", quality=quality)
        # ~ f.seek(0)
        # ~ return f

    def resize(self, size):
        pb = self.__im
        (wx, wy) = self.width, self.height
        rx = 1.0 * wx / size
        ry = 1.0 * wy / size
        if rx > ry:
            rr = rx
        else:
            rr = ry

        # 3= best quality (gtk.gdk.INTERP_HYPER)
        pb = pb.scale_simple(int(wx / rr), int(wy / rr), 3)
        return Img(im=pb)

    def resizeC(self, size, color=rgb(0, 0, 0)):
        # ~ pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, 0, 8, size, size)
        # ~ pb.fill(color)
        if color is not None:
            pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, 0, 8, size, size)
            pb.fill(color)
        else:
            pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, size, size)
            pb.fill(0x00000000)

        newimg = self.resize(size)

        if newimg.width == size:
            x = 0
            y = (size - newimg.height) / 2
        else:
            x = (size - newimg.width) / 2
            y = 0
        newimg.__im.copy_area(0, 0, newimg.width, newimg.height, pb, x, y)
        return Img(im=pb)

    def save(self, dest, quality=80, format="jpeg"):
        assert type(dest) == unicode
        self.__im.save(dest, format, {"quality": str(quality)})


# Class pictureselector
# This class provides a thumbnailview with a slider. It behaves as a normaol
# gtk class, and emits the signal "value_changed" whenever a user changes the
# slider

#~ class PictureSelector(gtk.VBox):

    #~ def __init__(self, photo_list):
        #~ gtk.VBox.__init__(self)

        #~ self.photo_list = photo_list

        #~ # The integer cast is for the result is needed because the dates are
        #~ # usually of type long, and a comparison needs an int
        #~ # self.photo_list.sort(lambda f, s: int(int(s.date) - int(f.date)))

        #~ self.photo_list.sort(lambda f, s: cmp(s.date, f.date))

        #~ # Create all the visual elements
        #~ self.thumb_display = gtk.Image()
        #~ self.slider = gtk.HScrollbar()
        #~ self.text_display = gtk.Label("Photo 1/1")
        #~ self.pack_start(self.thumb_display, expand=False)
        #~ self.pack_start(self.slider, expand=True, fill=True)
        #~ self.pack_start(self.text_display, expand=False)

        #~ # Initialize the slider
        #~ if (len(self.photo_list) > 1):
            #~ self.slider.set_range(1, len(self.photo_list))
            #~ self.slider.set_increments(1, 10)

        #~ self.updateDisplay()
        #~ # --Instead of this, wouldnt it make sense just to not show the slider?
        #~ # Otherwise the photo looks ugly all grey. See below
        #~ # --Daniel Patterson (dbpatterson@riseup.net) 12th June 2007

        #~ # Create the callbacks
        #~ self.slider.connect("value_changed", self.onSliderChange)

        #~ # Display everything
        #~ if (len(self.photo_list) > 1):
            #~ self.slider.show()
        #~ self.text_display.show()
        #~ self.thumb_display.show()

    #~ def onSliderChange(self, widget):
        #~ # Update the display of the text widget and the thumbnail
        #~ self.updateDisplay()

        #~ # Emit a signal that we have changed
        #~ self.emit("value_changed", self)

    #~ def getValue(self):
        #~ # Returns the index value of the photolist. Watch out for off-by-one
        #~ # errors!
        #~ slider_value = int(self.slider.get_value())
        #~ if (slider_value == 0):
            #~ slider_value = 1
        #~ return slider_value - 1

    #~ def updateDisplay(self):
        #~ photo_num = self.getValue()
        #~ if photo_num < len(self.photo_list):
            #~ self.text_display.set_text(
                #~ "Photo %d/%d: %s" % (photo_num + 1, len(self.photo_list),
                                     #~ self.photo_list[photo_num].name))
            #~ self.thumb_display.set_from_pixbuf(
                #~ self.photo_list[photo_num].getThumb())

    #~ def set_sensitive(self, value):
        #~ # Make the widget greyed out or active. If the photo list has only one
        #~ # picture, it can never be active
        #~ if value and (len(self.photo_list) < 2):
            #~ value = False

        #~ if value:
            #~ gtk.VBox.set_sensitive(self, True)
        #~ else:
            #~ gtk.VBox.set_sensitive(self, False)

#~ # Create the "value_changed" signal and connect it to the PictureSelector class
#~ gobject.signal_new("value_changed", PictureSelector,
                   #~ gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                   #~ (gobject.TYPE_PYOBJECT,))


class Buffer(object):   # NOT NEEDED ANYMORE, buffer is handle on client side (thanks browser)
    size = None

    images = {}
    # ~ pixbufRefresh = gtk.gdk.pixbuf_new_from_file( "data/gfx/refresh.png" )
    pixbufRefresh = Img("data/gfx/refresh.png").pixbuf

    pbFolder = Img("data/gfx/folder.png").pixbuf
    pbBasket = Img("data/gfx/basket.png").pixbuf

    pbReadOnly = Img("data/gfx/check_no.png").pixbuf

    pbCheckEmpty = Img("data/gfx/check_false.png").pixbuf
    pbCheckInclude = Img("data/gfx/check_true.png").pixbuf
    pbCheckExclude = Img("data/gfx/check_no.png").pixbuf
    pbCheckDisabled = Img("data/gfx/check_disabled.png").pixbuf

    pixRaw = Img("data/gfx/raw.png").pixbuf

    @staticmethod
    def remove(file):
        if file in Buffer.images:
            del(Buffer.images[file])
            return True
        else:
            return False

    @staticmethod
    def clear():
        size = Buffer.size or 160
        Buffer.images = {}
        Buffer.pixbufNF = Img("data/gfx/imgNotFound.png").resizeC(size).pixbuf
        Buffer.pixbufNFNE = Img("data/gfx/imgNotFound.png").resizeC(
            size, rgb(255, 0, 0)).pixbuf

        Buffer.pixbufNT = Img("data/gfx/imgNoThumb.png").resizeC(size).pixbuf
        Buffer.pixbufNTNE = Img("data/gfx/imgNoThumb.png").resizeC(
            size, rgb(255, 0, 0)).pixbuf

        Buffer.pixbufERR = Img("data/gfx/imgError.png").resizeC(size).pixbuf
        Buffer.pixbufERRNE = Img("data/gfx/imgError.png").resizeC(
            size, rgb(255, 0, 0)).pixbuf

if __name__ == "__main__":
    pass
