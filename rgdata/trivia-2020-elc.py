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
      """[warmup question] What is the latest released Linux kernel?
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
      """In 1968, Edsger Dijstra had a letter published in
         "Communications of the ACM" with the title "Go To Statement
         Considered Harmful."
         <p>
         In 2020, how many goto statements are there in the Linux
         kernel source code (for a recent kernel version)?
         <p>
         <img src="%(image_url)s/spaghetti-bowl-high-res-with-wording.jpg" height="120">
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
             <li>Arguments (including by Linus Torvalds) in favor of some uses
                 of gotos: <a href="https://koblents.com/Ches/Linux/Month-Mar-2013/20-Using-Goto-In-Linux-Kernel-Code/">
                 https://koblents.com/Ches/Linux/Month-Mar-2013/20-Using-Goto-In-Linux-Kernel-Code/</a>
             </li>
         </ul>
      """
     ],
3: [  """The papers and notes from Edsger Dijkstra's career are housed in
        Austin, Texas.
        <p>
        <img src="%(image_url)s/Edsger_Wybe_Dijkstra.jpg" height="120">
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
             </li>
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
6: [ """
        Linus said in his keynote session that much work in operating systems
        is based on principles from the 1960's.  What did he mention as one
        technology that might require new ideas in the kernel?
      """,
      "Quantum computing",
      "Artificial Intelligence",
      "",
      "red",
      """
         Linus mentioned AI.
         <p>
         <img src="%(image_url)s/artificial-intelligence-brain-4x3.jpg" height="120">
      """
     ],
7: [ """It is estimated that how many Linux-based computers are currently
        in outer space? (counting inter-planetary probes)
        <p>
         <img src="%(image_url)s/space.jpg" height="180" width="500">
     """,
      "less than about 65",
      "more than about 65",
      "",
      "red",
      """There are currently over <u>32,000</u> computers in outer space running Linux.
      Each SpaceX launch of Starlink satellites adds another 4000 or so.<br>
      (Each Starlink satellite includes over 60 Linux computers).
      <p>
      It is estimated that in a few years, there will be <u>2 million</u> Linux
      computers in low earth orbit.
      <p>
      Sources:<br>
      <ul>
          <li><a href="https://zd.net/30kdr4y">
          htts://zd.net/30kdr4y</a></li>
          <li>Reddit SpaceX Q&A:
          <a href="https://old.reddit.com/r/spacex/comments/gxb7j1/we_are_the_spacex_software_team_ask_us_anything/">
          https://old.reddit.com/r/spacex/comments/gxb7j1/we_are_the_spacex_software_team_ask_us_anything/"</a></li>
      </ul>
      <p>
      <i>I propose we call this system "SkyNet" when it is complete.</i> :-)
      """
     ],
8: [ """It will be hard to use a Nexus 4 Android phone in the year 2040.
     """,
      "True",
      "False",
      "",
      "green",
      """Android in that era was subject to the "year-2038" bug, where
         32-bit UNIX time rolls over.
         <p>
         Luckily, year-2038 problems have mostly been fixed in the kernel,
         due to a lot of hard work by Arnd Bergmann and others.
         <p>
         Sources:
         <ul>
             <li><a href="https://elinux.org/images/6/6e/End_of_Time_--_Embedded_Linux_Conference_2015.pdf">
             https://elinux.org/images/6/6e/End_of_Time_--_Embedded_Linux_Conference_2015.pdf</a> (slide 3)</li>
             <li><a href="https://www.reddit.com/r/Android/comments/16vci0/heh_you_can_crash_android_with_the_2038_unix_bug/">
             https://www.reddit.com/r/Android/comments/16vci0/heh_you_can_crash_android_with_the_2038_unix_bug/</a></li>
        </ul>
      """
     ],
