#!/usr/bin/env python

# Copyright 2020 by Tim Bird

# turn this on to show the game data in the admin view
# (for debugging)
show_data = 0

import sys
import os
import cgi
import re
import cgitb

cgitb.enable()

data_dir = "/home/tbird/work/games/red-green/rgdata/"
game_file_pattern = "rgdata-([0-9][0-9][0-9]).txt"
game_file_fmt = "rgdata-%03d.txt"

user_file_pattern = "rg-user-.*[.]txt"
user_file_fmt = "rg-user-%s.txt"
url = "rg.cgi"

winner_file_fmt = "winners-%02d.txt"

# To login as administrator, use the url:
# http://localhost:8000/rg.cgi?user_id=admin-game-admin
#  or enter: admin-game-admin, Real Name=Tim in the registration form
ADMIN_USER_ID = "admin-game-admin"
ADMIN_NAME = "Tim"

# import the trivia data
sys.path.append(data_dir)

# this will provide the 'qdata' dictionary
# each entry is a list, with question_num as the key:
# and a list with:
#    0) question text
#    1) red answer text
#    2) green answer text
#    3) both answer text
#    4) answer code
#    5) answer text (explanation)
#
# The answer code can be "red", "green", or "both".
#
# {"1": ["question #1", "true", "false", "" "red", "answer #1 because..."],
#  "2": ["question #2", "less than 10", "10 or more", "", "green", "answer #2"],
#  ...
# }
from trivia import *

# this will provide the 'rps_data' dictionary
# each entry is a string with, round_num as the key:
# The host_throw can be "rock", "paper", or "scissors".
#
# {"1": "rock",
#  "2": "scissors",
#  ...
# }
from rps import *

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


class data_class():
    def __init__(self):
        self.data = {}

    def __getitem__(self):
        if self.data.has_key(key):
            item = self.data[key]
        elif hasattr(self, key):
            item = getattr(self,key)
        else:
            raise KeyError

        if callable(item):
            return item(self)
        else:
            return item

    def __setitem__(self, key, value):
        self.data[key] = value

    def keys(self):
        # FIXTHIS - are the __dict__ keys needed?
        keys = self.__dict__.keys()
        keys.append(self.data.keys())
        return keys

old_stub_data = {
"data_sequence":"0",
"winner_group":"1",
"phase":"registration", # registration, trivia, rps
"question_num":"1",
"state":"question", # question, waiting, answer, winners ; for trivia
    # query, waiting, result, winners ; for rps
"round_num":"1",
}

stub_data = data_class()
stub_data["data_sequence"] = "0"
stub_data["winner_group"] = "1"
stub_data["phase"] = "registration"  # registration, trivia, rps
stub_data["question_num"] = "1"
stub_data["state"] = "question" # question, waiting, answer, winners ; for trivia
    # query, waiting, result, winners ; for rps
stub_data["round_num"] = "1"

class user_class():
    def __init__(self, user_id, alias, name, email, status="still-in"):
        self.user_id = user_id
        self.alias = alias
        self.name = name
        self.email = email
        # status can be 'still-in' or 'out'
        self.status = status
        self.last_answer = ""

    def write_file(self):
        line="%s,%s,%s,%s,%s,%s\n" % (self.user_id, self.alias, self.name, self.email, self.status, self.last_answer)
        user_filepath = data_dir + (user_file_fmt % self.user_id)
        fd = open(user_filepath, "w")
        fd.write(line)
        fd.close()

######################################################

err_msg_list = []
def add_error_message(data, msg):
    global err_msg_list

    err_msg_list.append('<font color="red">ERROR: %s<br></font>' % msg)

######################################################

def get_errors():
    global err_msg_list

    html = ""
    if err_msg_list:
        html += '<table bgcolor="pink"><tr><td>\n'
        last_msg = err_msg_list[-1]
        for msg in err_msg_list:
            html += msg+"\n"
            if msg != last_msg:
                html += "<BR>\n"
        html += '</td></tr></table>\n'
        err_msg_list = []
    return html


######################################################

header_shown = False
def get_http_header(data):
    global header_shown

    html = ""
    if not header_shown:
        html += "Content-type: text/html\n"
        if data.has_key("cookie"):
            html += data["cookie"]
        html += '\n\n'
        header_shown = True
    return html

