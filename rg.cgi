#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
#
# Copyright 2020 by Sony Corporation
#
# Author: Tim Bird <tim.bird@sony.com> or <tbird20d@yahoo.com>
#
# This is an implementation of the "red-green" trivia game, often
# used for the closing game session of the Embedded Linux Conference.
# This can be used as either a CGI script or a WSGI script.
#
# See "GAME DATA and state machine" below for a description of
# game data.
#
# Implementation notes:
#   j in front of variable means "junk_" - something that is discarded
#   and not used in the function
#

import sys
import os
import cgi
import re
import copy
import time

VERSION=(2, 1, 0)

# turn this on to show the game data in the admin view
# (for debugging)
show_data = False
user_show_data = False

data_dir = "/home/tbird/work/games/red-green/rgdata/"
user_dir = data_dir + "users/"
still_in_dir = data_dir + "still_in/"
still_in_backup = data_dir + "still_in_backup/"

# keep pages from automatically refreshing, while I'm debugging
rfile =  data_dir + "suppress_refresh"
default_suppress_refresh = os.path.exists(rfile)
#default_suppress_refresh = True

def log_this(msg):
   t = time.time()
   tfrac = int((t - int(t))*100)
   timestamp = time.strftime("%Y-%m-%d_%H:%M:%S.") + "%02d" % tfrac

   with open(data_dir+"rg.log", "a", encoding="utf-8") as f:
       f.write("[%s] %s\n" % (timestamp, msg))

# mode indicates whether we're doing a group play (with an admin game
# moderator) or just letting a single user run through the questions
# to get their own score.
# this has a significant effect on the game mechanics
SINGLE="single"
#default_mode = SINGLE
default_mode = "group"

# in single-player mode:
#   question forms have a timeout
#   each user has their own game data file  to control game state
#   each page must automatically drive to the next status
#   start_trivia, and done are automatic
#   declare_winners is not supported
#   users are allowed to make state changes
# in multi-player
#   administrator makes all game state changes

# STATUS consts
STILL_IN = "still-in"
OUT = "out"

# import the trivia data
if data_dir not in sys.path:
    sys.path.append(data_dir)

from trivia import tdata
from rps import rps_data

game_file_pattern = "rgdata-([0-9][0-9][0-9]).txt"
game_file_fmt = "rgdata-%03d.txt"

winner_file_fmt = "winners-%02d.txt"
CGI_URL = "/cgi-bin/rg.cgi"
WSGI_URL = "/rg"
if os.path.isdir("/var/www/owncloud/red-green/images"):
    IMAGE_URL = "/red-green/images"
else:
    IMAGE_URL = "/images"

REFRESH_SECONDS = 2

# To login as administrator, use the url:
# http://localhost:8000/rg.cgi?user_id=admin-game-admin
#  or enter: admin-game-admin, Real Name=Tim in the registration form
ADMIN_USER_ID = "admin-game-admin"
ADMIN_NAME = "Tim"

OBSERVER_USER_ID = "observer"

NOBODY_USER_ID = "nobody-not-logged-in"

# trivia.py provides the trivia data in the form of the 'tdata' dictionary
# Each entry is a list, with question_num as the key:
# This list has the following items:
#    0) question text
#    1) red answer text
#    2) green answer text
#    3) both answer text
#    4) answer code
#    5) answer text (explanation)
#
# The answer code can be "red", "green", or "both".
# The answer can consist of multiple answers (for fake-out or lenient questions)
# Multiple correct answers are separated by a vertical bar ('|')
# example: "red|green"
#
# {1: ["question #1", "true", "false", "" "red", "answer #1 because..."],
#  2: ["question #2", "less than 10", "10 or more", "", "green", "answer #2"],
#  ...
# }

# rps.py provides the this will provide the 'rps_data' dictionary
# Each entry is a string with, round_num as the key:
# The host_throw can be "rock", "paper", or "scissors".
#
# {1: "rock",
#  2: "scissors",
#  ...
# }

#  GAME DATA and state machine
# The game has 4 phases:
#   - registration          (phase="registration")
#   - red-green trivia      (phase="trivia")
#   - rock-paper-scissors   (phase="rps")
#   - done                  (phase="done")
#
# each question goes through a state machine:
#   ask_question, wait_for_answer, show_answer
#   for a player, the ask_question page has the question and a form
#      when the player responds, they go to the "wait_for_answer" state
#      the admin has a screen showing the number of players who have voted
#       as well as the number of players "still-in"
#   the state "wait_for_answer" is entered per-user
#   everyone stays in the "wait_for_answer" state until the administrator
#    changes the global state to "show_answer"
#   In the show_answer state, user answers are checked, and their status is updated
#     this writes a new status to their user file
#
# The game progresses as a series of rounds.
#   within the trivia each round consists of several questions:
#   for each question:
#     players are presented with a question and a form to answer
#     when players have answered, they sit on a "waiting" page
#     when the administrator reveals the answer, each player sees their outcome
#     when the administrator moves to the next question, each player sees the question page
#     - a user is in one of 3 states: "question", "waiting", "answer"
#     - the admin goes from "question" to "waiting"
#     - the user goes from "question" to "waiting"
#     - the admin goes from "waiting" to "answer"
#     - the admin goes from "waiting" to "answer"
#
# there are two views of the game, the player view.  If player_view=1,
# the the player_view is shown, an no actions are processed.
# if answer_to_show is not zero, then an answer is shown in player_view
#
# The player view automatically refreshes for certain pages,
# so as the game state changes, it should change without manual intervention.
#
# The admin screen allows changing the game state.
#
class data_class(object):
    def __init__(self):
        self.data = {}
        self.html = []
        self.err_msg_list = []
        self.admin_view = False
        self.is_observer = False
        self.notice_list = []
        self.suppress_refresh = default_suppress_refresh
        self.refresh_count = REFRESH_SECONDS
        self.is_form_page = False
        self.header_shown = False
        self.cookie = ""
        self.resp_status = "200 OK"
        self.resp_headers = [('Content-type', 'text/html')]
        self.is_wsgi = False
        self.url = CGI_URL
        self.image_url = IMAGE_URL
        self.rps_image_size = 80
        self.mode = default_mode
        self.user = None

        # here is the game data
        self.game_attr_list = ['sequence', 'winner_group', 'phase',
                               'state', 'question_num', 'round_num']
        self.game_attr_ints = ['sequence', 'winner_group',
                               'question_num', 'round_num']
        self.sequence = 0
        self.winner_group = 0
        self.phase = "registration"  # registration, trivia, rps, done
        self.state = "question"  # question, wiating, answer, winners
           # or, for rps: query, waiting, result, winners
        self.question_num = 1
        self.round_num = 1

        self.game_file_mtime = 0

    def set_data(self, new_data):
        for key in list(new_data.__dict__.keys()):
            if key in self.game_attr_list:
                self.__dict__[key] = new_data.__dict__[key]

    def __getitem__(self, key):
        if key in self.data:
            item = self.data[key]
        elif hasattr(self, key):
            item = getattr(self, key)
        else:
            raise KeyError

        if callable(item):
            return item(self)
        else:
            return item

    def __setitem__(self, key, value):
        self.data[key] = value

    def has_key(self, key):
        return key in self.data

    def keys(self):
        # FIXTHIS - are the __dict__ keys needed?
        keys = list(self.__dict__.keys())
        keys.extend(list(self.data.keys()))
        return keys

######################################################

    def html_append(self, html):
        if isinstance(html, str):
            self.html.append(html.encode("utf-8"))
        else:
            self.html.append(html)

    def emit_html(self):
        # trick to change encoding of sys.stdout to utf8
        #import io
        #sys.stdout = io.open(sys.stdout.fileno(), 'w', encoding='utf8')
        for hline in self.html:
            # uncomment this to enable debugging, via a custom log file
            #log_this(hline)

            # output each line as bytes
            sys.stdout.buffer.write(hline)
        self.html = []

    def add_error_message(self, msg):
        self.err_msg_list.append('<font color="red">ERROR: %s<br></font>' % msg)
        # give time for user to see error
        self.refresh_count = 10

    def get_errors_as_html(self):
        html = ""
        if self.err_msg_list:
            html += '<table bgcolor="pink"><tr><td>\n'
            last_msg = self.err_msg_list[-1]
            for msg in self.err_msg_list:
                html += msg+"\n"
                if msg != last_msg:
                    html += "<BR>\n"
            html += '</td></tr></table>\n'
            self.err_msg_list = []
        return html

    def add_notice(self, msg):
        self.notice_list.append('<font color="green">NOTE: %s<br></font>' % msg)

    def get_notices_as_html(self):
        html = ""
        if self.notice_list:
            html += '<table bgcolor="lime"><tr><td>\n'
            last_msg = self.notice_list[-1]
            for msg in self.notice_list:
                html += msg+"\n"
                if msg != last_msg:
                    html += "<BR>\n"
            html += '</td></tr></table>\n'
            self.notice_list = []
        return html

    def debug_data(self):
        d = self.__dict__.copy()
        for attr in ["html", "err_msg_list", "notice_list", "game_attr_ints", "game_attr_list"]:
            del d[attr]
        return str(d)


