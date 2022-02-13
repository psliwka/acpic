acpic - an acpid client
=======================

This little daemon extends [acpid](https://sourceforge.net/projects/acpid2/)
event handling capabilities. Normally, event handlers are placed by root in
`/etc/acpi/events/`. With acpic, you can place additional handlers in a per-user
`~/.config/acpi/events/` directory.

I personally use it to control PulseAudio with hardware volume buttons on my
laptop (see [examples](example-events/)).

Installation
------------

The easiest way is to install `acpic` with `pip`:

```
$ pip install acpic
```

Then, place your handlers in `~/.config/acpi/events/` and make `acpic` somehow
start when you log in, for example by creating an XDG-compliant entry in
`~/.config/autostart/acpic.desktop`:

```
[Desktop Entry]
Name=acpic
Comment=acpid event handler
TryExec=acpic
Exec=acpic
Type=Application
```

License
-------

Copyright © 2018-2022 [Piotr Śliwka](https://github.com/psliwka)

This work is free. You can redistribute it and/or modify it under the terms of
the Do What The Fuck You Want To Public License, Version 2, as published by Sam
Hocevar. See the [COPYING] file for more details.