######################################################

def read_game_data_from_last_file():
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
    return read_game_data(last_game_filename)

######################################################

# FIXTHIS - need to save off err_msg_list and html, in case
# they already have data
def read_game_data(game_filename):
    try:
        game_lines = open(game_filename, "r").readlines()
    except:
        add_error_message("Warning: failed to open game data file: %s\n<p>\n" % game_filename)
        game_lines = []

    #data = stub_data.copy()
    data = stub_data.data
    for line in game_lines:
        line = line.strip()
        if line and line[0]!='#':
            (name, value) = line.split('=',1)
            # FIXTHIS - (data_change) use data_class.set_attr instead???
            data[name] = value

    data["game_filename"] = game_filename
    return data

######################################################

def write_game_data(data):
    # write out file to next filename in sequence

    # increment sequence number
    data_sequence = int(data["data_sequence"])
    data_sequence += 1
    data["data_sequence"] = str(data_sequence)
    game_filename = data_dir+game_file_fmt % data_sequence
    data["game_filename"] = game_filename

    fd = open(game_filename, "w")
    klist = data.keys()
    klist.sort()
    for name in klist:
        if name not in ["err_msg_list", "html"]:
            fd.write("%s=%s\n" % (name, data[name]))
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
def get_status_counts():
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
                user_id, alias, name, email, status, last_answer = line.split(',',5)
                if status == "still-in":
                    still_in_count += 1
                if last_answer.strip():
                    answer_count += 1
            except:
                add_error_message("Problem reading data from '%s'" % (data_dir + filename))

    return (user_count, still_in_count, answer_count)

######################################################

# returns list of winner tuples (id, alias, name, email)
def get_winners():
    file_list = os.listdir(data_dir)
    winners = []
    for filename in file_list:
        m = re.match(user_file_pattern, filename)
        if m:
            try:
                fd = open(data_dir + filename, "r")
                line = fd.readline().strip()
                user_id, alias, name, email, status, last_answer = line.split(',',5)
                if status == "still-in":
                    winners.append((user_id, alias, name, email))
            except:
                add_error_message("Problem reading data from '%s'" % (data_dir + filename))

    return winners

def save_winners(data):
    # write out file to next filename in sequence

    # increment sequence number
    winner_group = int(data["winner_group"])
    winner_group += 1
    data["winner_group"] = str(winner_group)
    winner_filepath = data_dir+winner_file_fmt % winner_group

    winners = get_winners()
    try:
        fd = open(winner_filepath, "w")
        for w in winners:
            line = "%s,%s,%s,%s\n" % w
            fd.write(line)
        fd.close()
    except:
        add_error_message("Problem writing winner file %s" % winner_filepath)


######################################################

def question_value(data, row):
    row = int(row)
    round = int(data["round"])
    return row * (round * 100)

######################################################


# show the game board
# big_board indicates whether to use large fonts and fill the screen

# here is some size data
big_screen_data = {
    "border":0,
    "debug":0,
    "size":5,
    "tsize":7,
    "fsize":6,
    # main gameboard offsets
    "w0":100,
    "h0":30,
    # main gameboard cell dimensions
    "w":200,
    #"h":80,
    "h":80,
    "cat_font":5,
    "answer_height":440,
    "value_font_size":5,
    # score table stuff
    "score_offset":300,
    "score_spacing":200,
}

small_screen_data = {
    "border":0,
    "debug":0,
    "size":3,
    "tsize":3,
    "fsize":3,
    # main gameboard offsets
    "w0":1,
    "h0":1,
    # main gameboard cell dimensions
    "w":60,
    "h":60,
    "cat_font":3,
    "answer_height":200,
    "value_font_size":3,
    # score table stuff
    "score_offset":100,
    "score_spacing":40,
}

######################################################

def show_registration(data, user=None):
    if not user:
        # show player registration form
        html_start(data, user)
        print("This is the registration page.\n<p>\n")
        show_register_form(data)
    else:
        html_start(data, user, True)
        show_waiting_page(data)

######################################################