######################################################

stub_data = data_class()

######################################################

class user_class(object):
    def __init__(self, user_id, alias, name, email, status=STILL_IN):
        self.user_id = user_id
        self.alias = alias
        self.name = name
        self.email = email
        # status can be STILL_IN or OUT
        self.status = status
        self.last_answer = ""
        self.logged_in = False

    def write_file(self):
        line = "%s,%s,%s,%s,%s,%s\n" % (self.user_id, self.alias, self.name,
                                        self.email, self.status,
                                        self.last_answer)
        user_filepath = user_dir + self.user_id
        fd = open(user_filepath, "w", encoding="utf-8")
        fd.write(line)
        fd.close()

    def save_answer(self, data, form, answer):
        # make sure answer is for current question
        if data.phase == "trivia":
            try:
                qnum = form["qnum"].value
            except:
                data.add_error_message("Question form missing 'qnum'")
                qnum = 0

            if int(qnum) != data.question_num:
                data.add_error_message(
                  "Incorrect question num %s in form<br>" % qnum + \
                  "Discarding answer for this question. " + \
                  "Maybe you got behind in the game??")
                return

            if data.state != "question":
                data.add_error_message(
                  "I'm sorry - you missed your opportunity to respond<br>" + \
                  "Discarding answer for this question. " + \
                  "Maybe you got behind in the game??")
                return

        elif data.phase == "rps":
            try:
                rnum = form["rnum"].value
            except:
                data.add_error_message("Question form missing 'rnum'")
                rnum = 0

            if int(rnum) != data.round_num:
                data.add_error_message(
                  "Incorrect round num %s in form<br>" % rnum + \
                  "Discarding throw for this round. " + \
                  "Maybe you got behind in the game??")
                return

            if data.state != "query":
                data.add_error_message(
                  "I'm sorry - you missed your opportunity to respond<br>" + \
                  "Discarding answer for this question. " + \
                  "Maybe you got behind in the game??")
                return
        else:
            data.add_error_message(
              "I'm sorry - you missed your opportunity to respond<br>" + \
              "Discarding answer for this question. " + \
              "Maybe the game is over or restarted??")
            return

        # put answer in user file (old method)
        self.last_answer = answer
        self.write_file()

        # put answer in separate file (new method)
        answer_dir = get_current_answer_dir(data)
        if not os.path.isdir(answer_dir):
            os.mkdir(answer_dir)

        answer_filepath = answer_dir + "/" + self.user_id
        try:
            fd = open(answer_filepath, "w", encoding="utf-8")
            fd.write(answer)
            fd.close()
        except:
            data.add_error_message("could not write to answer file %s" % answer_filepath)

    # FIXTHIS - user.save_status is unused
    def save_status(self, data, status):
        # put status in user file (old method)
        user.status = status
        self.write_file()

        # still-in status is kept in a different directory (new method)
        # remove still_in status if we're eliminated
        status_filepath = still_in_dir + self.user_id
        if status != STILL_IN and os.path.exists(status_filepath):
            os.remove(status_filepath)

######################################################

def read_game_data_from_last_file(data):
    # read from the last-numbered game-data file
    file_list = os.listdir(data_dir)
    max_sequence = -1
    max_filename = "no-game-data-file"
    for filename in file_list:
        m = re.match(game_file_pattern, filename)
        if m:
            sequence = int(m.groups()[0])
            if sequence > max_sequence:
                max_sequence = sequence
                max_filename = filename

    if max_filename == "no-game-data-file":
        return copy.deepcopy(stub_data)

    last_game_filename = data_dir + max_filename
    return read_game_data(data, last_game_filename)

######################################################

# FIXTHIS - may need to save off err_msg_list and html, in case
# they already have data
def read_game_data(data, game_filename):
    try:
        game_lines = open(game_filename, "r", encoding="utf-8").readlines()
    except:
        data.add_error_message("Warning: failed to open game data file: %s\n<p>\n" % game_filename)
        game_lines = []

    for line in game_lines:
        line = line.strip()
        if line and line[0] != '#':
            (name, value) = line.split('=', 1)
            if name in data.game_attr_list:
                if name in data.game_attr_ints:
                    value = int(value)
                setattr(data, name, value)

    data.game_filename = game_filename
    try:
        data.game_file_mtime = os.path.getmtime(game_filename)
    except:
        data.game_file_mtime = time.time()
    return data

######################################################

def write_game_data(data):
    # write out file to next filename in sequence

    # increment sequence number
    data.sequence += 1
    game_filename = data_dir + game_file_fmt % data.sequence
    data.game_filename = game_filename

    fd = open(game_filename, "w", encoding="utf-8")
    klist = list(data.keys())
    klist.sort()
    for name in klist:
        if name in data.game_attr_list:
            fd.write("%s=%s\n" % (name, str(getattr(data, name))))
    fd.close()

######################################################

def remove_undo_data_files():
    # scan for game-data files
    file_list = os.listdir(data_dir)
    for filename in file_list:
        m = re.match(game_file_pattern, filename)
        if m:
            target = data_dir + filename
            os.unlink(target)

def reset_answers_and_users(data):
    num_questions = len(tdata)
    data.phase = "trivia"
    for qnum in range(num_questions):
        data.question_num = qnum
        clear_current_answers(data)

    num_rounds = len(rps_data)
    data.phase = "rps"
    for rnum in range(num_rounds):
        data.round_num = rnum
        clear_current_answers(data)

    # erase all old still_in files
    file_list = os.listdir(still_in_dir)
    for f in file_list:
        os.remove(still_in_dir + f)

    make_all_users_still_in(data)

def get_registered_user_count():
    return len(os.listdir(user_dir))

######################################################

# returns answer dir, or None if we're in the wrong phase
def get_current_answer_dir(data):
    if data.phase == "trivia":
        return data_dir + "trivia-q%d/" % (data.question_num)
    elif data.phase == "rps":
        return data_dir + "rps-r%d/" % (data.round_num)
    else:
        return None

######################################################

# returns (user_count, answer_count, still_in_count)
def get_status_counts(data):
    file_list = os.listdir(user_dir)
    user_count = len(file_list)

    answer_dir = get_current_answer_dir(data)
    if answer_dir and os.path.exists(answer_dir):
        answer_count = len(os.listdir(answer_dir))
    else:
        answer_count = 0

    still_in_count = len(os.listdir(still_in_dir))

    return (user_count, answer_count, still_in_count)

def show_status_counts(data):
    (user_count, answers, still_in) = get_status_counts(data)

    last_question = len(list(tdata.keys()))
    last_round = len(list(rps_data.keys()))
    last_update_time = time.time() - data.game_file_mtime

    data.html_append('Game status:<br><table border="1"><tr>')
    data.html_append('<td>registered users</td>')
    data.html_append('<td>answers</td><td>still-in count</td>')
    data.html_append('<td width="10px">&nbsp;</td>')
    data.html_append('<td>sequence</td><td>phase</td><td>state</td>')
    data.html_append('<td>question</td><td>round</td>')
    data.html_append('<td>last update time</td>')
    data.html_append('</tr><tr>')
    data.html_append('<td align="center">%d</td>' % user_count)
    data.html_append('<td align="center">%d</td>' % answers)
    data.html_append('<td align="center">%d</td>' % still_in)
    data.html_append('<td align="center">&nbsp;</td>')
    data.html_append('<td align="center">%d</td>' % data.sequence)
    data.html_append('<td align="center">"%s"</td>' % data.phase)
    data.html_append('<td align="center">"%s"</td>' % data.state)
    data.html_append('<td align="center">%d of %d</td>' % (data.question_num, last_question))
    data.html_append('<td align="center">%d of %d</td>' % (data.round_num, last_round))
    data.html_append('<td align="center">%3.1f</td>' % (last_update_time))
    data.html_append('</tr></table>')

