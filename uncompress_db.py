#!/usr/bin/python
import bz2
import os
import sqlite3
import sys

dumpfile = sys.argv[1] if len(sys.argv) > 1 else 'openvectors.dump.bz2'

ch = raw_input("This will re-write the existing openvectors.db. Continue?(y/n):").lower()

if ch == 'y':
    try:
        os.remove('openvectors.db')
        os.remove('openvectors.dump')
    except:
        pass
    zipfile = bz2.BZ2File(dumpfile)
    data = zipfile.read()
    dump = dumpfile[:-4]
    open(dump, 'wb').write(data)
    f = open(dump, 'r+')
    s = [y for x, y in enumerate(f) if x not in [line - 1 for line in range(3, 9)]]
    f.seek(0)
    f.write(''.join(s))
    f.truncate(f.tell())
    f.close()

    con = sqlite3.connect('openvectors.db')
    cursor = con.cursor()
    try:
        cursor.executescript(
            'CREATE TABLE open_vectors (id INTEGER NOT NULL,word TEXT(65),vector TEXT,PRIMARY KEY (id));')
    except:
        pass

    with open(dump, 'r') as f:
        for line in f:
            cursor.executescript(line)

    con.close()
    os.remove('openvectors.dump')
    print "openvectors.db has been populated!"
