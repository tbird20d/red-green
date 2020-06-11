#!/usr/bin/env python

# Copyright 2020 by Tim Bird
# j in front of variable means "junk_" - something that is discarded
# and not used in the function

import sys
import os
import cgi
import re
import cgitb

cgitb.enable()

# turn this on to show the game data in the admin view
# (for debugging)
show_data = True
user_show_data = True

data_dir = "/home/tbird/work/games/red-green/rgdata/"

# import the trivia data
if data_dir not in sys.path:
    sys.path.append(data_dir)

from trivia import tdata
from rps import rps_data

game_file_pattern = "rgdata-([0-9][0-9][0-9]).txt"
game_file_fmt = "rgdata-%03d.txt"

user_file_pattern = "rg-user-.*[.]txt"
user_file_fmt = "rg-user-%s.txt"
url = "rg.cgi"

winner_file_fmt = "winners-%02d.txt"

REFRESH_SECONDS = 4

# To login as administrator, use the url:
# http://localhost:8000/rg.cgi?user_id=admin-game-admin
#  or enter: admin-game-admin, Real Name=Tim in the registration form
ADMIN_USER_ID = "admin-game-admin"
ADMIN_NAME = "Tim"

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

#
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
        self.notice_list = []
        self.suppress_refresh = False
        self.header_shown = False
        self.cookie = ""

        # here is the game data
        self.game_attr_list = ['sequence', 'winner_group', 'phase',
                               'state', 'question_num', 'round_num']
        self.game_attr_ints = ['sequence', 'winner_group',
                               'question_num', 'round_num']
        self.sequence = 0
        self.winner_group = 1
        self.phase = "registration"  # registration, trivia, rps, done
        self.state = "question"  # question, wiating, answer, winners
           # or, for rps: query, waiting, result, winners
        self.question_num = 1
        self.round_num = 1

    def set_data(self, new_data):
        for key in new_data.__dict__.keys():
            if key in self.game_attr_list:
                self.__dict__[key] = new_data.__dict__[key]

    def __getitem__(self, key):
        if self.data.has_key(key):
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
        return self.data.has_key(key)

    def keys(self):
        # FIXTHIS - are the __dict__ keys needed?
        keys = self.__dict__.keys()
        keys.append(self.data.keys())
        return keys

######################################################

    def html_append(self, html):
        self.html.append(html)

    def emit_html(self):
        for hline in self.html:
            print(hline)
        self.html = []

    def add_error_message(self, msg):
        self.err_msg_list.append('<font color="red">ERROR: %s<br></font>' % msg)

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

class user_class(object):
    def __init__(self, user_id, alias, name, email, status="still-in"):
        self.user_id = user_id
        self.alias = alias
        self.name = name
        self.email = email
        # status can be 'still-in' or 'out'
        self.status = status
        self.last_answer = ""
        self.logged_in = False

    def write_file(self):
        line = "%s,%s,%s,%s,%s,%s\n" % (self.user_id, self.alias, self.name,
                                        self.email, self.status,
                                        self.last_answer)
        user_filepath = data_dir + (user_file_fmt % self.user_id)
        fd = open(user_filepath, "w")
        fd.write(line)
        fd.close()

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
        return stub_data

    last_game_filename = data_dir + max_filename
    return read_game_data(data, last_game_filename)

######################################################

# FIXTHIS - may need to save off err_msg_list and html, in case
# they already have data
def read_game_data(data, game_filename):
    try:
        game_lines = open(game_filename, "r").readlines()
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
    return data

######################################################

def write_game_data(data):
    # write out file to next filename in sequence

    # increment sequence number
    data.sequence += 1
    game_filename = data_dir + game_file_fmt % data.sequence
    data.game_filename = game_filename

    fd = open(game_filename, "w")
    klist = data.keys()
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

######################################################

def get_registered_user_count():
    file_list = os.listdir(data_dir)
    count = 0
    for filename in file_list:
        m = re.match(user_file_pattern, filename)
        if m:
            count += 1
    return count

######################################################