######################################################

# returns list of winner tuples (id, alias, name, email)
def get_winners(data):
    # scan still_in_dir, and find data for each winner
    file_list = os.listdir(still_in_dir)
    winners = []
    for still_in_user_id in file_list:
        user_filepath = user_dir + still_in_user_id
        try:
            fd = open(user_filepath, "r", encoding="utf-8")
            line = fd.readline().strip()
            user_id, alias, name, email, status, jlast_answer = \
                line.split(',', 5)
            winners.append((user_id, alias, name, email))
        except:
            data.add_error_message("Problem reading data from '%s'" % (user_filepath))

    winners.sort()
    return winners

######################################################

def save_winners(data):
    # write out file to next filename in sequence

    # increment sequence number
    data.winner_group += 1
    winner_filepath = data_dir + winner_file_fmt % data.winner_group

    winners = get_winners(data)
    try:
        fd = open(winner_filepath, "w", encoding="utf-8")
        for w in winners:
            line = "%s,%s,%s,%s\n" % w
            fd.write(line)
        fd.close()
    except:
        data.add_error_message("Problem writing winner file %s" % winner_filepath)


######################################################

def show_registration(data, user):
    if not user.logged_in:
        # show player registration form
        html_start(data, user)
        data.html_append("This is the registration page.\n<p>\n")
        show_register_form(data, "", "", "", "")
        data.is_form_page = True
    else:
        html_start(data, user, True)
        show_waiting_to_begin_page(data)

######################################################

def show_question_form(data):
    qnum = data.question_num

    try:
        question = tdata[qnum][0]
        green_text = tdata[qnum][1]
        red_text = tdata[qnum][2]
        both_text = tdata[qnum][3]
    except (KeyError, IndexError):
        question = "What is wrong with the game engine?"
        green_text = "Aliens have taken over the server"
        red_text = "Tim doesn't know what he's doing"
        both_text = ""
        data.add_error_message("Corrupt trivia data for question %d" % qnum)

    d = {}
    d["qnum"] = data.question_num
    d["image_url"] = data.image_url
    d["question"] = question % d

    data.html_append("""
<h1>Question # %(qnum)s</h1>


%(question)s
<p>
<HR>
""" % d)

    data.html_append("""
Please choose an answer:
<FORM method=post action="%s" name="question_form">
<input type="hidden" name="action" value="submit_answer">
<input type="hidden" name="qnum" value="%s">
<ul>
<table>
  <tr>
    <td><font color="green">Green</font> : </td>
    <td><INPUT type="radio" name="answer" value="green">%s</td>
  </tr><tr>
    <td><font color="red">Red</font> : </td>
    <td><INPUT type="radio" name="answer" value="red">%s</td>
""" % (data.url, data.question_num, green_text, red_text))

    if both_text:
        data.html_append("""
  </tr><tr>
    <td><font color="red">B</font><font color="green">o</font><font color="red">t</font><font color="green">h</font> : </td>
    <td><INPUT type="radio" name="answer" value="both">%s</td>
""" % both_text)

    # now finish the form
    data.html_append("""
  </tr><tr>
    <td><input type="submit" name="give_answer" value="Submit"></td>
    <td></td>
  </tr>
</table>
</ul>
<FORM>
<p>
""")

    if data.mode == SINGLE:
        seconds = 20
        timer_html = get_timer_html(data, seconds, "submit")
        data.html_append(timer_html + """
<div>You have <span id="time">%s</span> seconds to answer the question</div>
<p>
""" % seconds)

    data.is_form_page = True


######################################################

def show_qwaiting_page(data, answer):
    qnum = data.question_num
    try:
        question = tdata[qnum][0]
        green_text = tdata[qnum][1]
        red_text = tdata[qnum][2]
        both_text = tdata[qnum][3]
    except (KeyError, IndexError):
        question = "What is wrong with the game engine?"
        green_text = "Aliens have taken over the server"
        red_text = "Tim doesn't know what he's doing"
        both_text = ""
        data.add_error_message("Corrupt trivia data for question %d" % qnum)

    d = {}
    d["qnum"] = data.question_num
    d["image_url"] = data.image_url
    d["question"] = question % d

    d["green_text"] = green_text
    d["red_text"] = red_text
    d["both_text"] = both_text

    data.html_append("""
<h1>Question # %(qnum)s</h1>

%(question)s
<p>
<HR>
""" % d)

    d["green_indicator"] = ""
    d["red_indicator"] = ""
    d["both_indicator"] = ""
    d["you_chose"] = "You chose an answer:"

    if answer == "green":
        d["green_indicator"] = "<--- Your answer"
    elif answer == "red":
        d["red_indicator"] = "<--- Your answer"
    elif answer == "both":
        d["both_indicator"] = "<--- Your answer"
    elif answer == "no-answer":
        d["you_chose"] = ""
    else:
        data.add_error_message("Invalid answer '%s' provided" % answer)

    data.html_append("""
%(you_chose)s
<ul>
<table>
  <tr>
    <td><font color="green">Green</font> : </td>
    <td>%(green_text)s</td>
    <td>%(green_indicator)s</td>
  </tr><tr>
    <td><font color="red">Red</font> : </td>
    <td>%(red_text)s</td>
    <td>%(red_indicator)s</td>
""" % d)

    if both_text:
        data.html_append("""
  </tr><tr>
    <td><font color="red">B</font><font color="green">o</font><font color="red">t</font><font color="green">h</font> : </td>
    <td>%(both_text)s</td>
    <td>%(both_indicator)s</td>
""" % d)

    # finish the page
    data.html_append("""
  </tr>
</table>
</ul>
<p>
<hr>
<h1 align="center">Waiting for answer</h1>
<HR>\n<p>\n
""")

    if data.mode == SINGLE:
        seconds = 5
        timer_html = get_timer_html(data, seconds, "show_answer")
        data.html_append(timer_html + """
<div>Answer will show in in <span id="time">%s</span> seconds</div>
<p>
""" % seconds)

######################################################

def show_answer_page(data, answer):
    qnum = data.question_num
    try:
        question = tdata[qnum][0]
        green_text = tdata[qnum][1]
        red_text = tdata[qnum][2]
        both_text = tdata[qnum][3]
        answer_code = tdata[qnum][4]
        answer_text = tdata[qnum][5]
    except (KeyError, IndexError):
        question = "What is wrong with the game engine?"
        red_text = "Tim doesn't know what he's doing"
        green_text = "Aliens have taken over the server"
        both_text = ""
        answer_code = "red"
        answer_text = "obviously"
        data.add_error_message("Corrupt trivia data for question %d" % qnum)

    #data.add_error_message("answer=%s" % answer)

    d = {}
    d["qnum"] = data.question_num
    d["image_url"] = data.image_url
    d["question"] = question % d

    d["green_text"] = green_text
    d["red_text"] = red_text
    d["both_text"] = both_text

    data.html_append("""
<h1>Question # %(qnum)s</h1>

%(question)s
<p>
<HR>
""" % d)

    d["red_indicator"] = ""
    d["green_indicator"] = ""
    d["both_indicator"] = ""
    d["you_chose"] = "You chose an answer:"

    if answer == "green":
        d["green_indicator"] = "<--- Your answer"
    elif answer == "red":
        d["red_indicator"] = "<--- Your answer"
    elif answer == "both":
        d["both_indicator"] = "<--- Your answer"
    elif answer == "no-answer":
        d["you_chose"] = ""
    else:
        data.add_error_message("Invalid answer '%s' provided" % answer)

    d["green_right"] = ""
    d["red_right"] = ""
    d["both_right"] = ""

    answer_list = answer_code.split("|")
    found_right_answer = False
    if "green" in answer_list:
        d["green_right"] = "<--- The right answer"
        found_right_answer = True
    if "red" in answer_list:
        d["red_right"] = "<--- The right answer"
        found_right_answer = True
    if "both" in answer_list:
        d["both_right"] = "<--- The right answer"
        found_right_answer = True

    if not found_right_answer:
        data.add_error_message("Invalid answer_code '%s'!!" % answer_code)

    data.html_append("""
%(you_chose)s
<ul>
<table>
  <tr>
    <td><font color="green">Green</font> : </td>
    <td>%(green_text)s</td>
    <td>%(green_indicator)s</td>
    <td>%(green_right)s</td>
  </tr><tr>
    <td><font color="red">Red</font> : </td>
    <td>%(red_text)s</td>
    <td>%(red_indicator)s</td>
    <td>%(red_right)s</td>
""" % d)

    if both_text:
        data.html_append("""
  </tr><tr>
    <td><font color="red">B</font><font color="green">o</font><font color="red">t</font><font color="green">h</font> : </td>
    <td>%(both_text)s</td>
    <td>%(both_indicator)s</td>
    <td>%(both_right)s</td>
""" % d)
    # finish the page
    if data.is_observer:
        msg = ""
    else:
        if answer in answer_code.split("|"):
            msg = "<h2>You got it right!!</h2>"
        else:
            msg = "Sorry - you didn't get it right!!"

    data.html_append("""
  </tr>
</table>
</ul>
<p>\n<HR>\n<p>\n
%s
<p>\n<HR>\n<p>\n
%s
<HR>\n<p>\n
""" % (answer_text % d, msg))

    if data.mode == SINGLE:
        seconds = 20
        timer_html = get_timer_html(data, seconds, "next_question")
        data.html_append(timer_html + """
<div>Next question will show in in <span id="time">%s</span> seconds</div>
<p>
""" % seconds)

