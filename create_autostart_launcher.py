#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_autostart_launcher.py
Utilitaire de création de lanceur suite à une connexion X

  Source : https://github.com/CyrilleBiot/create_autostart_launcher

__author__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__copyright__ = "Copyleft"
__credits__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__license__ = "GPL"
__version__ = "1.0"
__date__ = "2020/11/22"
__maintainer__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__email__ = "cyrille@cbiot.fr"
__status__ = "Devel"
"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
import re # regex
import os
from PIL import  Image

class FileChooserWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="FileChooser Example")
        #self.set_default_size(300, 400)

        self.long_text = "[Desktop Entry]\n" \
                    "Name=[NAME]\n" \
                    "Icon=[/path/to/icon/icon.png]\n" \
                    "Exec=[/path/to/exe/script.py]\n" \
                    "Terminal=false\n" \
                    "Type=Application\n" \
                    "X-GNOME-Autostart-enabled=true\n"

        # Set Entry Widget to the File Name
        self.entryFile = Gtk.Entry()
        self.entryFile.set_text("Chemin vers le fichier")
        self.entryFile.set_width_chars(75)
        self.entryFile.set_editable(False)

        # Set Entry Widget to the Icon
        self.entryIcon = Gtk.Entry()
        self.entryIcon.set_text("Chemin de l'icone")
        self.entryIcon.set_width_chars(75)
        self.entryIcon.set_editable(False)

        # Set Entry Widget to the Name on the starter
        self.entryName = Gtk.Entry()
        self.entryName.set_text("Nom du lanceur")
        self.entryName.set_width_chars(75)
        self.entryName.set_editable(True)

        # Set the Button to choose the File Name
        btnFileName = Gtk.Button(label="File Selection")
        btnFileName.connect("clicked", self.on_file_clicked, self.entryFile)

        # Set the Button to choose the File Ico
        self.btnFileIcon = Gtk.Button(label="Icon Selection")
        self.btnFileIcon.connect("clicked", self.on_file_clicked, self.entryIcon)

        # Set the Button to choose the File Ico
        btnName = Gtk.Button(label="Name of the starter")
        btnName.connect("clicked", self.update_textview, self.entryName)

        # a scrollbar for the child widget (that is going to be the textview)
        scrolledWindow = Gtk.ScrolledWindow()
        scrolledWindow.set_border_width(5)
        # we scroll only if needed
        scrolledWindow.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # A text Viex
        self.textView = Gtk.TextView()
        # wrap the text, if needed, breaking lines in between words
        self.textView.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textView.set_editable(False)

        # The text buffer
        self.text_buffer = self.textView.get_buffer()
        self.text_buffer.set_text(self.long_text)  # sympath pour inserer la où est le curseur mais pas nécessaire ici

        # Textview is scrolled
        scrolledWindow.add(self.textView)
        scrolledWindow.set_min_content_height(125)

        # Icon preview
        self.img = Gtk.Image()
        self.img.set_from_file('apropos.png')

        # Label to the switch
        labelSwitch = Gtk.Label(label="Mode Edition")
        labelSwitch.set_tooltip_text("Attention ! Soyez sûr des modification apportées manuellement !")


        # The Switch Button
        self.switch = Gtk.Switch()
        self.switch.connect("notify::active", self.on_switch_activated)
        self.switch.set_active(False)
        self.switch.set_vexpand(False)
        self.switch.set_hexpand(False)
        self.switch.set_halign(True)
        self.switch.set_tooltip_text("Attention ! Soyez sûr des modification apportées manuellement !")

        # Button Create starter
        btnCreateFile = Gtk.Button(label="Générer le fichier")
        btnCreateFile.connect("clicked", self.create_autostart_file)

        # Labels
        labelPreview = Gtk.Label(label="Prévisualisation du fichier généré")
        labelPreviewIcon = Gtk.Label(label="Prév. Icone")

        # Button About Dialog
        btnAbout = Gtk.Button(label="About")
        btnAbout.connect("clicked", self.on_clic_about)

        grid = Gtk.Grid()
        grid.set_column_spacing(6)
        grid.set_row_spacing(6)
        grid.set_row_homogeneous(False)
        grid.attach(self.entryName, 0, 0, 1, 1)
        grid.attach(btnName, 1, 0, 2, 1)
        grid.attach(self.entryFile,0,1,1,1)
        grid.attach(btnFileName,1,1,2,1)
        grid.attach(self.entryIcon,0,2,1,1)
        grid.attach(self.btnFileIcon,1,2,2,1)
        # Label
        grid.attach(labelPreview,0,3,3,1)
        grid.attach(labelPreviewIcon,1,4,2,1)

        grid.attach(scrolledWindow,0,4,1,10)
        grid.attach(self.img,1,5,2,1)
        grid.attach(labelSwitch,1,13,1,1)
        grid.attach(self.switch,2,13,1,1)
        grid.attach(btnCreateFile, 0, 14, 2, 1)
        grid.attach(btnAbout, 2, 14, 1, 1)

        self.add(grid)

    def warning_alert(self, widget, message1, message2):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CANCEL,
            text=message1,
        )
        dialog.format_secondary_text(message2)
        dialog.run()

        dialog.destroy()

    def create_autostart_file(self,widget):

        # If edition mode, save the current buffer. Without any test (name, file, icon...)
        if self.switch.get_active():
            print('Mode édition')
            start_iter = self.text_buffer.get_start_iter()
            end_iter = self.text_buffer.get_end_iter()
            self.long_text = self.text_buffer.get_text(start_iter, end_iter, True)
        else:
            print('NOT IN THE MODE EDITION')

            # Test of existence files to exec and icon
            if not os.path.isfile(self.entryFile.get_text()):
                print("Fichier FILE inexistant")
                msg1 = "L'exe n'est pas renseigné."
                msg2 = "Veuillez sélectionné un fichier depuis le bouton FILE."
                self.warning_alert(self, msg1, msg2)
                return

            if not os.path.isfile(self.entryIcon.get_text()):
                print("Fichier ICON inexistant")
                msg1 = "L'icone n'est pas renseigné."
                msg2 = "Veuillez sélectionné un fichier depuis le bouton ICON."
                self.warning_alert(self, msg1, msg2)
                return

            # Test is the file.desktop already exists or not
            homedir = os.environ['HOME']
            name_of_file = homedir + '/.config/autostart/' + self.entryName.get_text() + '.desktop'
            name_of_file = ''.join(name_of_file.split())
            print(name_of_file)

            if os.path.isfile(name_of_file):
                print("Le fichier existe. On quitte.")
                msg1 = "Un fichier portant ce nom existe déjà !"
                msg2 = "Veuillez changer son nom. Ou effacer le fichier déjà existant."
                self.warning_alert(self, msg1, msg2)
                return

        # Record the configuration file to  .config/autostart/NameOfFile.desktop
        file = open(name_of_file, "x")
        file.write(self.long_text)
        file.close()


    def on_switch_activated(self, switch, gparam):
        if switch.get_active():
            state = "on"
            self.textView.set_editable(True)
        else:
            state = "off"
            self.textView.set_editable(False)

    def create_text_buffer(self, widget):
        self.text_buffer.set_text(self.long_text)

    def update_textview(self, widget, varUpdate):

        # Update / Name
        if varUpdate == self.entryName:
            varUpdate = 'name'
            entryUpdate = self.entryName.get_text()
            self.long_text = re.sub("Name=.*\n", 'Name=' + entryUpdate + '\n', self.long_text)

        # Update / File path
        if varUpdate == 'file':
            entryUpdate = self.entryFile.get_text()
            self.long_text = re.sub("Exec=.*\n", 'Exec=' + entryUpdate + '\n', self.long_text)

        # Update / Icon path
        elif varUpdate == 'icon':
            entryUpdate = self.entryIcon.get_text()
            self.long_text = re.sub("Icon=.*\n", 'Icon=' + entryUpdate + '\n', self.long_text)
            self.img.set_from_file(entryUpdate)

        self.text_buffer.set_text(self.long_text)


    def on_file_clicked(self, widget, entry):

        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.add_filters(widget, dialog)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("Open clicked") #DEBUG
            print("File selected for file: " + dialog.get_filename()) # DEBUG

            # Test if image size < 48 x 48
            if widget.get_label() == "Icon Selection":
                print('This is a icon selection')
                img = Image.open(dialog.get_filename())
                print(img.size)
                if img.size[0] > 48 or img.size[1] > 48:
                    print("Size is bigger")
                    msg1 = "La taille de l'icone est inadaptée"
                    msg2 = "Veuillez sélectionné un fichier avec une taille maximale de 48X48"
                    self.warning_alert(self, msg1, msg2)
                    dialog.destroy()
                    return
            entry.set_text(dialog.get_filename())

            if entry == self.entryFile:
                entry = "file"

            if entry == self.entryIcon:
                entry = "icon"
            self.update_textview(self, entry)

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, widget, dialog):
        # Filters for the file
        if widget.get_label() == "File Selection":
            filter_text = Gtk.FileFilter()
            filter_text.set_name("Text files")
            filter_text.add_mime_type("text/plain")
            dialog.add_filter(filter_text)

            filter_py = Gtk.FileFilter()
            filter_py.set_name("Python files")
            filter_py.add_mime_type("text/x-python")
            dialog.add_filter(filter_py)

            filter_any = Gtk.FileFilter()
            filter_any.set_name("Any files")
            filter_any.add_pattern("*")
            dialog.add_filter(filter_any)

        # Filters for the icon file
        elif widget.get_label() == "Icon Selection":
            print("ICON")
            filter_png = Gtk.FileFilter()
            filter_png.set_name("Images PNG")
            filter_png.add_mime_type("image/png")
            dialog.add_filter(filter_png)

            filter_jpeg = Gtk.FileFilter()
            filter_jpeg.set_name("Images JPEG")
            filter_jpeg.add_mime_type("image/jpeg")
            dialog.add_filter(filter_jpeg)

            filter_jpg = Gtk.FileFilter()
            filter_jpg.set_name("Images JPG")
            filter_jpg.add_mime_type("image/jpeg")
            dialog.add_filter(filter_jpg)

            filter_svg = Gtk.FileFilter()
            filter_svg.set_name("Images SVG")
            filter_svg.add_mime_type("image/svg+xml")
            dialog.add_filter(filter_svg)

            filter_any = Gtk.FileFilter()
            filter_any.set_name("Any files")
            filter_any.add_pattern("*")
            dialog.add_filter(filter_any)

    def on_clic_about(self, widget):
        """
        Fonction de la Boite de Dialogue About
        :param widget:
        :return:
        """
        # Recuperation n° de version
        lignes = __doc__.split("\n")
        for l in lignes:
            if '__version__' in l:
                version = l[15:-1]
            if '__date__' in l:
                dateGtKBox = l[12:-1]

        authors = ["Cyrille BIOT"]
        documenters = ["Cyrille BIOT"]
        self.dialog = Gtk.AboutDialog()
        logo = GdkPixbuf.Pixbuf.new_from_file("./apropos.png")
        if logo != None:
            self.dialog.set_logo(logo)
        else:
            print("A GdkPixbuf Error has occurred.")
        self.dialog.set_name("Gtk.AboutDialog")
        self.dialog.set_version(version)
        self.dialog.set_copyright("(C) 2020 Cyrille BIOT")
        self.dialog.set_comments("pwgen.py.\n\n" \
                                 "[" + dateGtKBox + "]")
        self.dialog.set_license("GNU General Public License (GPL), version 3.\n"
                                "This program is free software: you can redistribute it and/or modify\n"
                                "it under the terms of the GNU General Public License as published by\n"
                                "the Free Software Foundation, either version 3 of the License, or\n"
                                "(at your option) any later version.\n"
                                "\n"
                                "This program is distributed in the hope that it will be useful,\n"
                                "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
                                "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
                                "GNU General Public License for more details.\n"
                                "You should have received a copy of the GNU General Public License\n"
                                "along with this program.  If not, see <https://www.gnu.org/licenses/>\n")
        self.dialog.set_website("https://cbiot.fr")
        self.dialog.set_website_label("cbiot.fr")
        self.dialog.set_website("https://github.com/CyrilleBiot/create_autostart_launcher")
        self.dialog.set_website_label("GIT Create Autostart Launcher")
        self.dialog.set_authors(authors)
        self.dialog.set_documenters(documenters)
        self.dialog.set_translator_credits("Cyrille BIOT")
        self.dialog.connect("response", self.on_click_response_about)
        self.dialog.run()

    def on_click_response_about(self, widget, response):
        """
        Fonction fermant la boite de dialogue About
        :param widget:
        :param response:
        :return:
        """
        self.dialog.destroy()

win = FileChooserWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()