def show_question_form(data, form, user):
    question_num = data["question_num"]
    question = qdata[question_num][0]
    red_text = qdata[question_num][1]
    green_text = qdata[question_num][2]
    both_text = qdata[question_num][3]

    print """
<h1>Question # %s</h1>


%s
<p>
<HR>
""" % (question_num, question)

    print """
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
""" % (url, red_text, green_text)

    if both_text:
        print """
  </tr><tr>
    <td><font color="red">B</font><font color="green">o</font><font color="red">t</font><font color="green">h</font> : </td>
    <td><INPUT type="radio" name="answer" value="both">%s</td>
""" % both_text

    # now finish the form
    print """
  </tr><tr>
    <td><input type="submit" name="submit" value="Submit"></td>
    <td></td>
  </tr>
</table>
</ul>
<FORM>
<p>
"""

######################################################

def show_qwaiting_page(data, answer, user):
    question_num = data["question_num"]
    question = qdata[question_num][0]
    red_text = qdata[question_num][1]
    green_text = qdata[question_num][2]
    both_text = qdata[question_num][3]

    print """
<h1>Question # %s</h1>

%s
<p>
<HR>
""" % (question_num, question)

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
        add_error_message("Invalid answer '%s' provided" % answer)

    print """
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
""" % (red_text, red_indicator, green_text, green_indicator)

    if both_text:
        print """
  </tr><tr>
    <td><font color="red">B</font><font color="green">o</font><font color="red">t</font><font color="green">h</font> : </td>
    <td>%s</td>
    <td>%s</td>
""" % (both_text, both_indicator)

    # finish the page
    print """
  </tr>
</table>
</ul>
<p>
<hr>
<h1 align="center">Waiting for answer</h1>
<HR>\n<p>\n
Page will refresh automatically.<br>
<HR>\n<p>\n
"""

    if admin_view:
        (user_count, still_in, answers) = get_status_counts()
        print("answer count=%d<br>" % answers)
        print("still-in count=%d<br>" % still_in)
        print("user count=%d\n<p>" % user_count)

######################################################

def show_answer_page(data, answer, user):
    question_num = data["question_num"]
    question = qdata[question_num][0]
    red_text = qdata[question_num][1]
    green_text = qdata[question_num][2]
    both_text = qdata[question_num][3]
    answer_code = qdata[question_num][4]
    answer_text = qdata[question_num][5]

    #add_error_message("answer=%s" % answer)

    print """
<h1>Question # %s</h1>

%s
<p>
<HR>
""" % (question_num, question)

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
        add_error_message("Invalid answer '%s' provided" % answer)

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
        add_error_message("Invalid answer_code '%s'!!" % answer_code)

    print """
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
""" % (red_text, red_indicator, red_right, green_text, green_indicator, green_right)

    if both_text:
        print """
  </tr><tr>
    <td><font color="red">B</font><font color="green">o</font><font color="red">t</font><font color="green">h</font> : </td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
""" % (both_text, both_indicator, both_right)

    # finish the page
    if answer == answer_code:
        msg = "<h2>You got it right!!</h2>"
    else:
        msg = "Sorry - you didn't get it right!!"

    print """
  </tr>
</table>
</ul>
<p>\n<HR>\n<p>\n
%s
<HR>\n<p>\n
Page will refresh automatically.<br>
<HR>\n<p>\n
""" % msg

    if admin_view:
        (user_count, still_in, answers) = get_status_counts()
        print("answer count=%d<br>" % answers)
        print("still-in count=%d<br>" % still_in)
        print("user count=%d\n<p>" % user_count)

######################################################

def show_winners_page(data, user):
    winners = get_winners()

    print("""<h1>We have winners!!</h1>
Here is the list of winners:
<hr>
<ul>
""")

    is_winner = False
    for w in winners:
        user_id = w[0]
        alias = w[1]
        if user_id == user.user_id:
            print("<li><b>%s</b>&nbsp;&nbsp;  <-- This is you!! - You are a winner!!" % alias)
            is_winner = True
        else:
            print("<li>%s" % alias)
        print("</li>")

    print("</ul>\n<hr>\n<p>\n")


    if admin_view:
        (user_count, still_in, answers) = get_status_counts()
        print("answer count=%d<br>" % answers)
        print("still-in count=%d<br>" % still_in)
        print("user count=%d\n<p>" % user_count)
    else:
        if not is_winner:
            print("Sorry - you did not win this time.\n<p>\n")

        print("""<HR>\n<p>\n
Page will refresh automatically.<br>
<HR>\n<p>\n""")