######################################################

def show_winners_page(data, user):
    winners = get_winners(data)

    data.html_append("""<h1>We have winners!!</h1>
Here is the list of winners:
<hr>
<ul>
""")

    is_winner = False
    for winner in winners:
        user_id = winner[0]
        alias = winner[1]
        if user_id == user.user_id:
            data.html_append("""<li><b>%s</b>&nbsp;&nbsp;
                <-- This is you!! - You are a winner!!""" % alias)
            is_winner = True
        else:
            data.html_append("<li>%s" % alias)
        data.html_append("</li>")

    data.html_append("</ul>\n<hr>\n<p>\n")


    if not data.admin_view:
        if not is_winner:
            data.html_append("Sorry - you did not win this time.\n<p>\n")

######################################################

def show_trivia(data, form, user):
    # if player:
    #    if state==question, show question and answer form (not refreshin)
    #       user can submit form, action=answer_question
    #    if state==waiting, show waiting_for_answer page (refreshing)
    #       put answer in user file
    #    if state==answer, show answer page (refreshing)
    #       on first answer page, update status:
    #          if answer!='recorded'
    #             get answer from file
    #             check answer against correct answer
    #             write status to user file
    #    if state==winners, show winners page (refreshing)
    # if admin:
    #    if state==question, show question (with user answer counts)
    #    if state==waiting, show question page (with user answer counts)
    #       admin can select "action=show_answer"
    #    if state==answer, show answer page
    #       admin can select "action=next_question"
    #       admin can select "action=declare_winners"
    #    if state==winners, show winners page (refreshing)
    #       admin can do: "action=reset_status"
    #       admin can do: "action=start_rps"
    #
    state = data.state
    if data.is_observer:
        answer = "no-answer"
    else:
        try:
            answer = form["answer"].value
        except LookupError:
            answer = user.last_answer

    if state == "question" and answer:
        state = "waiting"

    # data.add_notice("answer='%s'" % answer)
    # data.add_notice("state='%s'" % state)

    if not data.admin_view:
        if state == "question":
            if data.is_observer:
                html_start(data, user, True)
                show_qwaiting_page(data, "no-answer")
            else:
                html_start(data, user)
                show_question_form(data)
        elif state == "waiting":
            html_start(data, user, True)
            show_qwaiting_page(data, answer)
        elif state == "answer":
            html_start(data, user, True)
            show_answer_page(data, answer)
        elif state == "winners":
            html_start(data, user, True)
            show_winners_page(data, user)
        else:
            data.add_error_message("unknown trivia state: %s" % state)
            html_start(data, user)
            show_question_form(data)
    else:
        if state == "question" or state == "waiting":
            html_start(data, user, True)
            show_qwaiting_page(data, "no-answer")
        elif state == "answer":
            html_start(data, user)
            show_answer_page(data, "no-answer")
        elif state == "winners":
            html_start(data, user)
            show_winners_page(data, user)
        else:
            data.add_error_message("unknown trivia state: %s" % state)
            html_start(data, user)
            show_question_form(data)

######################################################

def show_rps_query_form(data):
    data.html_append("""
<h1>Round # %(round_num)d</h1>

<h1>Rock, Paper, Scissors</h1>
<p>
<HR>
Please choose an item to "throw":
<FORM method=post action="%(url)s">
<input type="hidden" name="action" value="submit_answer">
<input type="hidden" name="rnum" value="%(round_num)s">
<ul>
<table>
  <tr>
    <td><INPUT type="radio" name="answer" value="rock">Rock</td>
    <td><img src="%(image_url)s/rock.jpg" height="%(rps_image_size)d"></td>
  </tr><tr>
    <td><INPUT type="radio" name="answer" value="paper">Paper</td>
    <td><img src="%(image_url)s/paper.jpg" height="%(rps_image_size)d"></td>
  </tr><tr>
    <td><INPUT type="radio" name="answer" value="scissors">Scissors</td>
    <td><img src="%(image_url)s/scissors.jpg" height="%(rps_image_size)d"></td>
  </tr><tr>
    <td><input type="submit" name="submit" value="Submit"></td>
    <td></td>
  </tr>
</table>
</ul>
<FORM>
<p>
""" % data)
    data.is_form_page = True

######################################################

def show_rps_waiting_page(data, answer):
    data.html_append("""
<h1>Round # %d</h1>
<p>
<h1>Rock, Paper, Scissors</h1>
<HR>
""" % (data.round_num))

    d = {}
    d["rock_indicator"] = ""
    d["paper_indicator"] = ""
    d["scissors_indicator"] = ""
    d["you_chose"] = 'You chose to "throw":'

    if answer == "rock":
        d["rock_indicator"] = "<--- Your throw"
    elif answer == "paper":
        d["paper_indicator"] = "<--- Your throw"
    elif answer == "scissors":
        d["scissors_indicator"] = "<--- Your throw"
    elif answer == "no-answer":
        d["you_chose"] = ""
    else:
        data.add_error_message("Invalid guess '%s' provided" % answer)

    d["image_url"] = data.image_url
    d["rps_image_size"] = data.rps_image_size

    data.html_append("""
%(you_chose)s
<ul>
<table>
  <tr>
    <td>Rock : </td>
    <td><img src="%(image_url)s/rock.jpg" height="%(rps_image_size)d"></td>
    <td>%(rock_indicator)s</td>
  </tr><tr>
    <td>Paper : </td>
    <td><img src="%(image_url)s/paper.jpg" height="%(rps_image_size)d"></td>
    <td>%(paper_indicator)s</td>
  </tr><tr>
    <td>Scissors : </td>
    <td><img src="%(image_url)s/scissors.jpg" height="%(rps_image_size)d"></td>
    <td>%(scissors_indicator)s</td>
  </tr>
</table>
</ul>
<p>
""" % d)

    # finish the page
    data.html_append("""
<HR>
<h1 align="center">Waiting for answer</h1>
<HR>\n<p>\n
""")

######################################################

