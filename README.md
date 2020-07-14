quickstart
==========
To start a new game, you can just and access the cgi script (rg.cgi)
and click 'reset', then click 'really reset!!'

See "how to test" below, for different methods of running
a standalone local instance of a server that can serve the script.

Running under another web server
================================
To run on a machine with an existing web server,
put rg.cgi into /usr/lib/cgi-bin, and change the
data path to where you put the trivia.py and rps.py files.  The data
path must be read/writable by the cgi script (which means the
web server).

Then point your browser at: http://server.address/cgi-bin/rg.cgi
for the CGI version of the script, or
use: http://server.address/rg
for the WSGI verison of the script

Running with local web server
=============================
To run on a machine without a web server, run ./start-cgi-server.

Then point your browser at: http://localhost:8000/rg.cgi

To log in as admin, use this url:
http://localhost:8000/rg.cgi?user_id=admin_game_admin

Running with apache2
====================
I added the following line to /etc/apache2/conf-available/wsgi.conf

  WSGIScriptAlias /rg /usr/lib/cgi-bin/rg.cgi

Executing the game
==================

pre-game
--------
Remove user registration files in the rgdata directory
Remove winner files in the rgdata directory
Remove leftover answer, rps, and still-in data
('make clean' will do this)

Operating the game
------------------
On the admin screen, you will see a menu showing controls for the game.

there are 4 main phases:
 - registration
 - trivia
 - rock-paper-scissors
 - end

The game progresses in 2 sets of rounds, for two different games:
1 Red-green trivia game
2 rock-paper-scissors game

Every operation performed (link clicked, or data entry submitted)
changes the game's data file.
If you click on the wrong thing, or enter the wrong data, you can
click 'undo' to revert to a previous game state.

how to test (on specific machines)
==================================
There are notes for Tim's development machines.

desktop machine local work
--------------------------
 - this runs the script as a single-threaded, single-process CGI
   using a python web server
 - cd ~/work/games/red-green ; ./start_server
 - browse as admin:
   - firefox: http://localhost:8000/rg.cgi?user_id=admin-game-admin
 - browse as user:
   - desktop: chrome chrome: http://localhost:8000/rg.cgi?user_id=one
   - laptop: chrome: http://desktop:8000/rg.cgi?user_id=two

personal server work
--------------------
 - edit rg.cgi
   - cd ~/work/games/red-green/cgi-bin
   - vi rg.cgi
   - ./stop-uwsgi
   - (in other window) ./start-uwsgi
 - browse as admin:
   - firefox https://server-addr/rg?user_id=admin-game-admin
 - browse as user:
   - desktop: chrome https://server-addr/rg (register as 'one')
   - laptop: chrome https://server-addr/rg (register as 'two')

closinggame.net work
--------------------
 - start server and wsgi gateway
   - systemctl start nginx (if not already running)
   - cd ~/work/games/red-green
   - ./start-uwsgi
 - edit rg.cgi
   - cd ~/work/games/red-green
   - vi rg.cgi
 - browse as admin:
   - firefox https://closinggame.net/rg?user_id=admin-game-admin
 - browse as user:
   - timdesk: chrome https://closinggame.net/rg (register as 'one')
   - laptop: chrome https://closinggame.net/rg (register as 'two')

linux laptop work
-----------------
 - this runs the script as a single-threaded, single-process CGI
   using a python web server
 - cd ~/work/games/red-green ; ./start_old_server
 - browse as admin:
   - firefox: http://localhost:8000/rg.cgi?user_id=admin-game-admin
 - browse as user:
   - desktop: chrome chrome: http://localhost:8000/rg.cgi?user_id=one
   - laptop: chrome: http://desktop:8000/rg.cgi?user_id=two

