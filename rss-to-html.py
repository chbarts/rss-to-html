#!/usr/bin/env python3

import os
import sys
import atoma
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
        with air.body(style="max-width: 1080 px; margin: 0 auto !important; float: none !important;"):
            with air.div(klass="description", style="background-color: rgba(255, 255, 255, .5);"):
                with air.p():
                    air.strong(_t="Description: ")
                    air(feed.description)
            air.h1(_t="Items")
            for item in feed.items:
                with air.div(klass="item", style="border: 1px solid black;"):
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

if len(sys.argv) == 1:
    print("Usage: rss-to-html rss.xml > rss.html")
    sys.exit(0)

print(make_html(atoma.parse_rss_file(sys.argv[1])))
