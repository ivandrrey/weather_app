#!/usr/bin/env python
import os
import sys
import time

import psycopg2


def wait_for_db():
    try:
        params = f'dbname={os.environ.get("POSTGRES_DB")} ' \
                 f'user={os.environ.get("POSTGRES_USER")} ' \
                 f'host={os.environ.get("POSTGRES_HOST")} ' \
                 f'password={os.environ.get("POSTGRES_PASSWORD")} ' \
                 f'connect_timeout=1 '
        conn = psycopg2.connect(params)
        conn.close()
        return True
    except Exception as e:
        print("DB Exception: ", e)
        return False


if __name__ == '__main__':
    while not wait_for_db():
        print("Waiting for db connection...")
        time.sleep(5)
    print("DB connection OK")
    cmd = sys.argv[1]
    env = os.environ.copy()
    args = sys.argv[1:]
    print(f'Launch known command "{cmd}"')
    os.execvpe(cmd, args, env)
