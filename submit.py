#!/usr/bin/env python
import argparse
import json
import logging
import requests
import sys

log = logging.getLogger()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'builds', help="File containing build information (or '-' for stdin)")
    parser.add_argument('--url', '-u', required=True)
    return parser.parse_args()


def main(args=None):
    args = args or parse_args()
    if args.builds == '-':
        data = sys.stdin.read()
    else:
        data = open(args.builds).read()
    builds = json.loads(data)
    if not isinstance(builds, list):
        builds = [builds]
    for build in builds:
        submit(build, args.url)


def submit(build, url):
    data = json.dumps(build)
    resp = requests.post(
        url,
        data=data,
        headers={'Content-Type': 'application/json'},
    )
    if resp.status_code == 422:
        resp_obj = resp.json()
        issues = resp_obj['_issues'].values()
        if all(map(lambda s: 'is not unique' in s, issues)):
            pass
        else:
            log.error(resp.text)
            resp.raise_for_status()


if __name__ == '__main__':
    main()