######################################################

def show_trivia(data, form, user):
    global admin_view

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
    state = data["state"]
    try:
        answer = form["answer"].value
    except:
        answer = user.last_answer

    if state == "question" and answer:
        state = "waiting"

    #add_error_message("state='%s'" % state)

    if not admin_view:
        if state == "question":
            html_start(data, user)
            show_question_form(data, form, user)
        elif state == "waiting":
            html_start(data, user, True)
            show_qwaiting_page(data, answer, user)
        elif state == "answer":
            html_start(data, user, True)
            show_answer_page(data, answer, user)
        elif state == "winners":
            html_start(data, user, True)
            show_winners_page(data, user)
        else:
            add_error_message("unknown trivia state: %s" % state)
            html_start(data, user)
            show_question_form(data, form, user)
    else:
        #if state == "question":
        #    html_start(data, user)
        #    show_question_form(data, form, user)
        if state == "question" or state == "waiting":
            html_start(data, user, True)
            show_qwaiting_page(data, "admin-answer", user)
        elif state == "answer":
            html_start(data, user)
            show_answer_page(data, "admin-answer", user)
        elif state == "winners":
            html_start(data, user)
            show_winners_page(data, user)
        else:
            add_error_message("unknown trivia state: %s" % state)
            html_start(data, user)
            show_question_form(data, form, user)

######################################################

def show_query_form(data, form, user):
    round_num = data["round_num"]

    print """
<h1>Round # %s</h1>

<h1>Rock, Paper, Scissors</h1>
<p>
<HR>
""" % (round_num)

    print """
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
""" % url

######################################################

def show_rps_waiting_page(data, answer, user):
    round_num = data["round_num"]

    print """
<h1>Round # %s</h1>
<p>
<h1>Rock, Paper, Scissors</h1>
<HR>
""" % (round_num)

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
        add_error_message("Invalid guess '%s' provided" % answer)

    print """
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
""" % (rock_indicator, paper_indicator, scissors_indicator)

    # finish the page
    print """
<HR>
<h1 align="center">Waiting for answer</h1>
<HR>\n<p>\n
Page will refresh automatically.<br>
<HR>\n<p>\n
"""

    if admin_view:
        (user_count, still_in, answers) = get_status_counts()
        print("answer count=%d<br>" % answers)
        print("still-in count=%d<br>" % still_in)
        print("user count=%d\n<p>" % user_count)

######################################################

def show_result_page(data, answer, user):
    round_num = data["round_num"]
    host_throw = rps_data[round_num]

    #add_error_message("host_throw=%s" % host_throw)

    print """
<h1>Round # %s</h1>
<p>
<h1>Rock, Paper, Scissors</h1>
<HR>
""" % (round_num)

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
        add_error_message("Invalid guess '%s' provided" % answer)

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
        add_error_message("Invalid host throw '%s'!!" % host_throw)

    print """
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
""" % (rock_indicator, rock_host, paper_indicator, paper_host, scissors_indicator, scissors_host)

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
    print """
  </tr>
</table>
</ul>
<p><HR>\n<p>\n
%s
<p><HR>\n<p>\n
Page will refresh automatically.<br>
<HR>\n<p>\n
""" % msg

    if admin_view:
        (user_count, still_in, answers) = get_status_counts()
        print("answer count=%d<br>" % answers)
        print("still-in count=%d<br>" % still_in)
        print("user count=%d\n<p>" % user_count)

######################################################