9: [ """The Linux Foundation kernel documentation team recently added
        how many new people?<br>

        <img src="%(image_url)s/batch-books-document-education-357514.jpg" height="100">
     """,
      "less than 2",
      "more than 6",
      "",
      "green",
      """
         The Linux Foundation does not, to my knowledge, have a kernel
         documentation team.
         <p>
         <img src="%(image_url)s/black-and-white-board-boardroom-business-260689.jpg" height="120"><br>
         <font size="-1">The LF kernel doc team</font>
      """
     ],
10: [ """In April, an educational computer kit based on the Raspberry Pi 4
         was released, that was built and marketed by an 11-year old child.
      """,
      "True",
      "False",
      "",
      "red",
      """ The Sania Box embedded computer kit did go on sale recently,
          based on a kickstarter campaign.  But it was designed and is
          being sold by a <u>13-year old</u> young woman from India, named
          Sania Jain.<br>
         <img src="%(image_url)s/Sania-Jain.png" height="120">
         <p>
         <ul>
         <table><tr><td>
             The kit includes a Raspberry Pi 4 board and
             custom shield with multiple sensors, relay, pushbutton,
             LEDs, 7-segment display, and is targeted at the STEM
             education market.
         </td><td>
             <img src="%(image_url)s/Sania-Box.jpg" height="100">
         </td></tr></table>
         </ul>
         <p>
        Sources:<br>
        <a href="http://linuxgizmos.com/teen-launches-raspberry-pi-4-based-stem-kit/">
        http://linuxgizmos.com/teen-launches-raspberry-pi-4-based-stem-kit/</a>
        <p>
        <i>I kind of feel like I wasted my youth, by comparison...</i>
      """
     ],
11: [ """
        "Remember the Alamo"  Unfortunately we will be missing out
         on an opportunity to visit one of the most historic sites of Austin,
         Texas - The Alamo.
         <p>
         <img src="%(image_url)s/1854_Alamo.jpg" height="180">
         <p>
         In what year was the famous "Battle of Alamo" fought in Austin?
      """,
      "1836",
      "1841",
      "Neither of those years",
      "both",
      """
      <table><tr><td>
          The battle of Alamo was fought in 1836, but the Alamo Mission<br>
          is located in San Antonio, Texas, not Austin.
      </td><td>
         <img src="%(image_url)s/texas_1836_julius-300x411.jpg" height="200">
      </td></tr></table>
      """
     ],
12: [ """
        <table><tr><td>
           <img src="%(image_url)s/ossna-levin-sm.jpg" height="120">
        </td><td>
         What is the best (recent) evidence that Sasha Levin and<br>
         Greg Kroah-Hartmann have lost their minds?
        </td><td>
           <img src="%(image_url)s/800px-Greg-Kroah-Hartman.jpg" height="120">
        </td></tr></table>
      """,
      "They wrote a new event notification system for the kernel",
      "They increased the LTS support lifetime",
      "",
      "red",
      """
         <img src="%(image_url)s/kernel.org-lts.PNG" height="150">
         <p>
         There <i>is</i> a new event notification system, but that
         was added by David Howells.  Greg and Sasha have increased
         the support timeframe for 2 more LTS kernels from 2 years to 6
         years!!.  I really don't know how they do it.
      """
     ],
13: [ """What was the first commercial embedded Linux distribution?
      """,
      "MontaVista Hard Hat Linux",
      "Timesys Linux",
      "Lineo Embedix",
      "both",
      """Here are the release dates for each system:
      <ul>
          <li>Lineo Embedix 1.0 - January 24, 2000</li>
          <li>MontaVista Hard Hat Linux 1.0 - January 31, 2000</li>
          <li>Timesys Linux/RT 1.0 - May 16, 2000</li>
      </ul>
      <p>
      Embedded Linux is effectively 20 years old this year!
      <p>
      <i>I think I'm going to declare this the "Year of
      Embedded Linux".</i>
      """
     ],