def show_result_page(data, answer):
    host_throw = rps_data[data.round_num]

    #data.add_error_message("host_throw=%s" % host_throw)

    data.html_append("""
<h1>Round # %d</h1>
<p>
<h1>Rock, Paper, Scissors</h1>
<HR>
""" % (data.round_num))

    d = {}

    d["rock_indicator"] = ""
    d["paper_indicator"] = ""
    d["scissors_indicator"] = ""
    d["you_chose"] = 'You chose to "throw":'

    if answer == "rock":
        d["rock_indicator"] = "<--- Your throw"
    elif answer == "paper":
        d["paper_indicator"] = "<--- Your throw"
    elif answer == "scissors":
        d["scissors_indicator"] = "<--- Your throw"
    elif answer == "no-answer":
        d["you_chose"] = ""
    else:
        data.add_error_message("Invalid guess '%s' provided" % answer)

    d["rock_host"] = ""
    d["paper_host"] = ""
    d["scissors_host"] = ""

    if host_throw == "rock":
        d["rock_host"] = "<--- The host threw"
    elif host_throw == "paper":
        d["paper_host"] = "<--- The host threw"
    elif host_throw == "scissors":
        d["scissors_host"] = "<--- The host threw"
    else:
        data.add_error_message("Invalid host throw '%s'!!" % host_throw)

    d["image_url"] = data.image_url
    d["rps_image_size"] = data.rps_image_size

    data.html_append("""
%(you_chose)s
<ul>
<table>
  <tr>
    <td>Rock : </td>
    <td><img src="%(image_url)s/rock.jpg" height="%(rps_image_size)d"></td>
    <td>%(rock_indicator)s</td>
    <td>%(rock_host)s</td>
  </tr><tr>
    <td>Paper : </td>
    <td><img src="%(image_url)s/paper.jpg" height="%(rps_image_size)d"></td>
    <td>%(paper_indicator)s</td>
    <td>%(paper_host)s</td>
  </tr><tr>
    <td>Scissors : </td>
    <td><img src="%(image_url)s/scissors.jpg" height="%(rps_image_size)d"></td>
    <td>%(scissors_indicator)s</td>
    <td>%(scissors_host)s</td>
  </tr>
</table>
</ul>
<p>
""" % d)

    # finish the page
    # this will have to be made generic for alternate items
    if data.is_observer:
        msg = ""
    else:
        msg = "Sorry - you lost to the host!!"
    if answer == "rock" and host_throw == "scissors":
        msg = "<h2>You beat the host!!</h2>"
    if answer == "scissors" and host_throw == "paper":
        msg = "<h2>You beat the host!!</h2>"
    if answer == "paper" and host_throw == "rock":
        msg = "<h2>You beat the host!!</h2>"

    # finish the page
    data.html_append("""
  </tr>
</table>
</ul>
<p><HR>\n<p>\n
%s
<p><HR>\n<p>\n
""" % msg)


######################################################

def show_rps(data, form, user):
    # if player:
    #    if state==query, show query and rps selection form (not refreshin)
    #       user can submit form, action=choose_rps
    #          action=choose_rps - puts rps selection in user file
    #    if state==waiting, show waiting_for_answer page (refreshing)
    #       show rps selection
    #    if state==response, show response page (refreshing)
    #       show rps selection
    #    if state==winners, show winners page (refreshing)
    # if admin:
    #    if state==query, show query (with user answer counts)
    #    if state==waiting, show question page (with user answer counts)
    #       admin can select "action=show_host_rps"
    #    if state==response, show response page
    #       admin can select "action=next_round"
    #       admin can select "action=declare_winners"
    #    if state==winners, show rps_winners page (refreshing)
    #       admin can do: "action=done"
    #
    state = data.state
    if data.is_observer:
        answer = "no-answer"
    else:
        try:
            answer = form["answer"].value
        except:
            answer = user.last_answer

    if data.admin_view:
        answer = "no-answer"

    if state == "query" and answer:
        state = "waiting"

    #data.add_error_message("state='%s'" % state)

    if not data.admin_view:
        if state == "query":
            if data.is_observer:
                html_start(data, user, True)
                show_rps_waiting_page(data, answer)
            else:
                html_start(data, user)
                show_rps_query_form(data)
        elif state == "waiting":
            html_start(data, user, True)
            show_rps_waiting_page(data, answer)
        elif state == "result":
            html_start(data, user, True)
            show_result_page(data, answer)
        elif state == "winners":
            html_start(data, user, True)
            show_winners_page(data, user)
        else:
            data.add_error_message("unknown rps state: %s" % state)
            html_start(data, user)
            show_rps_query_form(data)
    else:
        if state == "query" or state == "waiting":
            html_start(data, user, True)
            show_rps_waiting_page(data, answer)
        elif state == "result":
            html_start(data, user)
            show_result_page(data, answer)
        elif state == "winners":
            html_start(data, user)
            show_winners_page(data, user)
        else:
            data.add_error_message("unknown rps state: %s" % state)
            html_start(data, user)
            show_rps_query_form(data)

######################################################

def show_page(data, form, user):
    phase = data.phase

    if phase == "registration" or not user.logged_in:
        show_registration(data, user)
        return

    if phase == "trivia":
        show_trivia(data, form, user)
        return

    if phase == "rps":
        show_rps(data, form, user)
        return

    # we must be done
    html_start(data, user)
    data.html_append("""<h1>Game Over</h1>
Thank you for playing the Embedded Linux Conference
closing game.
<p>
I hope you had a good time!!
<p>
    """)
    data.is_form_page = True

######################################################

def html_start(data, user, refresh=False):
    # for CGI, output the HTTP headers ourself, at the start of HTML
    # WSGI will output them separately in the application() function
    if not data.is_wsgi:
        html = ""
        if not data.header_shown:
            html += "Content-type: text/html\n"
            if data.cookie:
                html += data.cookie
            html += '\n\n'
            data.header_shown = True
        data.html_append(html)

    data.should_refresh = False
    if refresh and not data.suppress_refresh:
        refresh_str = '<meta http-equiv="refresh" content="%d; url=%s"/>' % \
            (data.refresh_count, data.url)
        data.should_refresh = True
    else:
        refresh_str = ''

    data.html_append("""
<HTML>
<HEAD>
<TITLE>ELC Closing Game</TITLE>
%s
</HEAD>
<BODY BGCOLOR="LightBlue">
<table border="1" bgcolor="DDDDDD"><tr>
""" % (refresh_str))

    # FIXTHIS - do this later, to get rid of user parameter above
    #user = data.user

    if user and user.logged_in:
        data.html_append("<td>&nbsp;Logged in as: <b>%s</b>&nbsp;</td>\n" % user.alias)
    else:
        data.html_append("<td>&nbsp;Not logged in.&nbsp;</td>\n")

    if user and data.phase != "registration":
        data.html_append('<td width="10px">###</td><td>&nbsp;')

        if user.status == STILL_IN:
            data.html_append("Status: <b>Still In!!</b> </td>\n")
        else:
            data.html_append("Status: <b>Eliminated for now</b> </td> \n")
    data.html_append("</td></tr></table>")

    # data.add_notice("browser cookie='%s'" % data.cookie)
    data.html_append("<br><hr><p>\n")

    data.html_append(data.get_notices_as_html())
    data.html_append(data.get_errors_as_html())

    # could show a footer here

######################################################

# admin view has some extra tables for managing the game
# line 1 = administration: (sequence) main, undo, edit_game_data, reset
# line 2 = trivia controls: start trivia, show_answer, next_question, declare_winners
# line 3 = rps controls: start rps, show_answer, next_rps, declare_winners

def show_admin_controls(data):
    d = {"url": data.url}
    d["sequence"] = data.sequence
    if default_suppress_refresh:
        d["refresh"] = "(currently off)"
    else:
        d["refresh"] = "(currently on)"

    # show admin controls
    data.html_append("""<p>Game controls:<br>
<table width="100%%" border=1><tr>
<td><a href="%(url)s">main</a></td>
<td><a href="%(url)s?action=undo">undo</a></td>
<td><a href="%(url)s?action=edit_game">edit game</a></td>
<td><a href="%(url)s?action=restore_still_ins">restore_still_ins</a></td>
<td><a href="%(url)s?action=toggle_refresh">toggle_refresh</a> %(refresh)s</td>
<td><a href="%(url)s?action=reset">reset</a></td>
</tr>""" % d)

    ### show trivia controls
    # make some controls conditional
    d["question_num"] = str(data.question_num)

    # default to no link for some controls
    d["start_trivia"] = "start_trivia"
    d["show_answer"] = "show_answer"
    d["next_question"] = 'next question'
    d["declare_winners"] = '<a href="%(url)s?action=declare_winners">declare_winners</a>' % d

    if data.phase == "registration":
        d["start_trivia"] = '<a href="%(url)s?action=start_trivia">start_trivia</a>' % d

    if data.phase == "trivia":
        if data.state == "question" or data.state == "waiting":
            d["show_answer"] = '<a href="%(url)s?action=show_answer">show_answer</a>' % d
        if data.state == "answer" or data.state == "winners":
            d["next_question"] = '<a href="%(url)s?action=next_question">next_question</a>' % d

    last_question = max([int(k) for k in list(tdata.keys())])
    if data.question_num >= last_question:
        # disable 'next question' link on admin page for last question
        d["next_question"] = "next_question (disabled)"

    if data.state == "winners":
        d["declare_winners"] = "declare_winners"

    data.html_append("""
<tr>
<td>%(start_trivia)s</td>
<td>question #%(question_num)s</td>
<td>%(show_answer)s</td>
<td>%(next_question)s</td>
<td>%(declare_winners)s</a></td>
</tr>""" % d)

    # show rps controls
    d["round_num"] = str(data.round_num)

    d["start_rps"] = 'start_rps'
    d["show_result"] = 'show_result'
    d["next_round"] = 'next_round'

    if data.phase == "trivia":
        d["start_rps"] = '<a href="%(url)s?action=start_rps">start_rps</a>' % d

    if data.phase == "rps":
        if data.state == "query" or data.state == "waiting":
            d["show_result"] = '<a href="%(url)s?action=show_result">show_result</a>' % d
        if data.state == "result" or data.state == "winners":
            d["next_round"] = '<a href="%(url)s?action=next_round">next_round</a>' % d


    last_round = max([int(k) for k in list(rps_data.keys())])
    if data.round_num >= last_round:
        # disable 'next round' link on admin page for last question
        d["next_round"] = "next_round (disabled)"

    if data.phase == "rps":
        d["done"] = '<a href="%(url)s?action=done">done</a>' % d
    else:
        d["done"] = 'done'

    d["sequence"] = str(data.sequence)

    data.html_append("""
<tr>
<td>%(start_rps)s</a></td>
<td>round #%(round_num)s</td>
<td>%(show_result)s</a></td>
<td>%(next_round)s</td>
<td>%(declare_winners)s</a></td>
</tr><tr>
<td>%(done)s</a></td>
<td>%(sequence)s</a></td>
</tr></table>""" % d)


