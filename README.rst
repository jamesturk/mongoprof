mongowatch
==========

Log watcher for `MongoDB <http://mongodb.org>`_.

Usage
-----

./mongoprof [--host hostname] [--slowms ms] dbname

    Monitors connections to DB ``dbname`` at ``hostname``.

    --host is an optional parameter, defaults to localhost (recommended)

    If slowms is included the log level will be set to only log queries slower than ``ms``
    milliseconds.



BSD-licensed. (see LICENSE)

Copyright 2012 Sunlight Foundation, James Turk