# returns (user_count, still_in_count, answer_count)
def get_status_counts(data):
    file_list = os.listdir(data_dir)
    user_count = 0
    still_in_count = 0
    answer_count = 0
    for filename in file_list:
        m = re.match(user_file_pattern, filename)
        if m:
            user_count += 1
            try:
                fd = open(data_dir + filename, "r")
                line = fd.readline().strip()
                juser_id, jalias, jname, jemail, status, last_answer = \
                        line.split(',', 5)
                if status == "still-in":
                    still_in_count += 1
                if last_answer.strip():
                    answer_count += 1
            except:
                data.add_error_message("Problem reading data from '%s'" % (data_dir + filename))

    return (user_count, still_in_count, answer_count)

def show_status_counts(data):
    (user_count, still_in, answers) = get_status_counts(data)
    data.html_append("answer count=%d<br>" % answers)
    data.html_append("still-in count=%d<br>" % still_in)
    data.html_append("user count=%d\n<p>" % user_count)

######################################################

# returns list of winner tuples (id, alias, name, email)
def get_winners(data):
    file_list = os.listdir(data_dir)
    winners = []
    for filename in file_list:
        m = re.match(user_file_pattern, filename)
        if m:
            try:
                fd = open(data_dir + filename, "r")
                line = fd.readline().strip()
                user_id, alias, name, email, status, jlast_answer = \
                    line.split(',', 5)
                if status == "still-in":
                    winners.append((user_id, alias, name, email))
            except:
                data.add_error_message("Problem reading data from '%s'" % (data_dir + filename))

    return winners

######################################################

def save_winners(data):
    # write out file to next filename in sequence

    # increment sequence number
    data.winner_group += 1
    winner_filepath = data_dir+winner_file_fmt % data.winner_group

    winners = get_winners(data)
    try:
        fd = open(winner_filepath, "w")
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
    else:
        html_start(data, user, True)
        show_waiting_page(data)

######################################################

def show_question_form(data):
    qnum = data.question_num
    try:
        question = tdata[qnum][0]
        red_text = tdata[qnum][1]
        green_text = tdata[qnum][2]
        both_text = tdata[qnum][3]
    except (KeyError, IndexError):
        question = "What is wrong with the game engine?"
        red_text = "Tim doesn't know what he's doing"
        green_text = "Aliens have taken over the server"
        both_text = ""
        data.add_error_message("Corrupt trivia data for question %d" % qnum)

    data.html_append("""
<h1>Question # %s</h1>


%s
<p>
<HR>
""" % (qnum, question))

    data.html_append("""
Please choose an answer:
<FORM method=post action="%s">
<input type="hidden" name="action" value="submit_answer">
<ul>
<table>
  <tr>
    <td><font color="red">Red</font> : </td>
    <td><INPUT type="radio" name="answer" value="red">%s</td>
  </tr><tr>
    <td><font color="green">Green</font> : </td>
    <td><INPUT type="radio" name="answer" value="green">%s</td>
""" % (url, red_text, green_text))

    if both_text:
        data.html_append("""
  </tr><tr>
    <td><font color="red">B</font><font color="green">o</font><font color="red">t</font><font color="green">h</font> : </td>
    <td><INPUT type="radio" name="answer" value="both">%s</td>
""" % both_text)

    # now finish the form
    data.html_append("""
  </tr><tr>
    <td><input type="submit" name="submit" value="Submit"></td>
    <td></td>
  </tr>
</table>
</ul>
<FORM>
<p>
""")

######################################################