def html_end(data):
    if data.admin_view:
        show_status_counts(data)
        show_admin_controls(data)

    if data.should_refresh:
        data.html_append("""
Page should refresh automatically.
<p>
If it doesn't, click <a href="%s">this link</a> to
proceed when instructed by the game host.
<HR>\n<p>\n
""" % data.url)
    else:
        if not data.is_form_page:
            data.html_append("""
Click <a href="%s">this link</a> to proceed when
instructed by the game host.<br>
<HR>\n<p>\n""" % data.url)

    data.html_append(data.get_notices_as_html())
    data.html_append(data.get_errors_as_html())

    # use this for debugging
    if show_data and data.admin_view:
        data.html_append("Debug:: data=%s\n<p>\n" % data.debug_data())

    if user_show_data and not data.admin_view:
        data.html_append("Debug:: data=%s\n<p>\n" % data.debug_data())

    data.html_append("</BODY></HTML>")
    #data.emit_html()

######################################################

# returns a 'user' instance
def create_user(user_id, alias, name, email):
    # write user file
    user = user_class(user_id, alias, name, email)
    user.write_file()
    return user

######################################################

# returns a 'user' instance, or a special "nobody" user if not found
def read_user(data, user_id):
    # read user file
    user_filepath = user_dir + user_id
    try:
        fd = open(user_filepath, "r", encoding="utf-8")
        line = fd.readline().strip()
        fd.close()
    except:
        return user_class(NOBODY_USER_ID, "not-logged-in", "", "")

    user_id, alias, name, email, status, last_answer = line.split(',', 5)
    user = user_class(user_id, alias, name, email, status)

    # FIXTHIS - this overrides the last_answer in the user file
    # should probably eliminate last_answer from user file
    answer_dir = get_current_answer_dir(data)
    if answer_dir:
        last_answer = ""
        answer_filepath = answer_dir + user_id
        if os.path.exists(answer_filepath):
            try:
                fd = open(answer_filepath, encoding="utf-8")
                last_answer = fd.read()
                fd.close()
            except:
                data.add_error_message("Problem reading answer file %s in read_user()" % answer_filepath)

    user.last_answer = last_answer
    return user

######################################################

def clear_user_answers(data):
    file_list = os.listdir(user_dir)
    for user_id_filename in file_list:
        user_filepath = user_dir + user_id_filename
        try:
            fd = open(user_filepath, "r+", encoding="utf-8")
            line = fd.readline().strip()
            user_id, alias, name, email, status, jlast_answer = \
                line.split(',', 5)
            fd.seek(0, os.SEEK_SET)
            line = "%s,%s,%s,%s,%s,\n" % \
                (user_id, alias, name, email, status)
            fd.write(line)
            fd.truncate()
            fd.close()
        except:
            data.add_error_message("Problem clearing answer from '%s'" % \
                (user_filepath))

######################################################

def clear_current_answers(data):
    # remove answers for current question or round
    answer_dir = get_current_answer_dir(data)
    if os.path.isdir(answer_dir):
        file_list = os.listdir(answer_dir)
        for filename in file_list:
            os.remove(answer_dir + filename)
    else:
        os.mkdir(answer_dir)

######################################################

def save_still_ins():
    # erase files in still_in_backup dir, and
    # copy contents of still_in_dir into it
    file_list = os.listdir(still_in_backup)
    for f in file_list:
        os.remove(still_in_backup + f)

    file_list = os.listdir(still_in_dir)
    for f in file_list:
        fd = open(still_in_backup + f, "w", encoding="utf-8")
        fd.write(STILL_IN)
        fd.close()

######################################################

def restore_still_ins(data):
    # erase files in still_in_dir, and
    # copy contents of still_in_backup dir into it
    file_list = os.listdir(still_in_dir)
    for f in file_list:
        os.remove(still_in_dir + f)

    file_list = os.listdir(still_in_backup)
    for f in file_list:
        fd = open(still_in_dir + f, "w", encoding="utf-8")
        fd.write(STILL_IN)
        fd.close()

        user_filepath = user_dir + f
        try:
            fd = open(user_filepath, "r+", encoding="utf-8")
            line = fd.readline().strip()
            user_id, alias, name, email, status, last_answer = \
                line.split(',', 5)
            status = STILL_IN
            fd.seek(0, os.SEEK_SET)
            line = "%s,%s,%s,%s,%s,\n" % \
                (user_id, alias, name, email, status)
            fd.write(line)
            fd.truncate()
            fd.close()
        except:
            data.add_error_message("Problem restoring still-in status in file: %s" % \
                (user_filepath))

######################################################

def make_all_users_still_in(data):
    # change user status back to STILL_IN for all users (old method)
    file_list = os.listdir(user_dir)
    for user_id_filename in file_list:
        user_filepath = user_dir + user_id_filename
        try:
            fd = open(user_filepath, "r+", encoding="utf-8")
            line = fd.readline().strip()
            user_id, alias, name, email, status, last_answer = \
                line.split(',', 5)
            status = STILL_IN
            fd.seek(0, os.SEEK_SET)
            line = "%s,%s,%s,%s,%s,\n" % \
                (user_id, alias, name, email, status)
            fd.write(line)
            fd.truncate()
            fd.close()
        except:
            data.add_error_message("Problem resetting status in file: %s" % \
                (user_filepath))

        # add still-in file to still_in directory (new method)
        try:
            fd = open(still_in_dir + user_id_filename, "w", encoding="utf-8")
            fd.write(status)
            fd.close()
        except:
            data.add_error_message("Problem setting status in file: %s" % \
                (still_in_dir + user_id_filename))

######################################################

def is_correct(data, phase, correct_answer, answer):
    if phase == "trivia":
        return answer in correct_answer.split("|")

    if phase == "rps":
        host_throw = correct_answer
        if answer == "rock" and host_throw == "scissors":
            return True
        if answer == "scissors" and host_throw == "paper":
            return True
        if answer == "paper" and host_throw == "rock":
            return True
        return False

    data.add_error_message("Invalid phase '%s' detected in is_correct()" % phase)
    return False

def update_user_status(data, correct_answer):
    #data.add_error_message("correct_answer=%s" % correct_answer)
    phase = data.phase

    file_list = os.listdir(user_dir)
    # FIXTHIS - potentially expensive loop here (but only for admin)
    for user_id_filename in file_list:
        user_filepath = user_dir + user_id_filename
        try:
            fd = open(user_filepath, "r+", encoding="utf-8")
            line = fd.readline().strip()
            user_id, alias, name, email, status, last_answer = \
                line.split(',', 5)
            if status == STILL_IN:
                if not is_correct(data, phase, correct_answer, last_answer):
                    status = OUT
                    fd.seek(0, os.SEEK_SET)
                    line = "%s,%s,%s,%s,%s,%s\n" % \
                        (user_id, alias, name, email, status, last_answer)
                    fd.write(line)
                    fd.truncate()
            fd.close()
        except:
            data.add_error_message("Problem clearing answer from '%s'" % \
                (user_filepath))

        # remove still_in status if we're eliminated
        in_filepath = still_in_dir + user_id_filename
        if status != STILL_IN and os.path.exists(in_filepath):
            os.remove(in_filepath)

