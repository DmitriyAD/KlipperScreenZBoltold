import datetime
import gi
import logging

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
from jinja2 import Environment, Template

from ks_includes.KlippyGtk import KlippyGtk
from ks_includes.KlippyGcodes import KlippyGcodes
from ks_includes.screen_panel import ScreenPanel

class Panel(ScreenPanel):
    def __init__(self, screen, title, back=True, action_bar=True, printer_name=True):
        super().__init__(screen, title, back, action_bar, printer_name)
        



        button_scale = self._gtk.get_header_image_scale()
        logging.debug("Button scale: %s" % button_scale)

        self.control['macro_shortcut'] = self._gtk.ButtonImage(
            'custom-script', None, None, button_scale[0], button_scale[1])
        self.control['macro_shortcut'].connect("clicked", self.menu_item_clicked, "gcode_macros", {
            "name": "Macros",
            "panel": "gcode_macros"
        })

        self.control['estop'] = self._gtk.ButtonImage('emergency', None, None, button_scale[0], button_scale[1])
        self.control['estop'].connect("clicked", self.emergency_stop)

        self.locations = {
            'macro_shortcut': 2,
            'printer_select': 2
        }
        button_range = 3
        if len(self._config.get_printers()) > 1:
            self.locations['macro_shortcut'] = 3
            if self._config.get_main_config_option('side_macro_shortcut') == "True":
                button_range = 4

        for i in range(button_range):
            self.control['space%s' % i] = Gtk.Label("")
            self.control_grid.attach(self.control['space%s' % i], 0, i, 1, 1)

        self.control_grid.attach(self.control['estop'], 0, 4, 1, 1)

        try:
            env = Environment(extensions=["jinja2.ext.i18n"])
            env.install_gettext_translations(self.lang)
            j2_temp = env.from_string(title)
            title = j2_temp.render()
        except Exception:
            logging.debug("Error parsing jinja for title: %s" % title)

    

