#!/usr/bin/env python3

import os
import sys
import atoma
import argparse
from airium import Airium
from datetime import datetime, timezone

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def make_html(feed):
    air = Airium()
    air('<!DOCTYPE html>')
    with air.html(lang="en"):
        with air.head():
            air.meta(charset="utf-8")
            air.title(_t=feed.title)
        with air.body():
            with air.div(klass="main"):
                with air.p(klass="description", style="background-color: rgb(220,220,220); margin: 1em;"):
                    air.strong(_t="Description: ")
                    air(feed.description)
                air.h1(_t="Items")
                for item in feed.items:
                    with air.div(klass="item", style="border: 1px solid white; margin: 1em; background-color: rgb(231,254,255);"):
                        with air.p():
                            air.strong(_t=item.title)
                            air(': ')
                            date = utc_to_local(item.pub_date)
                            air(date.strftime("%A, %B %d, %Y %T %z"))
                            with air.div(klass="itemdesc"):
                                air(item.description)
                            with air.div(klass="links", style="background-color: rgba(0,128,64,.25);"):
                                with air.p():
                                    air.a(href=item.link, _t="Link")
                                with air.p():
                                    air.strong(_t="Enclosures:")
                                with air.ol():
                                    for enc in item.enclosures:
                                        with air.li():
                                            air.a(href=enc.url, _t="{0} link".format(enc.type))
    return str(air)

def rss2html(inf, outf):
    outf.write(make_html(atoma.parse_rss_bytes(inf.read())))
    outf.write("\n")

parser = argparse.ArgumentParser(description='Convert RSS to HTML')

parser.add_argument('-i', '--input', metavar='INFILE', type=str, nargs=1, default='', help='Specify INFILE as RSS input file, defaults to stdin')
parser.add_argument('-o', '--output', metavar='OUTFILE', type=str, nargs=1, default='', help='Specify OUTFILE as HTML output file, defaults to stdout')

args = parser.parse_args()

if (len(args.input) > 0) and (len(args.output) > 0):
    with open(args.input[0], 'rb') as inf:
        with open(args.output[0], 'w') as outf:
            rss2html(inf, outf)
    sys.exit(0)
elif len(args.input) > 0:
    with open(args.input[0], 'rb') as inf:
        rss2html(inf, sys.stdout)
    sys.exit(0)
elif len(args.output) > 0:
    with open(args.output[0], 'w') as outf:
        rss2html(sys.stdin.buffer, outf)
    sys.exit(0)
else:
    rss2html(sys.stdin.buffer, sys.stdout)
    sys.exit(0)
