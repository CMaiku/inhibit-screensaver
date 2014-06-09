#!/usr/bin/env python

import subprocess
import sys

from gi.repository import GLib, Gio

bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
proxy = Gio.DBusProxy.new_sync(bus, Gio.DBusProxyFlags.NONE, None,
    'org.freedesktop.ScreenSaver', '/ScreenSaver',
    'org.freedesktop.ScreenSaver', None)

cookie = proxy.Inhibit('(ss)', sys.argv[1],
    "Wrapping this command in a screensaver inhibitor")

print('Inhibited the screensaver')

try:
    subprocess.call(sys.argv[1:])
finally:
    proxy.UnInhibit('(u)', cookie)
    print('UnInhibited the screensaver')
