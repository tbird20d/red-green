# trivia data for the red-green game, to be imported by rg.cgi
# each question has a key that is the question number (as a string)
# and value that is a list with the question and answer
#   that is: qdata[question_num][0] = question text
#            qdata[question_num][1] = answer code
#            qdata[question_num][2] = answer text
qdata = {
"1": [
      "Do bears poop in the woods?",
      "true",
      "false",
      "",
      "red",
      "According to wikipedia, bears poop in the woods 90% of the time"
     ],
"2": [
      "What color do you get by mixing blue and yellow?",
      "red",
      "green",
      "",
      "green",
      "Or maybe chartreuse, if you use too much yellow..."
     ],
"3": [ "Who benefits from open source?",
      "Developers",
      "Customers",
      "Companies",
      "both",
      "Everybody wins!!"
     ],
}
