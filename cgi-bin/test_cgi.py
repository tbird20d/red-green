#!/usr/bin/env python

import os

print "Content-type: text/html"
print ""
print "<html>\n<body>\nHi there<br>"

env_keys = os.environ.keys()
env_keys.sort()
print "Here is the environment:"
print "<ul>"
for key in env_keys:
    print "<li>%s=%s" % (key, os.environ[key])
print "</ul>"

print """<p>Back to <a href="/index.html">/index.html</a>"""