14: [ """
         In "The Rise of Skywalker", Rey continues her training under
         which Jedi:
         <p>
         <img src="%(image_url)s/rey-in-training.jpg" height="200">
      """,
      "Leia Organa",
      "Plo Koon",
      "",
      "green",
      """
        Leia trains Rey to become a full-fledges Jedi.<br>
        Also, in some brief footage, we see Leia's own Jedi training with Luke.
        <p>
        <img src="%(image_url)s/leia-jedi-training.jpg" height="120">
        <p>
        <i>Sorry if that was a spoiler for you!</i>
      """
     ],
15: [ """
         The Yocto Project has its roots in the RPM package management system.
         <p>
         <img src="%(image_url)s/rpm.jfif" height="100">
      """,
      "True",
      "False",
      "",
      "red",
      """
         BitBake, the YP build tool, was originally inspired by
         Portage, which is the package management tool use by Gentoo
         Linux (not RedHat).
         <p>
         Source:<br>
         <a href="https://en.wikipedia.org/wiki/BitBake">
         https://en.wikipedia.org/wiki/BitBake</a>
      """
     ],
16: [ """
         BusyBox was initially created for MMU-less systems (uClinux)."
         <p>
         <img src="%(image_url)s/busybox.png" height="100">
      """,
      "True",
      "False",
      "",
      "red",
      """
         BusyBox was created for Debian boot floppies.
         <p>
         Source:<br>
         <a href="https://en.wikipedia.org/wiki/BusyBox">
         https://en.wikipedia.org/wiki/BusyBox</a>
      """
     ],
17: [ """What embedded Linux build system does SpaceX use?
        <p>
         <img src="%(image_url)s/spacex-logo-on-rocket.jfif" height="150">
      """,
      "Yocto Project",
      "Buildroot",
      "An in-house build system",
      "red",
      """
         SpaceX uses buildroot.
         Source:<br>
         <ul>
             <li>Reddit SpaceX Q&A:
             <a href="https://old.reddit.com/r/spacex/comments/gxb7j1/we_are_the_spacex_software_team_ask_us_anything/">
             https://old.reddit.com/r/spacex/comments/gxb7j1/we_are_the_spacex_software_team_ask_us_anything/</a></li>
         </ul>
      """
     ],
18: [ """
         According to the Debian popularity contest,
         what text editor is more popular?
         <p>
         <img src="%(image_url)s/emacs-user.jpg" height="150">
      """,
      "Vim",
      "Emacs",
      "Nano",
      "both",
      """
         <img src="%(image_url)s/vi-emacs-nano.png" height="400">
         <p>
         Source:<br>
         <a href="https://qa.debian.org/popcon-graph.php?packages=vim%%2C+emacs%%2C+nano&show_vote=on&want_percent=on&want_legend=on&want_ticks=on&from_date=2010-01-02&to_date=2020-06-29&hlght_date=&date_fmt=%%25Y-%%25m&beenhere=1">
         https://qa.debian.org/popcon-graph.php?packages=vim%%2C+emacs%%2C+nano&show_vote=on&want_percent=on&want_legend=on&want_ticks=on&from_date=2010-01-02&to_date=2020-06-29&hlght_date=&date_fmt=%%25Y-%%25m&beenhere=1</a>
      """
     ],
19: [ """
         About how many of the "Reported-by" credits for bugfix patches
         in the 5.6 kernel are for automated testing systems?
         <p>
         <img src="%(image_url)s/robot-test.jfif" height="150">
      """,
      "about 20%",
      "about 35%",
      "about 45%",
      "red",
      """
         The top 3 "Reported-by" lines for bugfixes in v5.6 are for
         automated testing systems.
         <p>
         <img src="%(image_url)s/reported-by.png" height="100">
         <p>
         Source:<br>
         <a href="https://lwn.net/Articles/816068/">
         https://lwn.net/Articles/816068/</a>
         <p>
         <i>I, for one, welcome our new automated testing overlords.</i>
      """
     ],