def show_rps(data, form, user):
    global admin_view

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
    state = data["state"]
    try:
        answer = form["answer"].value
    except:
        answer = user.last_answer

    if admin_view:
        answer="admin-answer"

    if state == "query" and answer:
        state = "waiting"

    #add_error_message("state='%s'" % state)

    if not admin_view:
        if state == "query":
            html_start(data, user)
            show_query_form(data, form, user)
        elif state == "waiting":
            html_start(data, user, True)
            show_rps_waiting_page(data, answer, user)
        elif state == "result":
            html_start(data, user, True)
            show_result_page(data, answer, user)
        elif state == "winners":
            html_start(data, user, True)
            show_winners_page(data, user)
        else:
            add_error_message("unknown rps state: %s" % state)
            html_start(data, user)
            show_query_form(data, form, user)
    else:
        if state == "query" or state == "waiting":
            html_start(data, user, True)
            show_rps_waiting_page(data, answer, user)
        elif state == "result":
            html_start(data, user)
            show_result_page(data, answer, user)
        elif state == "winners":
            html_start(data, user)
            show_winners_page(data, user)
        else:
            add_error_message("unknown rps state: %s" % state)
            html_start(data, user)
            show_query_form(data, form, user)

######################################################

def show_page(data, user):
    phase = data["phase"]

    if phase=="registration" or not user:
        show_registration(data, user)
        return

    # get size data for display
    #if player_view:
    #    size_data = big_screen_data
    #else:
    #    size_data = small_screen_data
    #
    #data.update(size_data)

    if phase=="trivia":
        show_trivia(data, form, user)
        return

    if phase=="rps":
        show_rps(data, form, user)
        return

    # we must be done
    html_start(data, user)
    print ("""<h1>Game Over</h1>
Thank you for playing the Embedded Linux Conference
closing game.
<p>
I hope you had a good time!!
    """)

######################################################

suppress_refresh = False

def html_start(data, user, refresh=False):
    html = get_http_header(data)
    #raise Exception, html
    print html

    suppress_refresh = False
    try:
        if data["suppress_refresh"] == "True":
            suppress_refresh = True
    except:
        pass

    if refresh and not suppress_refresh:
        refresh_str = '<meta http-equiv="refresh" content="2; url=%s">' % url
    else:
        refresh_str = ''

    try:
        cookie = data["cookie"]
    except:
        cookie = "No cookie"

    if user:
        user_alias = user.alias
    else:
        user_alias = None

    print """
<HTML>
<HEAD>
<TITLE>ELC Closing Game</TITLE>
%s
</HEAD>
<BODY BGCOLOR="LightBlue">
""" % (refresh_str)

    if user_alias:
        print("<hr>| Logged in as: <b>%s</b> |\n" % user_alias)
    else:
        print("<hr>| Not logged in. |\n")

    if user and data["phase"] != "registration":
        print(" == |&nbsp;")

        if user.status == "still-in":
            print("Status: <b>Still In!!</b> |\n")
        else:
            print("Status: <b>Eliminated from this round!</b> | \n")

    print("<br><hr><p>\n")

    html = get_errors()
    print html

######################################################

# admin view has some extra tables for managing the game
# line 1 = administration: (sequence) main, undo, edit_game_data, reset
# line 2 = trivia controls: start trivia, show_answer, next_question, declare_winners
# line 3 = rps controls: start rps, show_answer, next_rps, declare_winners

def html_end(data):
    global admin_view

    if admin_view:
        d = {"url": url}
        d["sequence"] = data["data_sequence"]


        # show admin controls
        print """
<p><table width="100%%" border=1><tr>
<td><a href="%(url)s">main</a></td>
<td>sequence=%(sequence)s</td>
<td><a href="%(url)s?action=undo">undo</a></td>
<td><a href="%(url)s?action=edit_game">edit game</a></td>
<td><a href="%(url)s?action=reset">reset</a></td>
</tr>""" % d

        ### show trivia controls
        # make some controls conditional
        question_num = int(data["question_num"])

        d["question_num"] = str(question_num)
        d["next_link"] = '<a href="%s?action=next_question">next_question</a>' % url
        last_question = max( [ int(k) for k in qdata.keys()] )

        if question_num >= last_question:
            # disable 'next question' link on admin page for last question
            d["next_link"] = "next_question (disabled)"
        print """
<tr>
<td><a href="%(url)s?action=start_trivia">start_trivia</a></td>
<td>question #%(question_num)s</td>
<td><a href="%(url)s?action=show_answer">show_answer</a></td>
<td>%(next_link)s</td>
<td><a href="%(url)s?action=declare_winners">declare_winners</a></td>
</tr>""" % d

        # show rps controls
        round_num = int(data["round_num"])

        d["round_num"] = str(round_num)
        d["next_link"] = '<a href="%s?action=next_round">next_round</a>' % url

        last_round = max( [ int(k) for k in rps_data.keys()] )

        if round_num >= last_round:
            # disable 'next round' link on admin page for last question
            d["next_link"] = "next_question (disabled)"

        print """
<tr>
<td><a href="%(url)s?action=start_rps">start_rps</a></td>
<td>round #%(round_num)s</td>
<td><a href="%(url)s?action=show_result">show_result</a></td>
<td>%(next_link)s</td>
<td><a href="%(url)s?action=declare_winners">declare_winners</a></td>
</tr><tr>
<td><a href="%(url)s?action=done">done</a></td>
</tr></table>""" % d

    html = get_errors()
    print html

    print """</BODY></HTML>"""

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
        return None

    user_id, alias, name, email, status, last_answer = line.split(',',5)

    user = user_class(user_id, alias, name, email, status)
    user.last_answer = last_answer
    return user