def show_qwaiting_page(data, answer):
    qnum = data.question_num
    try:
        question = tdata[qnum][0]
        red_text = tdata[qnum][1]
        green_text = tdata[qnum][2]
        both_text = tdata[qnum][3]
    except (KeyError, IndexError):
        question = "What is wrong with the game engine?"
        red_text = "Tim doesn't know what he's doing"
        green_text = "Aliens have taken over the server"
        both_text = ""
        data.add_error_message("Corrupt trivia data for question %d" % qnum)


    data.html_append("""
<h1>Question # %d</h1>

%s
<p>
<HR>
""" % (qnum, question))

    red_indicator = ""
    green_indicator = ""
    both_indicator = ""

    if answer == "red":
        red_indicator = "<--- Your answer"
    elif answer == "green":
        green_indicator = "<--- Your answer"
    elif answer == "both":
        both_indicator = "<--- Your answer"
    elif answer == "admin-answer":
        pass
    else:
        data.add_error_message("Invalid answer '%s' provided" % answer)

    data.html_append("""
You chose an answer:
<ul>
<table>
  <tr>
    <td><font color="red">Red</font> : </td>
    <td>%s</td>
    <td>%s</td>
  </tr><tr>
    <td><font color="green">Green</font> : </td>
    <td>%s</td>
    <td>%s</td>
""" % (red_text, red_indicator, green_text, green_indicator))

    if both_text:
        data.html_append("""
  </tr><tr>
    <td><font color="red">B</font><font color="green">o</font><font color="red">t</font><font color="green">h</font> : </td>
    <td>%s</td>
    <td>%s</td>
""" % (both_text, both_indicator))

    # finish the page
    data.html_append("""
  </tr>
</table>
</ul>
<p>
<hr>
<h1 align="center">Waiting for answer</h1>
<HR>\n<p>\n
Page will refresh automatically.<br>
<HR>\n<p>\n
""")

    if data.admin_view:
        show_status_counts(data)

######################################################

def show_answer_page(data, answer):
    qnum = data.question_num
    try:
        question = tdata[qnum][0]
        red_text = tdata[qnum][1]
        green_text = tdata[qnum][2]
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

    data.html_append("""
<h1>Question # %s</h1>

%s
<p>
<HR>
""" % (qnum, question))

    red_indicator = ""
    green_indicator = ""
    both_indicator = ""

    if answer == "red":
        red_indicator = "<--- Your answer"
    elif answer == "green":
        green_indicator = "<--- Your answer"
    elif answer == "both":
        both_indicator = "<--- Your answer"
    elif answer == "admin-answer":
        pass
    else:
        data.add_error_message("Invalid answer '%s' provided" % answer)

    red_right = ""
    green_right = ""
    both_right = ""

    if answer_code == "red":
        red_right = "<--- The right answer"
    elif answer_code == "green":
        green_right = "<--- The right answer"
    elif answer_code == "both":
        both_right = "<--- The right answer"
    else:
        data.add_error_message("Invalid answer_code '%s'!!" % answer_code)

    data.html_append("""
You chose an answer:
<ul>
<table>
  <tr>
    <td><font color="red">Red</font> : </td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
  </tr><tr>
    <td><font color="green">Green</font> : </td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
""" % (red_text, red_indicator, red_right, green_text, green_indicator, green_right))

    if both_text:
        data.html_append("""
  </tr><tr>
    <td><font color="red">B</font><font color="green">o</font><font color="red">t</font><font color="green">h</font> : </td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
""" % (both_text, both_indicator, both_right))

    # finish the page
    if answer == answer_code:
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
Page will refresh automatically.<br>
<HR>\n<p>\n
""" % (answer_text, msg))

    if data.admin_view:
        show_status_counts(data)

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


    if data.admin_view:
        show_status_counts(data)
    else:
        if not is_winner:
            data.html_append("Sorry - you did not win this time.\n<p>\n")

        data.html_append("""<HR>\n<p>\n
Page will refresh automatically.<br>
<HR>\n<p>\n""")

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
    try:
        answer = form["answer"].value
    except LookupError:
        answer = user.last_answer

    if state == "question" and answer:
        state = "waiting"

    #data.add_error_message("state='%s'" % state)

    if not data.admin_view:
        if state == "question":
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
            show_qwaiting_page(data, "admin-answer")
        elif state == "answer":
            html_start(data, user)
            show_answer_page(data, "admin-answer")
        elif state == "winners":
            html_start(data, user)
            show_winners_page(data, user)
        else:
            data.add_error_message("unknown trivia state: %s" % state)
            html_start(data, user)
            show_question_form(data)

######################################################

def show_query_form(data):
    data.html_append("""
<h1>Round # %d</h1>

