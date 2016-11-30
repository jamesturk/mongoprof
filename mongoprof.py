#!/usr/bin/env python
__version__ = '0.3.0'

import time
import datetime
import signal
import argparse

from pymongo import Connection
from termcolor import colored

# global quit monitor
quit = False


def watch(host, dbname, refresh, slowms=0):
    global quit
    db = getattr(Connection(host), dbname)
    # 1 - slow operations
    # 2 - all operations
    db.set_profiling_level(1 if slowms else 2, slowms)
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
        for e in db.system.profile.find({'ns': {'$ne': exclude_name}, 'ts': {'$gt': last_ts}}):
            output = []
            output.append(colored('{ts:%H:%M:%S}'.format(**e), 'white'))

            if 'ns' in e:
                output.append(colored('{ns}'.format(**e), 'blue'))

            # operation
            op = e.get('op')
            if op == 'query':
                output.append(colored('query {query}'.format(**e), 'cyan'))
            elif op == 'update':
                output.append(colored('update {query}'.format(**e), 'green'))
            elif op == 'getmore':
                output.append(colored('getmore {0}'.format(e.get('query', '')), 'grey'))
            elif op == 'command':
                output.append(colored('{command}'.format(**e), 'cyan'))
            else:
                output.append(colored('unknown operation: {0}'.format(op), 'red'))
                print(e)

            if 'nscanned' in e:
                output.append(colored('scanned {nscanned}'.format(**e), 'yellow'))
            if 'ntoskip' in e:
                output.append(colored('skip {ntoskip}'.format(**e), 'blue'))
            if 'nreturned' in e:
                output.append(colored('returned {nreturned}'.format(**e), 'green'))
            if e.get('scanAndOrder'):
                output.append(colored('scanAndOrder', 'red'))

            if 'millis' in e:
                output.append(colored('{millis}ms'.format(**e), 'green'))
            print(' '.join(output))
            last_ts = e['ts']
        time.sleep(refresh)


def main():
    parser = argparse.ArgumentParser(description='watch mongo queries')
    parser.add_argument('dbname', help='name of database to watch')
    parser.add_argument('--host', help='hostname', default='localhost')
    parser.add_argument('--slowms', type=int, default=0,
                        help='only show transactions slower than ms')
    args = parser.parse_args()
    watch(args.host, args.dbname, 0.1, args.slowms)


if __name__ == '__main__':
    main()
