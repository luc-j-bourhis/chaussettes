""" Main application """

from os import path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk, Gio as gio
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator

from chaussettes import ssh

class Chaussettes:
  """ The application

  It features a menu listing all the Host in the current user's ssh config
  file.
  """

  APPINDICATOR_ID = 'fr.ljbo.chaussette'

  def __init__(self):
    """ Setup the GUI and the business logic """
    # Basic setup
    self.indicator = appindicator.Indicator.new(
      self.APPINDICATOR_ID,
      'n/a',
      appindicator.IndicatorCategory.SYSTEM_SERVICES)
    self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

    # Build menu
    self.menu = gtk.Menu()

    # State of the connections: either 1 or 0
    self.connections = 0

    # Populate menu with ssh hosts
    config = ssh.Config(path.expanduser('~/.ssh/config'))
    self.selectable = []
    self.hosts = config.hosts
    for h in self.hosts:
      item = gtk.CheckMenuItem(
        '{}\n\t{}'.format(h.host, h.hostname) if h.hostname else
        h.host)
      item.connect('toggled', self.select, h)
      self.menu.append(item)
      self.selectable.append(item)

    # Quit
    self.menu.append(gtk.SeparatorMenuItem())
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', self.quit)
    self.menu.append(item_quit)

    # Finish menu setup
    self.menu.show_all()
    self.indicator.set_menu(self.menu)

  def main(self):
    """ Run the application """
    gtk.main()

  def setup_gnome(self, proxy):
    """ Setup or disable a SOCKS proxy in the system preferences,
    depending on the value of the flag `proxy`
    """
    s1 = gio.Settings('org.gnome.system.proxy')
    s2 = gio.Settings('org.gnome.system.proxy.socks')
    if proxy:
      s1.set_string('mode', 'manual')
      s2.set_int('port', ssh.Host.PORT)
    else:
      s1.set_string('mode', 'none')

  def select(self, item, host):
    """ Called when the toggled event is triggered for one of the menu item:
    - `item` is the instance of CheckMenuItem which triggered the event
    - `host` is the corresponding instance of ssh.Host
    """
    if not item.get_active():
      # item has been disabled
      self.connections -= 1
      host.disconnect()
      if not self.connections:
        self.setup_gnome(proxy=False)
    else:
      # item has been enabled
      self.connections += 1
      for item1 in self.selectable:
        if item1 is not item:
          item1.set_active(False)
      host.connect()
      self.setup_gnome(proxy=True)

  def quit(self, source):
    """ Quit the application """
    for h in self.hosts:
      h.disconnect()
    self.setup_gnome(proxy=False)
    gtk.main_quit()

if __name__ == "__main__":
  import logging
  ssh.module_logger.setLevel(logging.INFO)
  ssh.module_logger.addHandler(logging.StreamHandler())
  Chaussettes().main()
