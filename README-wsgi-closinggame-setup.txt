Here is the closing game setup on closinggame.net:

nginx is the web server
 - it answers http requests on port 437 (https)
 - it communicates to uwsgi using the uwsgi protocol on network address 127.0.0.1:3031
 - config is in:
   /etc/nginx/sites-enabled - see section "location /rg"
 - to start or stop, use systemctl
   - systemctl start nginx
   - systemctl stop nginx
 - logs are in: /var/log/nginx

uwsgi is the wsgi gateway
 - it answers the uwsgi protocol on network address 127.0.0.1:3031
 - it loads python and the wsgi program ~/tbird/work/games/red-green/rg.py
 - logs are in: /var/log/wsgi/app

rg.py is the wsgi application
 - it is loaded by uwsgi
 - it is located at ~/work/games/red-green/rg.py