######################################################

def clear_user_answers():
    file_list = os.listdir(data_dir)
    for filename in file_list:
        m = re.match(user_file_pattern, filename)
        if m:
            #try:
                fd = open(data_dir + filename, "r+")
                line = fd.readline().strip()
                user_id, alias, name, email, status, last_answer = line.split(',',5)
                fd.seek(0, os.SEEK_SET)
                line="%s,%s,%s,%s,%s,\n" % (user_id, alias, name, email, status)
                fd.write(line)
                fd.truncate()
                fd.close()
            #except:
            #    add_error_message("Problem clearing answer from '%s'" % (data_dir + filename))

def reset_user_status():
    # change user status back to 'still-in' for all users
    file_list = os.listdir(data_dir)
    for filename in file_list:
        m = re.match(user_file_pattern, filename)
        if m:
            #try:
                fd = open(data_dir + filename, "r+")
                line = fd.readline().strip()
                user_id, alias, name, email, status, last_answer = line.split(',',5)
                fd.seek(0, os.SEEK_SET)
                line="%s,%s,%s,%s,%s,\n" % (user_id, alias, name, email, 'still-in')
                fd.write(line)
                fd.truncate()
                fd.close()
            #except:
            #    add_error_message("Problem clearing answer from '%s'" % (data_dir + filename))

######################################################

def is_correct(phase, correct_answer, answer):
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

    add_error_message("Invalid phase '%s' detected in is_correct()" % phase)
    return False

def update_user_status(data, correct_answer):
    #add_error_message("correct_answer=%s" % correct_answer)
    phase = data["phase"]

    file_list = os.listdir(data_dir)
    for filename in file_list:
        m = re.match(user_file_pattern, filename)
        if m:
            try:
                fd = open(data_dir + filename, "r+")
                line = fd.readline().strip()
                user_id, alias, name, email, status, last_answer = line.split(',',5)
                fd.seek(0, os.SEEK_SET)
                if status == "still-in":
                    if not is_correct(phase, correct_answer, last_answer):
                        status = "out"
                line="%s,%s,%s,%s,%s,%s\n" % (user_id, alias, name, email, status, last_answer)
                fd.write(line)
                fd.truncate()
                fd.close()
            except:
                add_error_message("Problem clearing answer from '%s'" % (data_dir + filename))

######################################################

def show_register_form(data):
    # FIXTHIS - add form to fill in already-entered data, if available
    print """
<FORM method=post action="%s">
<input type="hidden" name="action" value="register_user">
<table>
  <tr>
    <td>Event Confirmation Number:</td>
    <td align="right"><INPUT type=text name="user_id"></td>
  </tr><tr>
    <td>Account Name (alias):</td>
    <td align="right"><INPUT type=text name="alias"></td>
  </tr><tr>
    <td>Real Name:</td>
    <td align="right"><INPUT type=text name="name"></td>
  </tr><tr>
    <td>E-mail:</td>
    <td align="right"><INPUT type=text name="email"></td>
  </tr><tr>
    <td><input type="Submit" name="submit" value="Cancel"></td>
    <td><input type="Submit" name="submit" value="Submit"></td>
  </tr>
</table>
</FORM>
<p>
<ul>
  The Event Confirmation Number is avaialble in your registration confirmation
  email for the event.  Please check that email to find the number.

  Note that the 'Real Name' and 'E-mail' will not be displayed or shared with
  anyone.<br>
  They will only be used to contact you in the event you win a prize.<br>
  Your account name (alias) may be displayed during the game if you are among
  a small number of contestants still in the running for a prize, for a particular
  trivia round.
</ul>
""" % url

