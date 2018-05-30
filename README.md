acpic - an acpid client
=======================

This little daemon extends [acpid](https://sourceforge.net/projects/acpid2/)
event handling capabilities. Normally, event handlers are placed by root in
`/etc/acpi/events/`. With acpic, you can place additional handlers in a per-user
`~/.config/acpi/events/` directory.

I personally use it to control PulseAudio with hardware volume buttons on my
laptop (see [examples](example-events/)).

License
-------

Copyright © 2018 [Piotr Śliwka](https://github.com/psliwka)

This work is free. You can redistribute it and/or modify it under the terms of
the Do What The Fuck You Want To Public License, Version 2, as published by Sam
Hocevar. See the [COPYING] file for more details.
