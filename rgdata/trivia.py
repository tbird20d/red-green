# trivia data for the red-green game, to be imported by rg.cgi
# each question has a key that is the question number (as a string)
# and value that is a list with the question and answer
#   that is: qdata[question_num][0] = question text
#            qdata[question_num][1] = answer code
#            qdata[question_num][2] = answer text
tdata = {
1: [
      """[warmup question] What is the latest released kernel?
      """,
      "v5.7.6",
      "v5.8-rc5",
      "",
      "green",
      """The latest kernel release on kernel.org is v5.7.6
         <p>
         Release candidates don't count as released kernels.
         It says it right in their names! ('candidates')
         <p>
         Besides - the current release candidate is 5.8-rc3,
         not rc-5!
      """
     ],
2: [
      """In 1968, Edsger Dijstra has a letter published in
         "Communications of the ACM" with the title "Go To Statement
         Considered Harmful."
         <p>
         In 2020, how many goto statements are there in the Linux
         kernel source code (for a recent kernel version)?<br>
         <img src="%(image_url)s/spaghetti-bowl-300x192.jpg">
      """,
      "less than 180,000",
      "greater than 180,000",
      "",
      "green",
      """There are 168764 goto statements in the 5.8-rc2 kernel according to:<br>
         <font size="-1">'find . -name "*.[chS]" | xargs grep "[^_a-z]goto +[a-zA-Z0-9_*;" | grep -v "/[*].*goto" | wc -l'</font>
         <p>
         Some notes:
         <ul>
             <li>Dijkstra did not give his letter the infamous "considered harmful" name.
                 Niklaus Wirth did</li>
             <li>See the paper "gotos considered harmful considered harmful"
                 CACM March 1987 by Frank Rubin for one rebuttal</li>
             <li>Argumens (including by Linus Torvalds) in favor of some uses
                 of gotos: <a href="https://koblents.com/Ches/Linux/Month-Mar-2013/20-Using-Goto-In-Linux-Kernel-Code/">
                 https://koblents.com/Ches/Linux/Month-Mar-2013/20-Using-Goto-In-Linux-Kernel-Code/</a>
             </li>
         </ul>
      """
     ],
3: [  """The Edsger W. Eijkstra papes and notes from his career are housed in
        Austin, Texas.
        <p>
        <img src="%(image_url)s/Edsger_Wybe_Dijkstra.jpg" height="80">
      """,
      "True",
      "False",
      "",
      "green",
      """Dijkstra's last job was in the computer science department at
         the Universtiy of Texas at Austin."
         <p>
         The online E.W.Dijkstra Archive is here:<br>
         <a href="http://www.cs.utexas.edu/users/EWD">
         http://www.cs.utexas.edu/users/EWD</a>
      """
     ],
4: [ """The warning against lines that are too long for Linux
        source contributions was recently changed from its old value
        to 120 columns.
     """,
      "True",
      "False",
      "",
      "red",
      """Checkpatch.pl was modified so the warning occurs at 100
         character line length (not 120).  (It used to be 80)
         <p>
         However:
         <ul>
             <li>80-chars max is still preferred</li>
             <li>See <a href="https://www.phoronix.com/scan.php?page=news_item&px=Linux-Kernel-Deprecates-80-Col">
                 https://www.phoronix.com/scan.php?page=news_item&px=Linux-Kernel-Deprecates-80-Col</a>
             <li>
             <li>Extrapolation from the timing of this change, we should
                 see the limit expanded to 120 chars on March 9, 2049!</li>
         </ul>
      """
     ],
5: [ """In the 4.x series of Linux kernels, was it possible to configure an
         ARM kernel smaller than 700,000 bytes (text, data, and bss)?
     """,
      "Yes",
      "No",
      "",
      "green",
      """According to a presentation at ELC 2017, Michael Opdenacker built a 
         kernel with a footprint of under 600,000 bytes.
         <p>
         Source:<br>
         <a href="https://elinux.org/images/0/07/Opdenacker-embedded-linux-size-reduction-techniques.pdf">
         https://elinux.org/images/0/07/Opdenacker-embedded-linux-size-reduction-techniques.pdf</a> (graph on slide 16)
      """
     ],
6: [ """It is estimated that how many Linux-based computers are currently
        in outer space (counting inter-planetary probes)?
        <p>
         <img src=%(image_url)s/space.jpg height="200" width="500">
     """,
      "less than about 65",
      "more than about 65",
      "",
      "red",
      """There are currently over 32,000 computers in outer space running Linux.
      Each SpaceX launch of Starlink satellites adds another 4000 or so.<br>
      (Each Starlink satellite includes over 60 Linux computers).
      <p>
      It is estimated that in a few years, there will be 2 million Linux
      computers in low earth orbit.
      <p>
      Source:<br>
      FIXTHIS
      <p>
      <i>I propose we call this system "SkyNet" when it is complete.</i>
      """
     ],
7: [ """question
     """,
      "green answer",
      "red answer",
      "",
      "green",
      """answer_text
         <img src=%(image_url)s height="64">
      """
     ],
98: [ """What embedded Linux build system does SpaceX use?
     """,
      "Yocto Project",
      "buildroot",
      "An in-house build system",
      "red",
      """SpaceX uses buildroot.
      <p>
      Source:
      """
     ],
99: [ """question
     """,
      "green answer",
      "red answer",
      "",
      "answer_code [red, green, both]",
      """answer_text
         <img src=%(image_url)s height="64">
      """
     ],
}
