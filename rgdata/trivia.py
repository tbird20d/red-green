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
         What company launched the rocket shown here?
         <p>
         <img src="%(image_url)s/spacex-logo-on-rocket.jfif" height="150">
      """,
      "SpaceX",
      "Blue Origin",
      "",
      "green",
      """
         There's a logo on the side of the rocket.
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
3: [
      """
         What is the name of the organization that Linus Torvalds works for?
      """,
      "The Linus Foundation",
      "Linaro",
      "something else",
      "both",
      """
         Linus is employed by the <u>Linux Foundation</u><br>
         <i>Not the Linu<u>s</u> Foundation!</i>
      """
   ],
}
