# trivia data for the red-green game, to be imported by rg.cgi
# each question has a key that is the question number
# and value that is a list with the question and answer data
#   that is: tdata[qnum][0] = question text
#            tdata[qnum][1] = green answer
#            tdata[qnum][2] = red answer
#            tdata[qnum][3] = both answer
#            tdata[qnum][4] = answer code
#            tdata[qnum][5] = answer text

# the question text and answer text may include format
# strings to reference images, like so: %(image_url)s

tdata = {
1: [
      """
         [Warmup question] What is the main benefit of Open Source?
      """,
      "freedom",
      "free price",
      "",
      "green",
      """
         Open Source provides freedom for users and developers.
      """
     ],
2: [
      """
         What is the the airspeed velocity of an unladen swallow?
      """,
      "26 mph",
      "I don't know that!",
      "",
      "red|green",
      """
         Either answer is OK.
      """
     ],
99: [ """
        question
      """,
      "green answer",
      "red answer",
      "",
      "answer_code [green, red, both]",
      """
         answer_text
         <img src="%(image_url)s/foo.jpg" height="64">
      """
     ],
}