<h1>Rock, Paper, Scissors</h1>
<p>
<HR>
Please choose an item to "throw":
<FORM method=post action="%s">
<input type="hidden" name="action" value="submit_answer">
<ul>
<table>
  <tr>
    <td><INPUT type="radio" name="answer" value="rock">Rock</td>
  </tr><tr>
    <td><INPUT type="radio" name="answer" value="paper">Paper</td>
  </tr><tr>
    <td><INPUT type="radio" name="answer" value="scissors">Scissors</td>
  </tr><tr>
    <td><input type="submit" name="submit" value="Submit"></td>
    <td></td>
  </tr>
</table>
</ul>
<FORM>
<p>
""" % (data.round_num, url))

######################################################

def show_rps_waiting_page(data, answer):
    data.html_append("""
<h1>Round # %d</h1>
<p>
<h1>Rock, Paper, Scissors</h1>
<HR>
""" % (data.round_num))

    rock_indicator = ""
    paper_indicator = ""
    scissors_indicator = ""

    if answer == "rock":
        rock_indicator = "<--- Your throw"
    elif answer == "paper":
        paper_indicator = "<--- Your throw"
    elif answer == "scissors":
        scissors_indicator = "<--- Your throw"
    elif answer == "admin-answer":
        pass
    else:
        data.add_error_message("Invalid guess '%s' provided" % answer)

    data.html_append("""
You chose a "throw":
<ul>
<table>
  <tr>
    <td>Rock : </td>
    <td>%s</td>
  </tr><tr>
    <td>Paper : </td>
    <td>%s</td>
  </tr><tr>
    <td>Scissors : </td>
    <td>%s</td>
  </tr>
</table>
</ul>
<p>
""" % (rock_indicator, paper_indicator, scissors_indicator))

    # finish the page
    data.html_append("""
<HR>
<h1 align="center">Waiting for answer</h1>
<HR>\n<p>\n
Page will refresh automatically.<br>
<HR>\n<p>\n
""")

    if data.admin_view:
        show_status_counts(data)

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

    rock_indicator = ""
    paper_indicator = ""
    scissors_indicator = ""

    if answer == "rock":
        rock_indicator = "<--- Your guess"
    elif answer == "paper":
        paper_indicator = "<--- Your guess"
    elif answer == "scissors":
        scissors_indicator = "<--- Your guess"
    elif answer == "admin-answer":
        pass
    else:
        data.add_error_message("Invalid guess '%s' provided" % answer)

    rock_host = ""
    paper_host = ""
    scissors_host = ""

    if host_throw == "rock":
        rock_host = "<--- The host threw"
    elif host_throw == "paper":
        paper_host = "<--- The host threw"
    elif host_throw == "scissors":
        scissors_host = "<--- The host threw"
    else:
        data.add_error_message("Invalid host throw '%s'!!" % host_throw)

    data.html_append("""
You chose a "throw":
<ul>
<table>
  <tr>
    <td>Rock : </td>
    <td>%s</td>
    <td>%s</td>
  </tr><tr>
    <td>Paper : </td>
    <td>%s</td>
    <td>%s</td>
  </tr><tr>
    <td>Scissors : </td>
    <td>%s</td>
    <td>%s</td>
  </tr>
</table>
</ul>
<p>
""" % (rock_indicator, rock_host, paper_indicator, paper_host,
       scissors_indicator, scissors_host))

    # finish the page
    # this will have to be made generic for alternate items
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
Page will refresh automatically.<br>
<HR>\n<p>\n
""" % msg)

    if data.admin_view:
        show_status_counts(data)

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
    try:
        answer = form["answer"].value
    except:
        answer = user.last_answer

    if data.admin_view:
        answer = "admin-answer"

    if state == "query" and answer:
        state = "waiting"

    #data.add_error_message("state='%s'" % state)

    if not data.admin_view:
        if state == "query":
            html_start(data, user)
            show_query_form(data)
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
            show_query_form(data)
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
            show_query_form(data)

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

######################################################

