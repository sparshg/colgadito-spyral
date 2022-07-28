#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2012, Gonzalo Odiard <godiard@gmail.com>
# Copyright (C) 2012, Walter Bender <walter@sugarlabs.org>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# HelpButton widget

from gettext import gettext as _

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk

from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.icon import Icon
from sugar3.graphics import style

import logging

''' Set up a help palette for the main toolbars '''
help_palettes = {}
help_windows = {}
help_box = Gtk.VBox()
help_box.set_homogeneous(False)
help_palettes['main-toolbar'] = help_box
help_windows['main-toolbar'] = Gtk.ScrolledWindow()
help_windows['main-toolbar'].set_size_request(
    int(Gdk.Screen.width() / 3),
    Gdk.Screen.height() - style.GRID_CELL_SIZE * 3)
help_windows['main-toolbar'].set_policy(
    Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
help_windows['main-toolbar'].add_with_viewport(
    help_palettes['main-toolbar'])
help_palettes['main-toolbar'].show()

class HelpButton(Gtk.ToolItem):

    def __init__(self, activity):
        self._activity = activity

        Gtk.ToolItem.__init__(self)

        help_button = ToolButton('toolbar-help')
        help_button.set_tooltip(_('Ayuda'))
        self.add(help_button)
        help_button.show()

        self._palette = help_button.get_palette()

        help_button.connect('clicked', self.__help_button_clicked_cb)

    def set_current_palette(self, name):
        self._current_palette = name

    def __help_button_clicked_cb(self, button):
        self._palette.set_content(help_windows['main-toolbar'])
        help_windows['main-toolbar'].show_all()

        self._palette.popup(immediate=True, state=1)


def add_section(help_box, section_text, icon=None):
    ''' Add a section to the help palette. From helpbutton.py by
    Gonzalo Odiard '''
    max_text_width = int(Gdk.Screen.width() / 3) - 20
    hbox = Gtk.HBox()
    label = Gtk.Label()
    label.set_use_markup(True)
    label.set_markup('<b>%s</b>' % section_text)
    label.set_line_wrap(True)
    label.set_size_request(max_text_width, -1)
    hbox.add(label)
    if icon is not None:
        _icon = Icon(icon_name=icon)
        hbox.add(_icon)
        label.set_size_request(max_text_width - 20, -1)
    else:
        label.set_size_request(max_text_width, -1)

    hbox.show_all()
    help_box.pack_start(hbox, False, False, padding=5)


def add_paragraph(help_box, text, icon=None):
    ''' Add an entry to the help palette. From helpbutton.py by
    Gonzalo Odiard '''
    max_text_width = int(Gdk.Screen.width() / 3) - 20
    hbox = Gtk.HBox()
    label = Gtk.Label(label=text)
    label.set_justify(Gtk.Justification.LEFT)
    label.set_line_wrap(True)
    hbox.add(label)
    if icon is not None:
        _icon = Icon(icon_name=icon)
        hbox.add(_icon)
        label.set_size_request(max_text_width - 20, -1)
    else:
        label.set_size_request(max_text_width, -1)

    hbox.show_all()
    help_box.pack_start(hbox, False, False, padding=5)

    return hbox

add_section(help_box, "Cómo jugar")
add_paragraph(help_box, "¡Descubre las frases ocultas y asegúrate de comprender su significado!")
add_paragraph(help_box, "Presiona cualquier letra para empezar.")
add_paragraph(help_box, "")
add_section(help_box, "Taller del Artesano")
add_paragraph(help_box, "Tu experiencia no es completa hasta que no hayas modificado el programa.")
add_paragraph(help_box, "")
add_section(help_box, "Cómo modificar este juego")
add_paragraph(help_box, "Vista de juego.", icon="gamecanvas")
add_paragraph(help_box, "Modifica el juego.", icon="view-source")
add_paragraph(help_box, "Guarda tus cambios.", icon="dialog-ok")
add_paragraph(help_box, "Reinicia para ver tus cambios en acción.", icon="system-restart")
add_paragraph(help_box, "La consola permite analizar tu programa y encontrar errores o realizar pruebas.", icon="sources")

