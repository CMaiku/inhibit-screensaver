#!/usr/bin/env python

import subprocess
import sys

from gi.repository import GLib, Gio

def main():
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

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main()
    else:
        import os.path
        print("usage: {} <program-to-wrap> [arguments to pass to program]"
            .format(os.path.basename(sys.argv[0])))
