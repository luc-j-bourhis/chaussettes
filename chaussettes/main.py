from os import path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator

from chaussettes import ssh

class Chaussettes:

  APPINDICATOR_ID = 'fr.ljbo.chaussette'

  def __init__(self):
    # Basic setup
    self.indicator = appindicator.Indicator.new(
      self.APPINDICATOR_ID,
      'n/a',
      appindicator.IndicatorCategory.SYSTEM_SERVICES)
    self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

    # Build menu
    self.menu = gtk.Menu()

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
    gtk.main()

  def select(self, item, host):
    if not item.get_active():
      # item has been disabled
      host.disconnect()
    else:
      # item has been enabled
      host.connect()
      for item1 in self.selectable:
        if item1 is not item:
          item1.set_active(False)

  def quit(self, source):
    for h in self.hosts:
      h.disconnect()
    gtk.main_quit()

if __name__ == "__main__":
  import logging
  ssh.module_logger.setLevel(logging.INFO)
  ssh.module_logger.addHandler(logging.StreamHandler())
  Chaussettes().main()