def do_register_user(data, form):
    # collect user data from form
    error_count = 0
    try:
        user_id = form["user_id"].value
    except:
        add_error_message("Missing form value for 'Event Confirmation Number'")
        error_count += 1

    try:
        email = form["email"].value
    except:
        add_error_message("Missing form value for action 'E-mail'")
        error_count += 1

    try:
        name = form["name"].value
    except:
        add_error_message("Missing form value for action 'Real Name'")
        error_count += 1

    try:
        alias = form["alias"].value
    except:
        add_error_message("Missing form value for action 'Alias'")
        error_count += 1

    # FIXTHIS - check form data
    # See if confirmation number is already in use
    # check for blank data
    if not user_id:
        add_error_message("Missing Event Confirmation Number")
        error_count += 1

    if error_count:
        html_start(data, None)
        show_register_form(data)
        html_end(data)
        sys.exit(0)

    if user_id == ADMIN_USER_ID and name == ADMIN_NAME:
        user = create_user(user_id, "admin", name, "tim.bird@sony.com")
    else:
        # save data to user database
        user = create_user(user_id, alias, name, email)

    # set cookie expiration for 10 days (in seconds)
    data["cookie"] = "Set-Cookie: user_id=%s; Max-Age=864000;" % user_id

    # show - Success, waiting for game to start page
    html_start(data, user, True)
    print("Successfuly registered user: %s\n<p>\n" % alias)
    show_waiting_page(data)
    html_end(data)
    sys.exit(0)

def show_waiting_page(data):
    print("""
<h1 align="center">Waiting for game to begin...</h1>
<HR>\n<p>\n
Page will refresh automatically.<br>
<HR>\n<p>\n
""")

    user_count = get_registered_user_count()
    print("Number of registered players=%d\n<p>" % user_count)

