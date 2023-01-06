import gi
import sys
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango


class MainWindow(Gtk.Window):

    def __init__(self, title: str, ):
        super().__init__(title=title)

        self.ribbon = self.make_ribbon()
        self.sidebar = self.make_sidebar()
        self.scroll = self.make_text()

        up_down = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        left_right = Gtk.Box()
        left_right.pack_start(self.sidebar, False, True, 0)
        left_right.pack_start(self.scroll, True, True, 0)
        up_down.pack_start(self.ribbon, False, True, 0)
        up_down.pack_start(left_right, True, True, 0)

        self.add(up_down)

    def make_ribbon(self) -> Gtk.Grid:
        button = Gtk.Button(label="asd")
        button2 = Gtk.Button(label="asd")
        ribbon = Gtk.Grid()
        ribbon.attach(button, 0, 0, 1, 1)
        ribbon.attach(button2, 1, 0, 1, 1)
        return ribbon

    def make_sidebar(self) -> Gtk.Grid:
        sidebar = Gtk.Grid()
        button = Gtk.Button.new_with_label("Test")
        button.connect("clicked", self.test)
        sidebar.attach(button, 0, 0, 1, 1)
        return sidebar

    def test(self, button):
        print(self.textbuffer.serialize(self.textbuffer.get_start_iter(),
              self.textbuffer.get_end_iter(), False, False))

    def make_text(self) -> Gtk.ScrolledWindow:
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(
            "This is some text inside of a Gtk.TextView. "
            + "Select text and click one of the buttons 'bold', 'italic', "
            + "or 'underline' to modify the text accordingly."
        )
        scrolledwindow.add(self.textview)
        self.textbuffer.insert_markup(self.textbuffer.get_start_iter(), "<b>a</b>", -1)

        self.textview.set_justification(Gtk.Justification.FILL)
        self.tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
        self.tag_italic = self.textbuffer.create_tag("italic", style=Pango.Style.ITALIC)
        self.tag_underline = self.textbuffer.create_tag(
            "underline", underline=Pango.Underline.SINGLE
        )
        self.tag_found = self.textbuffer.create_tag("found", background="yellow")
        return scrolledwindow
