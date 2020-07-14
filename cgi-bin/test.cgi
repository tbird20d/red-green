#!/bin/sh

echo "Content-type: text/html"
echo
echo "<html>"
echo "<head>"
echo "<title>test cgi script</title>"
echo "</head>"
echo "<body>Here is the CGI environment:"
echo "<pre>"
env
echo "</pre>"
echo "</body>"
echo "</html>"