def do_action(action, data, form, user):
    phase = data["phase"]

    #print "action=<b>%s</b><br>" % action
    if action == "none":
        return

    if action == "register_user":
        do_register_user(data, form)

    if action == "logout":
        data["cookie"] = "Set-cookie: user_id=;expires=Thu, 01 Jan 1970 00:00:01 GMT";
        html_start(data, None)
        print("<h1>User logged out</h1>")
        print('Click <a href="%s">here</a> to reload page' % url)
        html_end(data)
        return

    if action == "start_trivia":
        data["phase"] = "trivia"
        data["question_num"] = "1"
        data["state"] = "question" # can be one of "question", "waiting, "answer"
        write_game_data(data)
        clear_user_answers()
        reset_user_status()
        return

    if action == "submit_answer":
        answer = form["answer"].value
        user.last_answer = answer
        user.write_file()
        return

    if phase=="trivia" and action == "show_answer":
        data["state"] = "answer"
        write_game_data(data)
        question_num = data["question_num"]
        answer_code = qdata[question_num][4]
        update_user_status(data, answer_code)
        return

    if phase=="trivia" and action == "next_question":
        last_state = data["state"]
        question_num = int(data["question_num"]) + 1
        data["question_num"] = str(question_num)
        data["state"] = "question"
        write_game_data(data)
        clear_user_answers()

        # after declaring winners, let everyone back into the game
        if last_state == "winners":
            reset_user_status()
        return

    if action == "declare_winners":
        data["state"] = "winners"
        save_winners(data)
        # write game data AFTER saving winners
        write_game_data(data)
        return

    if action == "start_rps":
        #do_start_rps(data, form, user)
        data["phase"] = "rps"
        data["state"] = "query"
        data["round"] = "1"
        write_game_data(data)
        clear_user_answers()
        reset_user_status()
        return

    if phase == "rps" and action == "show_result":
        data["state"] = "result"
        write_game_data(data)
        round_num = data["round_num"]
        host_throw = rps_data[round_num]
        update_user_status(data, host_throw)
        return

    if phase == "rps" and action == "next_round":
        last_state = data["state"]
        round_num = int(data["round_num"]) + 1
        data["round_num"] = str(round_num)
        data["state"] = "query"
        write_game_data(data)
        clear_user_answers()
        # after declaring winners, let everyone back into the game
        if last_state == "winners":
            reset_user_status()
        return

    if action == "done":
        data["phase"] = "done"
        write_game_data(data)
        return

    if action == "reset":
        data["suppress_refresh"] = "True"
        html_start(data, user)
        print """<h1>### RESET ###</h1>
Are you sure you want to reset the game?<br>
If so, click on the link below to really reset the game:<br>
<a href="%s?action=really_reset">Really Reset!!</a>&nbsp;&nbsp;&nbsp;
<a href="%s">cancel (don't reset)</a>
""" % (url, url)
        return

    if action=="really_reset":
        # save some variables...
        #reset_data = stub_data.copy()
        reset_data = stub_data.data

        # remove all undo sequence files
        remove_undo_data_files()

        write_game_data(reset_data)
        data.update(reset_data)
        return

    if action=="edit_game":
        # show a form to set values directly
        # bank, score_a, score_b, round, strike_1,2,3
        html_start(data, user)
        print "Please edit the game data:"
        print """<FORM method=post action="%s">
<INPUT type=hidden name="action" value="set_values">
<table border=0>
""" % url
        keys = data.keys()
        keys.sort()
        for name in keys:
            value = data[name]
            print """
<tr>
<TD BGCOLOR="#dddddd" WIDTH="55%%">
%s</td>
<TD WIDTH="33%%"><INPUT type="Text" name="%s" size="50" value="%s">
</TD>
</tr>""" % (name, name, value)

        print """
</table>
<ul>
<input type="Submit" name="submit" value="Submit">
</ul>"""
        html_end(data)
        sys.exit(0)

    if action=="set_values":
        # set values from the form
        for name in data.keys():
            value = form[name].value
            data[name] = value
        print "Set values for game from form data!!"
        write_game_data(data)
        return

    if action=="undo":
        data["suppress_refresh"] = "True"
        html_start(data, user)
        print """<h1>### UNDO ###</h1>
Are you sure you want to undo a step in the game?<br>
If so, click on the link below to really undo 1 game step:<br>
<a href="%s?action=really_undo">Really undo!!</a>&nbsp;&nbsp;&nbsp;
<a href="%s">cancel (don't undo anything)</a>
""" % (url, url)
        return

    if action=="really_undo":
        # back up one data file
        game_filename = data["game_filename"]
        os.unlink(game_filename)
        new_data = read_game_data_from_last_file()

        # replace items in data with items in new_data
        for key in data.keys():
            del(data[key])

        data.update(new_data)
        return

    add_error_message("Unknown action: '%s' (or illegal action for this phase)" % action)

    # end of do_action()

######################################################

admin_view = False

def get_user_id(data, form):
    global admin_view

    user_id = None
    cookie = os.environ["HTTP_COOKIE"]
    #add_error_message("os.environ=%s" % str(os.environ))
    #add_error_message("cookie=%s" % cookie)
    if "user_id=" in cookie:
        (first, value) = cookie.split("user_id=",1)
        if value.find(";") != -1:
            (value, rest) = value.split(";",1)
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
        data["cookie"] = "Set-Cookie: user_id=%s; Max-Age=864000;" % user_id

    if user_id == ADMIN_USER_ID:
        admin_view = True

    return user_id


if __name__ == "__main__":
    form = cgi.FieldStorage()

    data = read_game_data_from_last_file()
    data["html"] = ""

    user_id = get_user_id(data, form)
    if user_id != ADMIN_USER_ID:
        if not os.path.exists(data_dir + (user_file_fmt % user_id)):
            add_error_message("Invalid user_id specified in cookie")
        user = read_user(user_id)
    else:
        user = user_class(ADMIN_USER_ID, "admin", ADMIN_NAME, "tim.bird@sony.com")

    if "action" in form:
        action = form["action"].value
        do_action(action, data, form, user)

        # do_action doesn't return if it handled the action completely

    show_page(data, user)

    # use this for debugging
    if show_data and admin_view:
        print "Debug:: data=%s\n<p>\n" % data

    html_end(data)
