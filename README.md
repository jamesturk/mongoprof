mongoprof
=========

Log watcher for [MongoDB](http://mongodb.org)

Installation
------------

Just ``python setup.py install``


Usage
-----


``./mongoprof [--host hostname] [--slowms ms] dbname``


Monitors connections to DB ``dbname`` at ``hostname``.

--host is an optional parameter, defaults to localhost (recommended)

If slowms is included the log level will be set to only log queries slower than ``ms`` milliseconds.
    
    
Example Output:

![](https://raw.githubusercontent.com/jamesturk/mongoprof/master/example.png)