def html_start(data, user, refresh=False):
    # FIXTHIS - save headers for WSGI use
    html = ""
    if not data.header_shown:
        html += "Content-type: text/html\n"
        if data.cookie:
            html += data.cookie
        html += '\n\n'
        data.header_shown = True
    data.html_append(html)

    #raise Exception, html
    #data.emit_html()

    if refresh and not data.suppress_refresh:
        refresh_str = '<meta http-equiv="refresh" content="%d"; url=%s">' % \
            (REFRESH_SECONDS, url)
    else:
        refresh_str = ''

    data.html_append("""
<HTML>
<HEAD>
<TITLE>ELC Closing Game</TITLE>
%s
</HEAD>
<BODY BGCOLOR="LightBlue">
""" % (refresh_str))

    if user and user.logged_in:
        data.html_append("<hr>| Logged in as: <b>%s</b> |\n" % user.alias)
    else:
        data.html_append("<hr>| Not logged in. |\n")

    if user and data.phase != "registration":
        data.html_append(" == |&nbsp;")

        if user.status == "still-in":
            data.html_append("Status: <b>Still In!!</b> |\n")
        else:
            data.html_append("Status: <b>Eliminated from this round!</b> | \n")

    # data.add_notice("browser cookie='%s'" % data.cookie)
    data.html_append("<br><hr><p>\n")

    data.html_append(data.get_notices_as_html())
    data.html_append(data.get_errors_as_html())
    #data.emit_html()

######################################################

# admin view has some extra tables for managing the game
# line 1 = administration: (sequence) main, undo, edit_game_data, reset
# line 2 = trivia controls: start trivia, show_answer, next_question, declare_winners
# line 3 = rps controls: start rps, show_answer, next_rps, declare_winners

def html_end(data):
    if data.admin_view:
        d = {"url": url}
        d["sequence"] = data.sequence


        # show admin controls
        data.html_append("""
<p><table width="100%%" border=1><tr>
<td><a href="%(url)s">main</a></td>
<td>sequence=%(sequence)s</td>
<td><a href="%(url)s?action=undo">undo</a></td>
<td><a href="%(url)s?action=edit_game">edit game</a></td>
<td><a href="%(url)s?action=reset">reset</a></td>
</tr>""" % d)

        ### show trivia controls
        # make some controls conditional
        d["question_num"] = str(data.question_num)
        d["next_link"] = '<a href="%s?action=next_question">next_question</a>' % url
        last_question = max([int(k) for k in tdata.keys()])

        if data.question_num >= last_question:
            # disable 'next question' link on admin page for last question
            d["next_link"] = "next_question (disabled)"
        data.html_append("""
<tr>
<td><a href="%(url)s?action=start_trivia">start_trivia</a></td>
<td>question #%(question_num)s</td>
<td><a href="%(url)s?action=show_answer">show_answer</a></td>
<td>%(next_link)s</td>
<td><a href="%(url)s?action=declare_winners">declare_winners</a></td>
</tr>""" % d)

        # show rps controls
        d["round_num"] = str(data.round_num)
        d["next_link"] = '<a href="%s?action=next_round">next_round</a>' % url

        last_round = max([int(k) for k in rps_data.keys()])

        if data.round_num >= last_round:
            # disable 'next round' link on admin page for last question
            d["next_link"] = "next_question (disabled)"

        data.html_append("""
<tr>
<td><a href="%(url)s?action=start_rps">start_rps</a></td>
<td>round #%(round_num)s</td>
<td><a href="%(url)s?action=show_result">show_result</a></td>
<td>%(next_link)s</td>
<td><a href="%(url)s?action=declare_winners">declare_winners</a></td>
</tr><tr>
<td><a href="%(url)s?action=done">done</a></td>
</tr></table>""" % d)

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

# returns a 'user' instance, or None if not found
def read_user(user_id):
    # read user file
    user_filepath = data_dir + (user_file_fmt % user_id)
    try:
        fd = open(user_filepath, "r")
        line = fd.readline().strip()
        fd.close()
    except:
        return user_class(NOBODY_USER_ID, "not-logged-in", "", "")

    user_id, alias, name, email, status, last_answer = line.split(',', 5)

    user = user_class(user_id, alias, name, email, status)
    user.last_answer = last_answer
    return user

######################################################

def clear_user_answers(data):
    file_list = os.listdir(data_dir)
    for filename in file_list:
        m = re.match(user_file_pattern, filename)
        if m:
            try:
                fd = open(data_dir + filename, "r+")
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
                    (data_dir + filename))