######################################################

def show_register_form(data, user_id, alias, name, email):
    # FIXTHIS - add form to fill in already-entered data, if available
    data.html_append("""
<FORM method=post action="%s">
<input type="hidden" name="action" value="register_user">
<table>
  <tr>
    <td>Event Confirmation Number:</td>
    <td align="right"><INPUT type=text name="user_id" value="%s"></td>
  </tr><tr>
    <td>Account Name (alias):</td>
    <td align="right"><INPUT type=text name="alias" value="%s"></td>
  </tr><tr>
    <td>Real Name:</td>
    <td align="right"><INPUT type=text name="name" value="%s"></td>
  </tr><tr>
    <td>E-mail:</td>
    <td align="right"><INPUT type=text name="email" value="%s"></td>
  </tr><tr>
    <td><input type="Submit" name="submit" value="Cancel"></td>
    <td><input type="Submit" name="submit" value="Submit"></td>
  </tr>
</table>
</FORM>
<p>
<ul>
  <i><b>Note:</b><br>
  The Event Confirmation Number is available in your registration confirmation
  email for the event.  Please check that email to find the number.
  </i>
  <p>
  The 'Real Name' and 'E-mail' will not be displayed or shared with
  anyone.<br>
  They will only be used to contact you in the event you win a prize.<br>
  <p>
  Your account name (alias) may be displayed during the game if you are among
  a small number of contestants still in the running for a prize, for a particular
  trivia round. Since other users may see this, please keep your account
  name inoffensive.  Thanks :-)
</ul>
""" % (data.url, user_id, alias, name, email))

######################################################

def do_register_user(data, form):
    # check data while collecting it from form
    error_count = 0
    try:
        user_id = form["user_id"].value
    except:
        data.add_error_message("Missing form value for 'Event Confirmation Number'")
        user_id = ""
        error_count += 1

    # validate user_id
    try:
        from valid_user_ids import valid_user_ids
    except:
        data.add_error_message("Can't read valid user ids from rgdata/valid_user_ids.py")
        error_count += 1

    if user_id not in valid_user_ids:
        data.add_error_message("""Invalid Event Confirmation Number '%s'
specified.  Please use correct Event Confirmation Number.""" % user_id)
        error_count += 1

    try:
        alias = form["alias"].value
    except:
        data.add_error_message("Missing form value for action 'Alias'")
        alias = ""
        error_count += 1

    try:
        name = form["name"].value
    except:
        data.add_error_message("Missing form value for action 'Real Name'")
        name = ""
        error_count += 1

    try:
        email = form["email"].value
    except:
        data.add_error_message("Missing form value for action 'E-mail'")
        email = ""
        error_count += 1

    # See if confirmation number is already in use
    # check for blank data
    if not user_id:
        data.add_error_message("Missing Event Confirmation Number")
        error_count += 1

    if not alias:
        data.add_error_message("Missing Account Name" )
        error_count += 1

    if not name:
        data.add_error_message("Missing Real Name")
        error_count += 1

    if not email:
        data.add_error_message("Missing E-mail")
        error_count += 1

    if error_count:
        html_start(data, None)
        show_register_form(data, user_id, alias, name, email)
        return

    if user_id == ADMIN_USER_ID and name == ADMIN_NAME:
        user = create_user(user_id, "admin", name, "tim.bird@sony.com")
        user.logged_in = True
    else:
        # save data to user database
        user = create_user(user_id, alias, name, email)
        user.logged_in = True

    data.user = user

    if data.phase == "registration":
        # start user as still-in the game
        fd = open(still_in_dir + user_id, "w", encoding="utf-8")
        fd.write(STILL_IN)
        fd.close()
    else:
        # otherwise, start user out of the game
        # this prevents users from leaving the game and rejoining, in order
        # to change their status
        user.status = OUT
        user.write_file()


    # set cookie expiration for 10 days (in seconds)
    data.cookie = "Set-Cookie: user_id=%s; Max-Age=864000;" % user_id

    # show - Success, waiting for game to start page
    html_start(data, user, True)
    data.html_append("Successfuly registered user: %s\n<p>\n" % alias)
    show_waiting_to_begin_page(data)
    return

######################################################

def get_timer_html(data, seconds, action):
    if action == "submit":
        action_str = 'document.question_form.submit()'
    else:
        action_str = 'window.location.href="%s?action=%s"' % (data.url, action)

    return """
<script>
function start_timer(duration, display) {
    var timer = duration, seconds;
    setInterval(function () {
        seconds = parseInt(timer);
        display.textContent = seconds;
        if (--timer < 0 ) {
            %s;
        }
      }, 1000);
}

window.onload = function () {
    var seconds = %s;
    display = document.querySelector('#time');
    start_timer(seconds, display);
};
</script>

""" % (action_str, seconds)

######################################################

def show_waiting_to_begin_page(data):
    data.html_append("""
<h1 align="center">Waiting for game to begin...</h1>
<HR>\n<p>\n
""")

    if data.mode == SINGLE:
        seconds = 20
        timer_html = get_timer_html(data, seconds, "start_trivia")
        data.html_append(timer_html + """
<div>Game begins in <span id="time">%s</span> seconds</div>
<p>
""" % seconds)
    else:
        # FIXTHIS - only show if data.admin_view:  ??
        user_count = get_registered_user_count()
        data.html_append("Number of registered players=%d\n<p>" % user_count)

######################################################

