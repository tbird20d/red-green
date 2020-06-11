#!/bin/sh
#
# use test.sh -e to see only errors
# use test.sh -s (strict) to see more issues
# use test.sh -a (all) to see all issues
# use test.sh -h to see usage help
#
# use pylint --list-msgs to see message ids
#
# don't use spaces in either of these
# C0325 = superfluous-parens
# C0111 = missing-docstring
# C0103 = invalid-name
# W0612 = unused-variable
# W0702 = bare-except
# C0302 = too-many-lines
# R0902 = too-many-instance-attributes
# R0912 = too-many-branches
# R0915 = too-many-statements
# C0413 = wrong-import-position
# R0903 = too-few-public-methods
# R0914 = too-many-locals

DISABLED_IDS="C0111,C0325,C0103,W0612,W0702,C0302,R0902,R0912,R0915,C0413,R0903,R0914"

if [ "$1" = "-h" ] ; then
    echo "Usage: test.sh [option]"
    echo "  -e  = show only errors"
    echo "  -s  = show strict message (more than default)"
    echo "  -a  = show all errors and warnings"
    echo "  -h  = show this usage help"
    exit 0
fi

if [ "$1" = "-s" ] ; then
    DISABLED_IDS="C0111,C0325,C0103,C0411"
fi

if [ "$1" = "-a" ] ; then
    DISABLED_IDS="C001"
fi

# don't complain about these variable names
GOOD_NAMES="fd,d,m"

ARGS="-d $DISABLED_IDS --good-names=$GOOD_NAMES"

if [ "$1" = "-e" ] ; then
    PYTHONPATH=rgdata pylint -E $ARGS rg.cgi
else
    PYTHONPATH=rgdata pylint $ARGS rg.cgi
fi