def reset_user_status(data):
    # change user status back to 'still-in' for all users
    file_list = os.listdir(data_dir)
    for filename in file_list:
        m = re.match(user_file_pattern, filename)
        if m:
            try:
                fd = open(data_dir + filename, "r+")
                line = fd.readline().strip()
                user_id, alias, name, email, status, last_answer = \
                    line.split(',', 5)
                status = 'still-in'
                fd.seek(0, os.SEEK_SET)
                line = "%s,%s,%s,%s,%s,\n" % \
                    (user_id, alias, name, email, status)
                fd.write(line)
                fd.truncate()
                fd.close()
            except:
                data.add_error_message("Problem resetting status in file:" % \
                    (data_dir + filename))

######################################################

def is_correct(data, phase, correct_answer, answer):
    if phase == "trivia":
        return answer == correct_answer

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

    file_list = os.listdir(data_dir)
    for filename in file_list:
        m = re.match(user_file_pattern, filename)
        if m:
            try:
                fd = open(data_dir + filename, "r+")
                line = fd.readline().strip()
                user_id, alias, name, email, status, last_answer = \
                    line.split(',', 5)
                fd.seek(0, os.SEEK_SET)
                if status == "still-in":
                    if not is_correct(data, phase, correct_answer, last_answer):
                        status = "out"
                line = "%s,%s,%s,%s,%s,%s\n" % \
                    (user_id, alias, name, email, status, last_answer)
                fd.write(line)
                fd.truncate()
                fd.close()
            except:
                data.add_error_message("Problem clearing answer from '%s'" % (data_dir + filename))

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
  Your account name (alias) may be displayed during the game if you are among
  a small number of contestants still in the running for a prize, for a particular
  trivia round.
</ul>
""" % (url, user_id, alias, name, email))

def do_register_user(data, form):
    # collect user data from form
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
        email = form["email"].value
    except:
        data.add_error_message("Missing form value for action 'E-mail'")
        email = ""
        error_count += 1

    try:
        name = form["name"].value
    except:
        data.add_error_message("Missing form value for action 'Real Name'")
        name = ""
        error_count += 1

    try:
        alias = form["alias"].value
    except:
        data.add_error_message("Missing form value for action 'Alias'")
        alias = ""
        error_count += 1

    # FIXTHIS - check form data
    # See if confirmation number is already in use
    # check for blank data
    if not user_id:
        data.add_error_message("Missing Event Confirmation Number")
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

    # set cookie expiration for 10 days (in seconds)
    data.cookie = "Set-Cookie: user_id=%s; Max-Age=864000;" % user_id

    # show - Success, waiting for game to start page
    html_start(data, user, True)
    data.html_append("Successfuly registered user: %s\n<p>\n" % alias)
    show_waiting_page(data)
    return

def show_waiting_page(data):
    data.html_append("""
<h1 align="center">Waiting for game to begin...</h1>
<HR>\n<p>\n
Page will refresh automatically.<br>
<HR>\n<p>\n
""")

    user_count = get_registered_user_count()
    data.html_append("Number of registered players=%d\n<p>" % user_count)

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
        data.html_append('Click <a href="%s">here</a> to reload page' % url)
        done = True

    elif action == "start_trivia":
        data.phase = "trivia"
        data.question_num = 1
        data.state = "question"
        write_game_data(data)
        clear_user_answers(data)
        reset_user_status(data)

    elif action == "submit_answer":
        answer = form["answer"].value
        user.last_answer = answer
        user.write_file()

    elif phase == "trivia" and action == "show_answer":
        data.state = "answer"
        write_game_data(data)
        qnum = data.question_num
        answer_code = tdata[qnum][4]
        update_user_status(data, answer_code)

    elif phase == "trivia" and action == "next_question":
        last_state = data.state
        if data.question_num < len(tdata)-1:
            data.question_num += 1
        else:
            data.add_error_message("""Cannot move to next question.
                question_num is already %d""" % data.question_num)
        data.state = "question"
        write_game_data(data)
        clear_user_answers(data)

        # after declaring winners, let everyone back into the game
        if last_state == "winners":
            reset_user_status(data)

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
        reset_user_status(data)

    elif phase == "rps" and action == "show_result":
        data.state = "result"
        write_game_data(data)
        host_throw = rps_data[data.round_num]
        update_user_status(data, host_throw)

    elif phase == "rps" and action == "next_round":
        last_state = data.state
        data.round_num += 1
        data.state = "query"
        write_game_data(data)
        clear_user_answers(data)
        # after declaring winners, let everyone back into the game
        if last_state == "winners":
            reset_user_status(data)

    elif action == "done":
        data.phase = "done"
        write_game_data(data)

    elif action == "reset":
        data.suppress_refresh = "True"
        html_start(data, user)
        data.html_append("""<h1>### RESET ###</h1>