# return True if response was handled completely
def do_action(action, data, form, user):
    phase = data.phase

    #data.html_append("action=<b>%s</b><br>" % action)
    done = False
    if action == "none":
        pass

    elif action == "register_user":
        do_register_user(data, form)
        done = True

    elif action == "logout":
        data.cookie = \
            "Set-Cookie: user_id=;expires=Thu, 01 Jan 1970 00:00:01 GMT"
        html_start(data, None)
        data.html_append("<h1>User logged out</h1>")
        data.html_append('Click <a href="%s">here</a> to reload page' % data.url)
        done = True

    elif action == "start_trivia":
        data.phase = "trivia"
        data.question_num = 1
        data.state = "question"
        write_game_data(data)
        clear_user_answers(data)
        make_all_users_still_in(data)
        save_still_ins()

    elif action == "submit_answer":
        try:
            answer = form["answer"].value
        except KeyError:
            data.add_error_message("Form was missing answer")
            answer = ""

        if answer:
            user.save_answer(data, form, answer)

    elif phase == "trivia" and action == "show_answer":
        data.state = "answer"
        write_game_data(data)
        qnum = data.question_num
        answer_code = tdata[qnum][4]
        update_user_status(data, answer_code)

    elif phase == "trivia" and action == "next_question":
        last_state = data.state
        if data.question_num < len(tdata):
            data.question_num += 1
        else:
            data.add_error_message("""Cannot move to next question.
                question_num is already %d""" % data.question_num)
        data.state = "question"
        write_game_data(data)
        clear_user_answers(data)
        clear_current_answers(data)
        save_still_ins()

        # after declaring winners, let everyone back into the game
        if last_state == "winners":
            make_all_users_still_in(data)

    elif action == "declare_winners":
        data.state = "winners"
        save_winners(data)
        # write game data AFTER saving winners
        write_game_data(data)

    elif action == "start_rps":
        #do_start_rps(data, form, user)
        data.phase = "rps"
        data.state = "query"
        data.round = "1"
        write_game_data(data)
        clear_user_answers(data)
        # FIXTHIS - could allow still-ins to flow from trivia to rps game
        # just in case trivia didn't knock enough out
        # just need to remove 'make_all_users_still_in()'???
        # NOTE: declare winners can do the make_all_users_still_in() call in
        # case that was the last thing done before start_rps.
        make_all_users_still_in(data)
        save_still_ins()

    elif phase == "rps" and action == "show_result":
        data.state = "result"
        write_game_data(data)
        host_throw = rps_data[data.round_num]
        update_user_status(data, host_throw)

    elif phase == "rps" and action == "next_round":
        last_state = data.state
        if data.round_num < len(rps_data):
            data.round_num += 1
        else:
            data.add_error_message("""Cannot move to next round.
                round_num is already %d""" % data.round_num)

        data.state = "query"
        write_game_data(data)
        clear_user_answers(data)
        clear_current_answers(data)
        save_still_ins()

        # after declaring winners, let everyone back into the game
        if last_state == "winners":
            make_all_users_still_in(data)

    elif action == "done":
        data.phase = "done"
        write_game_data(data)

    elif action == "reset":
        data.suppress_refresh = True
        html_start(data, user)
        data.html_append("""<h1>### RESET ###</h1>
Are you sure you want to reset the game?<br>
If so, click on the link below to really reset the game:<br>
<a href="%s?action=really_reset">Really Reset!!</a>&nbsp;&nbsp;&nbsp;
<a href="%s">cancel (don't reset)</a>
""" % (data.url, data.url))

    elif action == "really_reset":
        # save initial variables...
        reset_data = copy.deepcopy(stub_data)

        # remove all undo sequence files
        remove_undo_data_files()
        write_game_data(reset_data)

        reset_answers_and_users(data)

        data.set_data(reset_data)
        data.suppress_refresh = True
        data.add_notice("Click 'main' to continue")

    elif action == "restore_still_ins":
        data.suppress_refresh = True
        html_start(data, user)
        data.html_append("""<h1>### RESTORE STILL INS ###</h1>
Are you sure you want to restore the still_ins from backup?<br>
If so, click on the link below to really reset the game:<br>
<a href="%s?action=really_restore_still_ins">Really Restore still_ins!!</a>&nbsp;&nbsp;&nbsp;
<a href="%s">cancel (don't restore)</a>
""" % (data.url, data.url))

    elif action == "really_restore_still_ins":
        restore_still_ins(data)

    elif action == "edit_game":
        # show a form to set values directly
        # bank, score_a, score_b, round, strike_1,2,3
        html_start(data, user)
        data.html_append("""Please edit the game data:
<FORM method=post action="%s">
<INPUT type=hidden name="action" value="set_values">
<table border=0>
""" % data.url)
        keys = list(data.keys())
        keys.sort()
        for name in keys:
            if not name in data.game_attr_list:
                continue

            value = getattr(data, name)
            data.html_append("""
<tr>
<TD BGCOLOR="#dddddd" WIDTH="55%%">
%s</td>
<TD WIDTH="33%%"><INPUT type="Text" name="%s" size="50" value="%s">
</TD>
</tr>""" % (name, name, value))

        data.html_append("""
</table>
<ul>
<input type="Submit" name="submit" value="Submit">
</ul>""")
        done = True

    elif action == "set_values":
        # set values from the form
        log_this("in set_values")
        html_start(data, user)
        data.html_append("Set values for game from form data!!")

        for name in data.keys():
            if name in data.game_attr_list:
                value = form[name].value
                if name in data.game_attr_ints:
                    log_this("settting %s=int(%s)" % (name, value))
                    try:
                        data.__dict__[name] = int(value)
                    except ValueError:
                        msg = "Invalid value '%s' for game data '%s' - expected integer" % (value, name)
                        log_this(msg)
                        data.add_error_message(msg)
                else:
                    log_this("settting %s=%s" % (name, value))
                    data.__dict__[name] = (value)

        #log_this("data.__dict__=%s" % data.__dict__)
        write_game_data(data)
        done = True

    elif action == "undo":
        data.suppress_refresh = True
        html_start(data, user)
        data.html_append("""<h1>### UNDO ###</h1>
Are you sure you want to undo a step in the game?<br>
If so, click on the link below to really undo 1 game step:<br>
<a href="%s?action=really_undo">Really undo!!</a>&nbsp;&nbsp;&nbsp;
<a href="%s">cancel (don't undo anything)</a>
""" % (data.url, data.url))

    elif action == "really_undo":
        # back up one data file
        game_filename = data.game_filename
        os.unlink(game_filename)
        new_data = read_game_data_from_last_file(data)

        # replace items in data with items in new_data
        data.set_data(new_data)
        data.suppresh_refresh = True

    elif action == "toggle_refresh":
        global default_suppress_refresh

        if os.path.exists(rfile):
            os.remove(rfile)
            default_suppress_refresh = False
            data.add_notice("removed %s and set 'default_suppress_refresh' to False" % rfile)
        else:
            fd = open(rfile, "w", encoding="utf-8")
            fd.write("suppress")
            fd.close()
            default_suppress_refresh = True
            data.add_notice("created %s and set 'default_suppress_refresh' to True" % rfile)

    else:
        data.add_error_message("""Unknown action: '%s'
            (or illegal action for this phase)""" % action)

    return done

    # end of do_action()

######################################################

def dict_to_html(d):
    keys = list(d.keys())
    keys.sort()
    html = b""
    for key in keys:
        html += b"<b>%s</b>=%s<br>" % (key, d[key])
    return html

######################################################

def get_user_id(environ, data, form):
    user_id = None
    try:
        cookie = environ["HTTP_COOKIE"]
    except KeyError:
        cookie = ""

    # data.add_notice("in get_user_id(): environ=%s" % dict_to_html(environ))
    # data.add_notice("in get_user_id(): cookie=%s" % cookie)
    if "user_id=" in cookie:
        (jfirst, value) = cookie.split("user_id=", 1)
        if value.find(";") != -1:
            (value, jrest) = value.split(";", 1)
        user_id = value

    if not user_id:
        try:
            value = form["user_id"].value
            if value == ADMIN_USER_ID:
                user_id = ADMIN_USER_ID
        except:
            pass

    # set cookie for response header
    # Cookie should only need to be set once
    if user_id:
        data.cookie = "Set-Cookie: user_id=%s; Max-Age=864000;" % user_id

    if user_id == ADMIN_USER_ID:
        data.admin_view = True

    if user_id == OBSERVER_USER_ID:
        data.is_observer = True

    return user_id

######################################################

def handle_request(environ, data, form):
    user_id = get_user_id(environ, data, form)
    #log_this("in handle_request: user_id=%s" % user_id)
    # data.add_notice("user_id from form = '%s'" % str(user_id))
    user = user_class(NOBODY_USER_ID, "not-logged-in", "", "")
    if user_id == ADMIN_USER_ID:
        user = user_class(ADMIN_USER_ID, "admin", ADMIN_NAME, "tim.bird@sony.com")
        user.logged_in = True
    else:
        if user_id:
            if os.path.exists(user_dir + user_id):
                user = read_user(data, user_id)
                user.logged_in = True
            else:
                data.add_error_message("Invalid user_id '%s' specified in cookie" % user_id)

    # data.add_notice("user.logged_in = '%s'" % str(user.logged_in))
    done = False
    if "action" in form:
        action = form["action"].value
        done = do_action(action, data, form, user)

        # do_action doesn't return if it handled the action completely

    if not done:
        show_page(data, form, user)

    html_end(data)


def main():
    form = cgi.FieldStorage()

    # we have a chicken-and-egg problem here
    pre_data = data_class()
    data = read_game_data_from_last_file(pre_data)
    data.html = pre_data.html
    data.err_msg_list = pre_data.err_msg_list
    data.url = CGI_URL

    try:
        handle_request(os.environ, data, form)
        data.emit_html()
    except:
        import traceback
        tb = traceback.format_exc()
        log_this(tb)

def application(environ, start_response):
    form = cgi.FieldStorage(
            fp = environ['wsgi.input'],
            environ = environ,
            keep_blank_values = True
            )

    # we have a chicken-and-egg problem here
    pre_data = data_class()
    data = read_game_data_from_last_file(pre_data)
    data.html = pre_data.html
    data.err_msg_list = pre_data.err_msg_list
    data.is_wsgi = True
    data.url = WSGI_URL

    try:
        handle_request(environ, data, form)
    except:
        import traceback
        tb = traceback.format_exc()
        log_this(tb)

    # convert data.cookie to WSGI resp_headers format (ie a tuple)
    if data.cookie:
        set_cookie, cookie = data.cookie.split(":", 1)
        data.resp_headers.append((set_cookie, cookie))

    start_response(data.resp_status, data.resp_headers)
    return data.html

if __name__ == "__main__":
    main()