20: [ """
        Which of the following is NOT running the Linux kernel?
        <p>
        <table><tr><td>
            <img src="%(image_url)s/mars-rover.jpg" height="120">
         </td><td width="50px">&nbsp;>
         </td><td>
            <img src="%(image_url)s/submarine.jfif" height="120">
         </td><td width="50px">&nbsp;>
         </td><td>
            <img src="%(image_url)s/LHC.jfif" height="120">
         </td></tr></table>
      """,
      "Mars Opportunity Rover",
      "US Nuclear submarines",
      "Large Hadron Collider",
      "green",
      """
         The rover runs VxWorks.
         <p>
         <img src="%(image_url)s/mars-rover.jpg" height="120">
         <p>
         Sources:
         <ul>
             <li><a href="https://www.linuxjournal.com/article/7789">
             https://www.linuxjournal.com/article/7789</a></li>
             <li><a href="https://www.omgubuntu.co.uk/2016/08/25-awesome-unexpected-things-powered-linux">
             https://www.omgubuntu.co.uk/2016/08/25-awesome-unexpected-things-powered-linux</a></li>
             <li><a href="https://www.computerworld.com/article/2563630/mars-rovers-get-long-distance-os-updates.html">
             https://www.computerworld.com/article/2563630/mars-rovers-get-long-distance-os-updates.html</a></li>
         </ul>
      """
     ],
21: [ """
        A significant security exploit in the "spectre" family is called
        what?
        <p>
         <img src="%(image_url)s/zombie-hand.jfif" height="100">
      """,
      "Zombieland",
      "Zombieload Attack",
      "",
      "red",
      """
         Zombieland is a movie.
         <table><tr><td>
           <img src="%(image_url)s/zombieload.jpg" height="100">
         </td><td><font size="+1">&nbsp;&nbsp;<b>is not</b>&nbsp;&nbsp;</font>
         </td><td>
         <img src="%(image_url)s/zombieland.jpg" height="100">
         </td></tr></table>
      """
     ],
22: [ """
        Can the Linux scheduler can take into account the thermal status of a
        processor?
        <p>
         <img src="%(image_url)s/hot-cpu.jfif" height="100">
      """,
      "Yes",
      "No",
      "",
      "green",
      """
         As of kernel v5.7, there is a new "Thermal Pressure" API
         and thermal governors in the kernel, which can help shift
         processing from overheated CPUs.
         <p>
         Source:<br>
         <a href="https://lwn.net/Articles/7888380">
         https://lwn.net/Articles/7888380</a>
      """
     ],
23: [ """
        After 13 long years out-of-tree, the PREEMPT_RT patch set is now
        poised to be accepted into mainline.  The initial kconfig entry
        has already been accepted.
        <p>
        <img src="%(image_url)s/stopwatch.jfif" height="100">
      """,
      "True",
      "False",
      "",
      "green",
      """
         The kconfig entry for PREEMPT_RT was added in the 5.3 kernel.
         See kernel/Kconfig.preempt.
         <p>
         <img src="%(image_url)s/shark-with-laser.jpg" height="200">
      """
     ],
24: [ """
        Despite being bitten by a penguin, Linus Torvalds likes penguins.
        <p>
        <img src="%(image_url)s/penguin-suspects.jpg" height="200">

      """,
      "True",
      "False",
      "",
      "green",
      """
         Linux was bitten by a penguin in 1993 while in Australia for a
         speaking engagement.  But he's OK with them now.
         <p>
         <img src="%(image_url)s/celf-tux.png" height="100">
         <p>
         Source:<br>
         <a href="https://fossbytes.com/why-is-the-penguin-tux-the-official-mascot-of-linux-because-torvalds-had-penguinitis">
         https://fossbytes.com/why-is-the-penguin-tux-the-official-mascot-of-linux-because-torvalds-had-penguinitis</a>
      """
     ],
