# An application indicator to establish dynamic proxies

It reads `~/.ssh/config` and displays the list of hosts in a menu. Selecting an item in the list establishes a dynamic forward using ssh and sets up a SOCKS proxy in the system settings. Thus from this point on, your internet browser, your email client, etc will connect to internet through that proxy. Only one proxy can be up at any time, and the corresponding ssh host in the menu is displayed with a checkmark. Clicking on the currently active ssh host in the menu result in the active dynamic forward being brought down and in the system settings being reset to not use a proxy. The checkmark will disappear to indicate that it has become inactive. The menu does also feature an item "Quit" to let the user quit the application indicator, also restoring the system to not use a proxy and bringing down the ssh dynamic forward.

One may annotate ssh config file so that only some hosts are listed in the app menu:

```
Host a.b.c
  #Chaussettes yes
  User bob

Host d.e.f
  User alice
```

The first host will be listed in the menu but not the second one.
