#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import re # regex
import os

class FileChooserWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="FileChooser Example")
        self.set_default_size(300, 400)

        self.long_text = "[Desktop Entry]\n" \
                    "Name=[NAME]\n" \
                    "Icon=[/path/to/icon/icon.png]\n" \
                    "Exec=[/path/to/exe/script.py]\n" \
                    "Terminal=false\n" \
                    "Type=Application\n" \
                    "X-GNOME-Autostart-enabled=true\n"

        # Set Entry Widget to the File Name
        self.entryFile = Gtk.Entry()
        self.entryFile.set_text("Path to File")
        self.entryFile.set_width_chars(75)
        self.entryFile.set_editable(False)

        # Set Entry Widget to the Icon
        self.entryIcon = Gtk.Entry()
        self.entryIcon.set_text("Path To Icon")
        self.entryIcon.set_width_chars(75)
        self.entryIcon.set_editable(False)

        # Set Entry Widget to the Name on the starter
        self.entryName = Gtk.Entry()
        self.entryName.set_text("Name of the started")
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
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_border_width(5)
        # we scroll only if needed
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # A text Viex
        self.text_view = Gtk.TextView()
        # wrap the text, if needed, breaking lines in between words
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_view.set_editable(False)

        # The text buffer
        self.text_buffer = self.text_view.get_buffer()
        self.text_buffer.set_text(self.long_text)  # sympath pour inserer la où est le curseur mais pas nécessaire ici

        # Textview is scrolled
        scrolled_window.add(self.text_view)
        scrolled_window.set_min_content_height(125)

        # Icon preview
        self.img = Gtk.Image()
        self.img.set_from_file('apropos.png')

        # Label to the switch
        labelSwitch = Gtk.Label(label="Mode Edition")
        labelSwitch.set_tooltip_text("Attention ! Soyez sûr des modification apportées manuellement !")


        # The Switch Button
        switch = Gtk.Switch()
        switch.connect("notify::active", self.on_switch_activated)
        switch.set_active(False)
        switch.set_vexpand(False)
        switch.set_hexpand(False)
        switch.set_halign(True)
        switch.set_tooltip_text("Attention ! Soyez sûr des modification apportées manuellement !")

        # Button Create starter
        btnCreateFile = Gtk.Button(label="Générer le fichier")
        btnCreateFile.connect("clicked", self.create_autostart_file)



        grid = Gtk.Grid()
        grid.set_column_spacing(6)
        grid.set_row_spacing(6)
        #grid.set_row_homogeneous(True)
        grid.attach(self.entryName, 0, 0, 1, 1)
        grid.attach(btnName, 1, 0, 1, 1)
        grid.attach(self.entryFile,0,1,1,1)
        grid.attach(btnFileName,1,1,1,1)
        grid.attach(self.entryIcon,0,2,1,1)
        grid.attach(self.btnFileIcon,1,2,1,1)
        grid.attach(scrolled_window,0,3,1,10)
        grid.attach(self.img,1,3,1,1)
        grid.attach(labelSwitch,1,4,1,1)
        grid.attach(switch,1,5,1,1)
        grid.attach(btnCreateFile,0,13,1,1)
        self.add(grid)

    def create_autostart_file(self,widget):
        homedir = os.environ['HOME']
        name_of_file = homedir + '/.config/autostart/' + self.entryName.get_text() +'.desktop'
        name_of_file = ''.join(name_of_file.split())
        print(name_of_file)
        file = open(name_of_file, "x")
        file.write(self.long_text)
        file.close()


    def on_switch_activated(self, switch, gparam):
        if switch.get_active():
            state = "on"
            self.text_view.set_editable(True)
        else:
            state = "off"
            self.text_view.set_editable(False)

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

        if widget.get_label() == "File Selection":
            print("FILE")
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


win = FileChooserWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()