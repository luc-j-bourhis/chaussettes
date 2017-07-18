import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = 'fr.ljbo.chaussette'

def main():
  # Basic setup
  indicator = appindicator.Indicator.new(
    APPINDICATOR_ID,
    'Chaussette',
    appindicator.IndicatorCategory.SYSTEM_SERVICES)
  indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

  # Build menu
  menu = gtk.Menu()

  # Quit
  item_quit = gtk.MenuItem('Quit')
  item_quit.connect('activate', quit)
  menu.append(item_quit)

  # Finish menu setup
  menu.show_all()
  indicator.set_menu(menu)

  # Event loop
  gtk.main()

def quit(source):
  gtk.main_quit()

if __name__ == "__main__":
  main()