Are you sure you want to reset the game?<br>
If so, click on the link below to really reset the game:<br>
<a href="%s?action=really_reset">Really Reset!!</a>&nbsp;&nbsp;&nbsp;
<a href="%s">cancel (don't reset)</a>
""" % (url, url))

    elif action == "really_reset":
        # save initial variables...
        reset_data = stub_data

        # remove all undo sequence files
        remove_undo_data_files()

        write_game_data(reset_data)
        data.set_data(reset_data)
        data.suppress_refresh = True
        data.add_error_message("Click 'main' to continue")

    elif action == "edit_game":
        # show a form to set values directly
        # bank, score_a, score_b, round, strike_1,2,3
        html_start(data, user)
        data.html_append("""Please edit the game data:
<FORM method=post action="%s">
<INPUT type=hidden name="action" value="set_values">
<table border=0>
""" % url)
        keys = data.keys()
        keys.sort()
        for name in keys:
            value = data[name]
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
        for name in data.keys():
            value = form[name].value
            data[name] = value
        data.html_append("Set values for game from form data!!")
        write_game_data(data)

    elif action == "undo":
        data.suppress_refresh = "True"
        html_start(data, user)
        data.html_append("""<h1>### UNDO ###</h1>
Are you sure you want to undo a step in the game?<br>
If so, click on the link below to really undo 1 game step:<br>
<a href="%s?action=really_undo">Really undo!!</a>&nbsp;&nbsp;&nbsp;
<a href="%s">cancel (don't undo anything)</a>
""" % (url, url))

    elif action == "really_undo":
        # back up one data file
        game_filename = data.game_filename
        os.unlink(game_filename)
        new_data = read_game_data_from_last_file(data)

        # replace items in data with items in new_data
        data.set_data(new_data)
        data.suppresh_refresh = True

    else:
        data.add_error_message("""Unknown action: '%s'
            (or illegal action for this phase)""" % action)

    return done

    # end of do_action()

######################################################

def get_user_id(data, form):
    user_id = None
    cookie = os.environ["HTTP_COOKIE"]
    #data.add_notice("in get_user_id(): os.environ=%s" % str(os.environ))
    #data.add_notice("in get_user_id(): cookie=%s" % cookie)
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

    return user_id

######################################################

def main():
    form = cgi.FieldStorage()

    # we have a chicken-and-egg problem here
    pre_data = data_class()
    data = read_game_data_from_last_file(pre_data)
    data.html = pre_data.html
    data.err_msg_list = pre_data.err_msg_list

    user_id = get_user_id(data, form)
    # data.add_notice("user_id from form = '%s'" % str(user_id))
    user = user_class(NOBODY_USER_ID, "not-logged-in", "", "")
    if user_id == ADMIN_USER_ID:
        user = user_class(ADMIN_USER_ID, "admin", ADMIN_NAME, "tim.bird@sony.com")
        user.logged_in = True
    else:
        if user_id:
            if os.path.exists(data_dir + (user_file_fmt % user_id)):
                user = read_user(user_id)
                user.logged_in = True
            else:
                data.add_error_message("Invalid user_id '%s' specified in cookie" % user_id)

    done = False
    if "action" in form:
        action = form["action"].value
        done = do_action(action, data, form, user)

        # do_action doesn't return if it handled the action completely

    if not done:
        show_page(data, form, user)

    html_end(data)
    # start_response(status, response_header)
    data.emit_html()

if __name__ == "__main__":
    main()