25: [ """
         What was Linux was first called?
         <p>
         <img src="%(image_url)s/linus.png" height="200">
      """,
      "Linus' Unix",
      "Freax",
      "",
      "red",
      """
         Yeah. Really.
         <p>
         Source:<br>
         <a href="https://en.wikipedia.org/wiki/History_of_Linux">
         https://en.wikipedia.org/wiki/History_of_Linux</a>
         <p>
         <i>And to think, we could have had an "Embedded Freax Conference"</i>
      """
     ],
26: [ """
         Which of the following quotes did Rusty Russel have in his e-mail
         signature?
      """,
      """ "There are those who do and those who hang on and you don't<br>
      see too many doers quoting their contemporaries. -- Larry McVoy" """,
      '"Anyone who quotes me in their sig is an idiot. -- Rusty Russell"',
      "",
      "green|red",
      """
         Both answers are acceptable.  Rusty has had both of these as his
         signatures at different times.
      """
     ],
27: [ """
        What noted science fiction author created the 3 laws of robotics?
        <p>
        <img src="%(image_url)s/robot.jfif" height="250">
      """,
      "Arthur C. Clark",
      "Isaac Asimov",
      "John W. Campbell",
      "red|both",
      """
         Issac Asimov attributed the Three Laws to John W. Campbell, from
         a conversation that took place on 23 December, 1940.  But I can't
         in good conscience exclude Asimov from the answer.
         <p>
         Source:<br>
         <a href="https://en.wikipedia.org/wiki/Three_Laws_of_Robotics">
         https://en.wikipedia.org/wiki/Three_Laws_of_Robotics</a>
      """
     ],
28: [ """
        Microsoft has begun shipping the Linux kernel to many of their
        Windows customers.
        <p>
        <img src="%(image_url)s/mslogo.jpg" height="120">
      """,
      "True",
      "False",
      "",
      "green",
      """
         Microsofts' Windows Subsystem for Linux (WSL) version 2
         includes a "real" Linux kernel, and can be used to run
         Linux apps on Windows 10.
         <p>
         Source:<br>
         <a href="https://www.howtogeek.com/424886/windows-20s-linux-kernel-is-now-available/">
         https://www.howtogeek.com/424886/windows-20s-linux-kernel-is-now-available/</a>
      """
     ],
29: [ """
        The Linux Foundation has become the home to many open source projects.
        How many LF projects are there currently?
        <p>
        <img src="%(image_url)s/Linux-Foundation_logo.png" height="120">
      """,
      "about 120",
      "about 180",
      "",
      "red",
      """
        It's hard to count, since new projects are created regularly.
        <p>
        There are 177 projects listed here:
        <a href="https://www.linuxfoundation.org/project/directory/">
        https://www.linuxfoundation.org/project/directory/</a><br>
        and there are some I'm aware of that are not listed.
      """
     ],
30: [ """
        On average, how many patches per hour were contributed to the
        Linux 5.7 release?
        <p>
        <img src="%(image_url)s/assembly-line.jfif" height="200">
      """,
      "about 9",
      "about 12",
      "",
      "green",
      """
         The actual patches-per-hour for 5.7 was about 9.2 per hour.
         This was a little less than the max of 9.7 for kernel version 4.9
         <p>
         Source:<br>
         <a href="https://github.com/gregkh/kernel-history/blob/master/kernel_stats.ods">
         https://github.com/gregkh/kernel-history/blob/master/kernel_stats.ods</a>
      """
     ],
31: [ """
        Who has the most code in the Linux kernel?
        <p>
         <img src="%(image_url)s/coder.jfif" height="100">
      """,
      "Linus Torvalds",
      "Alex Duecher",
      "Hawking Zhang",
      "red",
      """
         According to cregit for 5.7, it is Alex. Linus said he doesn't do
         much programming anymore (he's more like a manager), and even these
         stats for pre-git probably include lots of source from other
         people.
         <p>
         <img src="%(image_url)s/authors-cregit.PNG" height="100">
         <p>
         Source:<br>
         <a href="https://cregit.linuxsources.org/code/5.7/">
         https://cregit.linuxsources.org/code/5.7/</a>

      """
     ],
}
