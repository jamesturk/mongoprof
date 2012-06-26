#!/usr/bin/env python
__version__ = '0.1.0'

import time
import datetime
import signal
import argparse

from pymongo import Connection
from termcolor import colored

# global quit monitor
quit = False


def watch(dbname, refresh):
    global quit
    db = getattr(Connection('localhost'), dbname)
    db.set_profiling_level(2)
    last_ts = datetime.datetime.utcnow()
    exclude_name = '{0}.system.profile'.format(dbname)

    def ctrl_c(signal, frame):
        global quit
        print('returning profiling level to 0...')
        db.set_profiling_level(0)
        db.system.profile.drop()
        quit = True
    signal.signal(signal.SIGINT, ctrl_c)

    while not quit:
        for e in db.system.profile.find({'ns': {'$ne': exclude_name},
                                         'ts': {'$gt': last_ts}}):
            output = []
            output.append(colored('{ts:%H:%M:%S}'.format(**e), 'white'))

            if 'ns' in e:
                output.append(colored('{ns}'.format(**e), 'blue'))

            # operation
            if e['op'] == 'query':
                output.append(colored('query {query}'.format(**e), 'cyan'))
            elif e['op'] == 'update':
                output.append(colored('update {query}'.format(**e), 'green'))
            elif e['op'] == 'getmore':
                output.append(colored('getmore {0}'.format(e.get('query', '')),
                                      'grey'))
            elif e['op'] == 'command':
                output.append(colored('{command}'.format(**e), 'cyan'))
            else:
                output.append(colored('unknown operation: {op}'.format(**e),
                                      'red'))
                print(e)

            if 'nscanned' in e:
                output.append(colored('scanned {nscanned}'.format(**e),
                                      'yellow'))
            if 'ntoskip' in e:
                output.append(colored('skip {ntoskip}'.format(**e), 'blue'))
            if 'nreturned' in e:
                output.append(colored('returned {nreturned}'.format(**e),
                                      'green'))
            if e.get('scanAndOrder'):
                output.append(colored('scanAndOrder', 'red'))
            output.append(colored('{millis}ms'.format(**e), 'green'))
            print(' '.join(output))
            last_ts = e['ts']
        time.sleep(refresh)


def main():
    parser = argparse.ArgumentParser(description='watch mongo queries')
    parser.add_argument('dbname', help='name of database to watch')
    args = parser.parse_args()
    watch(args.dbname, 0.1)


if __name__ == '__main__':
    main()
