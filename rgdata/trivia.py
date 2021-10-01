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
#
# any bare percents need to be escaped '%' -> '%%'
# 
# single quotes are escaped.  This is not needed inside """ blocks
# by python, but vim doesn't handle it and if not escaped it messes
# up vim's syntax highlighting.
#
#

tdata = {
1: [
      """
          [Warmup question] The currently released version of Linux is:?
          <br>
          <img src="%(image_url)s/tux.png" height="100">
      """,

"v5.15-rc5",
"v5.14.8",
"",
"red",
"""

<p>
Release candidates aren\'t "released" kernels.  It says right in
their name that they are 'candidates', not actual releases yet. 
Besides - the current rc kernel is 5.15-rc3, not 5.15-rc5.
""",
],

2: [
"""
A group of academic security researchers got in trouble this past year for:
<p>
<img src="%(image_url)s/black-hat.jpeg" height="120">
""",
"Submitting patches with intentional security bugs to the Linux kernel",
"Publicly announcing kernel security flaws, without first notifying kernel developers",
"",
"green",
"""
Researchers from the University of Minnesota submitted some patches
that contained known flaws to a few mailing lists.  Their stated intention
was not to introduce bugs, but rather to test kernel security review practices.
However, this caused great consternation.  All previous patches from
U of MN were reviewed, and the researchers apologized.
<p>
Source:
https://www.theverge.com/2021/4/30/22410164/linux-kernel-university-of-minnesota-banned-open-source</a>
""",
],

3: [
"""
How many Embedded Linux Conferences have there been?
<img align="center" src="%(image_url)s/elc-logo.jpeg" height="100">
""",

"16",
"30",
"",
"red",
"""
<p>
<table><tr><td width="50%%">
There have been 30, counting Embedded Linux Conference Europe
(and not counting the CELF Worldwide Technical Conference in 2005)
</td><td>&nbsp;&nbsp;</td>
<td>
<img src="%(image_url)s/embeddedlinuxconference.png" height="200">
</td></tr></table>
<p>
Source: https://embeddedlinuxconference.com/
""",
],

4: [
"""
How old was Linus Torvalds when he made the first announcement of Linux?
<img align="center" src="%(image_url)s/linus.png" height="120">
""",
"21 years old",
"24 years old",
"",
"green",
"""

Linus was 21 years old, and a student at the University of Helsinki, in Finland,
when he announced Linux (in 1991).
<p>
Source:
https://en.wikipedia.org/wiki/History_of_Linux#The_creation_of_Linux
""",
],

5: [
"""

How many times has Linux landed on Mars?

<img align="center" src="%(image_url)s/mars.jpg" height="100">
""",
"once",
"14 times",
"more than 14 times",
"both",
"""
There were the following:
<ul>
<li>1 for the Ingenuity helicopter, while it was stowed during the landing
of the Perserverance rover</li>
<li>1 landing of the EDL camera linux (Linux was used for EDL video work)</li>
<li>1 landing of the helicopter base stationx Linux</li>
<li>13 landings from Helicopter flights
</ul>
<img align="center" src="%(image_url)s/perseverance-rover.jpg" height="100">
&nbsp; &nbsp;
<img align="center" src="%(image_url)s/nasa_perseverance_landing_graphic.jpg" height="100">
<img align="center" src="%(image_url)s/ingenuity-helicopter.jpeg" height="100">
&nbsp; &nbsp;
<p>
Source:
https://www.theregister.com/2021/02/23/perseverance_landing_video/
""",
],

6: [
"""
Who wrote the book "The War of the Worlds"?
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
<img align="center" src="%(image_url)s/war-of-the-worlds.jpeg" height="150">

""",
"Edgar Rice Burroughs",
"Jules Verne",
"H.G. Wells",
"both",
"""
<table><tr><td width="50%%">
The War of the Worlds was written betwen 1895 and 1897 by H.G. Wells.  It is
one of the earliest stories to describe a conflict between mankind and an
extraterrestrial race.</td>
<td>
<img align="center" src="%(image_url)s/HG-Wells.jpg" height="100">
</td></tr></table>
<p>
Sources:
<ul>
<li>https://en.wikipedia.org/wiki/The_War_of_the_Worlds
<li>Full Text available at: https://en.wikisource.org/wiki/The_War_of_the_Worlds
</ul>
<p align="center">
<i>Note: One of the rare science fiction books for which copyright has expired!</i>

""",
],

7: [
"""
<table><tr><td width="50%%">
Which of the following companies was victorious in an important lawsuit about
copyright of APIS, that was resolved this year by the US Supreme Court?
</td><td>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
<img align="center" src="%(image_url)s/supreme-court.webp" height="100">
</td></tr><table>
""",
"Oracle",
"Google",
"",
"red",
"""
<img align="center" src="%(image_url)s/google.png" height="70">
<p>
The court ruled that Google's use of the JAVA API constituted "fair use"
under copyright law.
<p>
Source:
https://www.zdnet.com/article/google-beats-oracle-in-biggest-programming-copyright-supreme-court-case-ever/</li>
""",

],

8: [
"""
How many instances of Linux are there now in outer space?
&nbsp; &nbsp; &nbsp;
<img align="center" src="%(image_url)s/space.jpg" height="90">
""",
"less than 100",
"more than 100",
"",
"red",
"""
<table><tr><td width="50%%">
There are actually about 106,000 instance of Linux in outer space - most
of them in the 1607 working Starlink satellites.  Each Starlink satellite uses
66 instances of Linux.
</td><td>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
<img align="center" src="%(image_url)s/starlink.png" height="120">
</td></tr></table>
<p>
Source:
https://en.wikipedia.org/wiki/Starlink
""",
],

9: [
"""
<table><tr><td>
<img align="center" src="%(image_url)s/space.jpg" height="120">
</td><td>&nbsp; &nbsp;
Speaking of space... The Space Needle is:
</td></tr></table>
""",
"the name of a hypothetical space elevator (project) proposed by NASA",
"an observation tower in Seattle, Washington",
"both",
"red",
"""
<table><tr><td>
<img align="center" src="%(image_url)s/Space_Needle.jpg" height="120">
</td><td>&nbsp;&nbsp;</td><td>
NASA has studied space elevators, but has no project named "Space Needle".
The most serious study of space elevators appears to
have been the NIAC (NASA Institute for Advanced Concepts)
Phase 2 report from 2003. In that report,
the space elevators were called ... "space elevators".
</td></tr></table>
<p>
Source:
http://www.niac.usra.edu/files/studies/final_report/521Edwards.pdf
""",
],

10: [
"""
How old is the Space Needle?
&nbsp; &nbsp; &nbsp;
<img align="center" src="%(image_url)s/Space_Needle.jpg" height="120">
""",
"less than 50 years old",
"more than 50 years old",
"",
"red",
"""
It was originally built in April, 1962 for the world's fair that year
in Seattle, making it currently 59 years old.<br>
I visited it in the early 1970s, when I was 10 years old.
<p>
When it was built, it was the tallest structure in the US west of the
Mississippi river.
<p>
Source:
https://en.wikipedia.org/wiki/Space_Needle
""",
],

11: [
"""
<table><tr><td>
<img align="center" src="%(image_url)s/laser.jpeg" height="150">
<td><td>&nbsp; &nbsp; &nbsp;</td><td>
Scientist recently demonstrate two ways to create truly random numbers
extremely quickly using a laser.<br>
Which solution produced data more quickly:
</td></tr></table>
""",
"a laser reflecting with itself in an special micro-cavity",
"a laser interacting with the quantum vacuum state",
"",
"green",
"""
<table><tr><td width="60%%">
Both of these were demonstrated this year.  The laser reflecting in a
micro-cavity produced random numbers at a rate of 250 terabytes per second.
The 'quantum vacuum' solution was susceptible to external noise, which could
de-randomize the output, that had to be removed in post-processing.
It "only" produced about 19 gigabits of random data per second.
</td><td>
&nbsp;&nbsp;
<img src="%(image_url)s/laser-hourglass-random-numbers.jpg" height="150">
</td></tr></table>
<p>
Sources:
<ul>
<li>https://phys.org/news/2021-02-scientists-laser-random-ultrafast.html
<li>https://physicsworld.com/a/fast-quantum-random-number-generator-fits-on-a-fingertip/
</ul>
<p align="center">
<i>That's more random data than you can shake a stick at.</i>
""",
],

12: [
"""
PREEMPT_RT has finally been fully merged into the mainstream Linux kernel!
&nbsp; &nbsp; &nbsp;
<img align="center" src="%(image_url)s/stopwatch.jfif" height="100">

""",
"True",
"False",
"",
"red",
"""
<table><tr><td>
<img align="center" src="%(image_url)s/shark-with-laser.jpg" height="100">
</td><td>&nbsp;&nbsp;</td><td>
Significant parts of the PREEMPT_RT patch were merged in the 5.13 and 5.15
kernels, but there are still some parts remaining:  175 patches, affecting
215 files, 1350+ 2650- lines.  A few items, including some things
related to cpu_chill() and NOHZ remain.
</td></tr></table>
<p>
Sources:
https://marketresearchtelecast.com/linux-central-real-time-patches-integrated-after-17-years/161932
<p align="center">
Note: <i>While researching this, I found articles announcing
that PREEMPT_RT was close to being fully mainlined in
 2015, 2017 2019, 2020, and 2021.</i>
""",
],

13: [
"""
printk() has been changed in the 5.15 Linux kernel with the ability to:
""",
"automatically translate messages into other languages besides English",
"get a list of all printk message strings included in the kernel",
"",
"red",
"""
The feature, called 'printk indexing' allows checking that kernel
messages that are detected by diagnostics tools are still present,
despite kernel code changes.

<p>
Source:
https://lwn.net/Articles/857148/
""",
],

14: [
"""
The 5.15 kernel now uses the -Werror flag by default.
The intended effect is that:

""",
"any compiler warning is converted into an error that will halt the build",
"certain errors (specified in a special variable) can now be ignored as warnings",
"",
"green",
"""
As one comentator put it:
<p>
<i>"YAY! One fewer way for stars to align wrong and maintainers to screw up."</i>
<p>
Source:
"The rest of the 5.15 merge window" - https://lwn.net/Articles/868221/
<p align="center">
<i>I warned you this would happen!</i>
""",
],

15: [
"""
How many private, all non-professional missions to outer space have there
been, ever?
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
<img align="center" src="%(image_url)s/private-astronauts.jpeg" height="120">
""",
"one",
"two",
"three",
"red",
"""
<img align="center" src="%(image_url)s/inspiration4.jpeg" height="80">
They are the Inspiration4 mission and the Blue Origin sub-orbital flight.
<img align="center" src="%(image_url)s/blue-origin.jpeg" height="80">
<p>
<ul>
<table bgcolor="#d0d0ff" border="1"><tr><td>attribute/mission</td>
<td>Inspiration 4 (Spacex)</td>
<td>Virign Galactic</td>
<td>Blue Original</td>
<td>other missions</td>
</tr>
<tr><td>privately funded</td>
<td align="center">yes</td><td align="center">yes</td><td align="center">yes</td><td align="center">some, partially</td>
</tr>
<tr><td>all non-professionals</td>
<td align="center">yes</td><td align="center">no*</td><td align="center">yes</td><td align="center">no</td>
</tr>
<tr><td>orbital</td>
<td align="center">yes</td><td align="center">no</td><td align="center">no</td><td align="center">many</td>
</tr>
<tr><td>to ISS</td>
<td align="center">no</td><td align="center">no</td><td align="center">no</td><td align="center">most</td>
</tr></table>
</ul>
<p>
* The Virgin Galactic sub-orbital flight had a professional pilot.

<p align="center">
<i>I, for one, welcome our new amatuer astronaut opportunities.</i>
""",
],

16: [
"""
During the landing sequence for the Inspiration4 private space mission,
one of the crew members is shown watching which "in-flight" movie?
<p>
""",
"Star Wars",
"Alien",
"Spaceballs",
"both",
"""
<table><tr><td>
You can see Spaceballs playing on Chris Sembroski's tablet during the
landing video.
</td><td>
<img src="%(image_url)s/Inspiration4-spaceballs2-during-landing.png" height="180">
</td></tr></table>
<p>

Source:
This youtube video of the landing: https://youtu.be/dpFKNNl47AM?t=789
<p align="center">
<i>I don't always go to space, but when I do, I watch "Spaceballs"</i>
""",
],

17: [
"""
<table><tr><td valign="middle">
<ul>
  <li>How old is Tux now?
</ul>
</td><td>
<img src="%(image_url)s/tux.png" height="200">
</td></tr></table>

""",
"30 years old",
"25 years old",
"20 years old",
"red",
"""

Tux was announced by Linus Torvalds in 1996
<p>
Source:
https://en.wikipedia.org/wiki/History_of_Linux#Official_mascot
""",
],

18: [
"""
New technology has been refined (pun intended) that can power a
bus from garbage.  It uses:
<p>

""",
"human waste (poo and pee)",
"banana peels and beer",
"",
"green",
"""
<table><tr><td>
<img src="%(image_url)s/bio-bus.jpeg" width="300">
</td><td>&nbsp;&nbsp;</td><td>
Recent work by the University of Bristol's Robotics Laboratory,
has taken existing Microbial Fuel Cells technology and
minituarized it to demonstrate MFCs that are smaller than
a AA battery, with similar performance.  (The MFCs powering the bus
are bigger.)
</td></tr></table>
<p>
The 'banana peels and beer' is from a scene where Doc Brown is filling
a "Mr. Fusion" device in the movie "Back to the Future".

<p>
Source:
https://robohub.org/robot-stomachs-powering-machines-with-garbage-and-pee/
<p align="center">
<i>Important Note: "Mr. Fusion" is a fictional device.</i>
""",
],

19: [
"""
<table><tr><td width="70%%">
A record size for chip feature density was announced in May
by IBM.<br>
The feature density was described as:
</td><td>
<img align="center" src="%(image_url)s/ibm-chip.jpeg" height="100">
</td></tr></table>
""",
"4 nanometers",
"2 nanometers",
"",
"red",
"""
<table><tr><td>
<img src="%(image_url)s/IBM-2NM-chip.png" height="180">
</td><td>&nbsp;&nbsp;</td><td>
Individual physical elements on the chip are larger than 2 nanometers, but
due to 3-D stacking the effective density of a demonstration wafer
had about 333 million transistors per square millimeter.
</td></tr></table>
<p>
Source:
https://www.anandtech.com/show/16656/ibm-creates-first-2nm-chip
<p align="center">
<i>What will those crazy scientists thing of next!!</i>

""",
],

20: [
"""
What major phone vendor has announced a program to "upcycle" old phones
into useful IOT devices:
""",
"Samsung",
"Apple",
"Sony",
"green",
"""
<table><tr><td>
<img align="center" src="%(image_url)s/galaxy-upcycling.jpeg" height="120">
</td><td>&nbsp;&nbsp;</td><td>
Samsung is releasing special firmware updates for old Galaxy phones that
turn them into smart home devices such as a childcare monitor,
a pet care solution, or a light sensor (for home automation control).
</td></tr></table>
<p>
Source:
https://www.zdnet.com/article/samsung-launches-software-update-to-turn-older-galaxy-phones-into-iot-devices/
<p align="center">
<i>Another win for embedded Linux!</i>
""",
],

21: [
"""
What large tech company is headquartered in Seattle?
&nbsp; &nbsp; &nbsp;
<img align="center" src="%(image_url)s/seattle.jpeg" height="120">
""",
"Amazon",
"Microsoft",
"",
"green",
"""
<table><tr><td>
<img src="%(image_url)s/amazon-spheres.jpeg" height="120">
</td><td>&nbsp;&nbsp;</td><td>
Amazon's headquarters are in downtown Seattle.
</td></tr></table>
<p>
Microsoft's headquarters are in Redmond Washington, about 12 miles away
<p>
Source:
https://en.wikipedia.org/wiki/Amazon_(company)
<p align="center">
<i>Just a few blocks from where I'm standing! (I think)</i>
""",
],

22: [
"""

<img src="%(image_url)s/beowulf.jpeg" height="100">
What is the Beowulf project?
""",
"The name of a new quantum computer by Google",
"One of the earliest uses of Linux in supercomputer clusters",
"",
"red",
"""
Beowulf was developed by NASA researchers in 1994, to provide supercomputer
performance using commodity hardware.
<p>
Google's quantum computer is named "Sycamore".
<p>
Source:
https://en.wikipedia.org/wiki/Beowulf_cluster
""",

],

23: [
"""
The movie "Free Guy" is about:
""",
"a Non-player character in a video game becoming sentient",
"a government agent who can travel forwards and backwards in time",
"",
"green",
"""
<table><tr><td>
<img src="%(image_url)s/free-guy.jpeg" height="180">
</td><td>&nbsp;&nbsp;</td><td>
Free Guy is a movie staring Ryan Reynolds about an NPC becoming a
true Artificial Intelligence.  It's also a fairly insightful comedy
about the state of modern video games.
</td></tr></table>
<p>
Source:
https://en.wikipedia.org/wiki/Free_Guy
<p align="center">
<i>
""",
],

24: [
"""
<table><tr><td width="50%%">
<img align="center" src="%(image_url)s/old-earth-map.jpeg" height="150">
How many countries has Embedded Linux Conference been in?

""",
"6",
"8",
"",
"red",
"""
As of 2021, Embedded Linux Conference has been held in the following
countries:
Austria, France, Spain, Germany, United Kingdom, Ireland,
the Czech Republic, and the USA.

<p align="center">
<i>We'll return to Europe someday...</i>

""",
],

25: [
"""
The FSF recently blogged about:

""",
"Writing their own version of the DCO (Developer Certificate of Origin)",
"Starting work on version 4 of the GPL license",
"",
"green",
"""
They want something that provides more of the capabilities that copyright
assignment provides, since some projects (notably gcc) have started
accepting DCOs in place of copyright assignment, and the FSF doesn't think
any of the the current industry-standard DCOs are adequate for this.
<p>
Source:
https://www.fsf.org/blogs/licensing/FSF-copyright-handling
<p align="center">
<i>James Bottomley and many others think this is a terrible idea.</i>
""",
],

26: [
"""
Which longstanding kernel interface was removed in 2021, due to security considerations:
""",
"/dev/kmem",
"/proc/sys/kernel",
"",
"green",
"""

/dev/kmem was finally removed, after years of being deprecated, in v5.12
of the Linux kernel.

Source:
<ul>
<li>"Killing off /dev/kmem" - https://lwn.net/Articles/851531/
</ul>
<p align="center">
<i>Hackers are sad that they can't read kernel memory directly anymore.</i>
""",
],

27: [
"""
What epic science fiction trilogy is coming to streaming this fall?

""",
"Dune",
"Foundation",
"both",
"both",
"""

<table><tr><td>
&nbsp;&nbsp;Dune
</td><td>
<img src="%(image_url)s/dune.jpeg" height="120">
</td><td>&nbsp; and Foundation &nbsp;&nbsp;
</td><td>
<img src="%(image_url)s/foundation-movie.jpeg" height="120">
</td></tr></table>

""",
],

28: [
"""
What version of Linux is running in the Mars Helicopter? 
&nbsp;&nbsp;
<img align="center" src="%(image_url)s/ingenuity-helicopter.jpeg" height="100">

""",
"3.4",
"4.15",
"5.13",
"green",
"""

It's a Qualcomm vendor kernel, from the BSP for the dragonboard (from 2014).

""",
],

29: [
"""
What subsystem of the Linux kernel had documentation in the mainline
source repository BEFORE the actual implementation? 

""",
"v4linux",
"selinux",
"ftrace",
"both",
"""

Somehow, the documentation patches for ftrace got integrated one kernel
version before the ftrace implementation code.
<p>
Greg KH was not amused.
<p>

Source: Steven Rostedt

""",
],


}

