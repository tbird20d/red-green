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
"v5.14.7",
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
<img src="%(image_url)s/mslogo.jpg" height="80">
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
<ul>
<a href="https://www.theverge.com/2021/4/30/22410164/linux-kernel-university-of-minnesota-banned-open-source">
https://www.theverge.com/2021/4/30/22410164/linux-kernel-university-of-minnesota-banned-open-source</a>
</ul>
""",
],

3: [
"""
How many Embedded Linux Conferences have there been?
""",

"16",
"30",
"",
"red",
"""
<p>
There have been 30, counting Embedded Linux Conference Europe
(and not counting the CELF Worldwide Technical Conference in 2005)

Source:
<ul>
<li>https://embeddedlinuxconference.com/
</ul>
""",
],

4: [
"""
How old was Linus Torvalds when he made the first announcement of Linux?
""",
"21 years old",
"24 years old",
"",
"green",
"""

Linus was 21 yeasr old, and a student at the University of Helsinki, in Finland,
when he announced Linux (in 1991).
<p>
Sources:
<ul>
<li>https://en.wikipedia.org/wiki/History_of_Linux#The_creation_of_Linux
</ul>
""",
],

5: [
"""

How many times has Linux landed on Mars?
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
<li>13 landings from Helicopter flights
<li>1 "landing" of the descent stage (Linux was used for EDL video work)</li>
</ul>
<p>
Sources:
<ul>
<li>https://www.theregister.com/2021/02/23/perseverance_landing_video/
</ul>
""",
],

6: [
"""
Who wrote which "War of the Worlds"?
<img align="center" src="%(image_url)s/asimov.jpeg" height="100">

""",
"Edgar Rice Burroughs",
"Jules Verne",
"H.G. Wells",
"both",
"""

<p>
Source:
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
Which of the following companies was victorious in an important lawsuit about
copyright of APIS, that was resolved this year by the US Supreme Court?
""",
"Oracle",
"Google",
"",
"red",
"""
The court ruled that Google's use of the JAVA API constituted "fair use"
under copyright law.
<p>
Source:
<ul>
<li>https://www.zdnet.com/article/google-beats-oracle-in-biggest-programming-copyright-supreme-court-case-ever/</li>
</ul>
""",

],

8: [
"""
How many instances of Linux are there now in outer space?
""",
"less than 100",
"more than 100",
"",
"red",
"""

There are actually about 106,000 instance of Linux in outer space - most
of them in the 1607 working Starlink satellites.  Each Starlink satellite uses
66 instances of Linux.
<p>
Source:
<ul>
<li>https://en.wikipedia.org/wiki/Starlink
</ul>

""",
],

9: [
"""
Speaking of space... The Space Needle is:
""",
"the name of a hypothetical space elevator (project) proposed by NASA",
"an observation tower in Seattle, Washington",
"both",
"red",
"""

NASA has studied space elevators, but has no project named "Space Needle".
The most serious study of space elevators appears to
have been the NIAC (NASA Institute for Advanced Concepts)
Phase 2 report from 2003. In that report,
the space elevators were called ... "space elevators".
<p>
Source:
<ul>
<li>
http://www.niac.usra.edu/files/studies/final_report/521Edwards.pdf
</ul>

""",
],

10: [
"""
How old is the Space Needle?
""",
"less than 50 years old",
"more than 50 years old",
"",
"red",
"""
It was originally built in April, 1962 the 1962 world's fair in Seattle,
making it currently 59 years old.  I visited it when I was 10 years old,
in the early 70s.

When it was built, it was the tallest structure in the US west of the
Mississippi river.

<p>
<img src="%(image_url)s/space_needle.png" height="150">
<p>
Source:
<ul>
<li>
</ul>
<p align="center">

""",
],

11: [
"""
Scientist recently demonstrate two ways to create truly random numbers
extremely quickly using a laser.  Which solution produced data more quickly:
""",
"a laser reflecting with itself in an special micro-cavity",
"a laser interacting with the quantum vacuum state",
"",
"green",
"""
Both of these were demonstrated this year.  The laser reflecting in a
micro-cavity produced random numbers at a rate of 250 terabytes per second.
The 'quantum vacuum' solution was susceptible to external noise, which could
de-randomize the output, that had to be removed in post-processing.
It "only" produced about 19 gigabits of random data per second.
<p>
<img src="%(image_url)s/RNG-laser-micro-cavity.jpg" height="150">
<img src="%(image_url)s/RNG-laser-quantum-vacuum" height="150">
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
""",
"True",
"False",
"",
"red",
"""
Significant parts of the PREEMPT_RT patch were merged in the 5.14 and 5.15
kernels, but there are still some parts remaining:  175 patches, affecting
215 files, 1350+ 2650- lines.  A few items, including some things
related to cpu_chill() and NOHZ remain.

Sources:
<ul>
<li>https://marketresearchtelecast.com/linux-central-real-time-patches-integrated-after-17-years/161932
</ul>

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
<ul>
<li>https://lwn.net/Articles/857148/
</ul>
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
<ul>
<li>"The rest of the 5.15 merge window" - https://lwn.net/Articles/868221/
</ul>

<p align="center">
<i>I warned you this would happen!</i>
<p align="center">

""",
],

15: [
"""
How many private, all non-professional missions to outer space have there
been, ever?
""",
"one",
"two",
"three",
"red",
"""

They are the Inspiration4 mission and the Blue Origin sub-orbital flight.
The Inspiration 4 mission (launched by Spacex) is the only orbital one
<p>
<table><tr><td>mission: -></td>
<td>spaceX (Inspiration 4)</td>
<td>Virign Galactic</td>
<td>Blue Original</td>
<td>other missions</td>
</tr>
<tr><td>privately funded</td>
</td>yes<td>
</td>yes<td>
</td>yes<td>
</td>some, partially<td>
</tr>
<tr><td>all non-professionals</td>
</td>yes<td>
</td>no*<td>
</td>yes<td>
</td>no<td>
</tr>
<tr><td>orbital</td>
</td>yes<td>
</td>no<td>
</td>no<td>
</td>many<td>
</tr>
<tr><td>to ISS</td>
</td>no<td>
</td>no<td>
</td>no<td>
</td>most<td>
</tr>
<tr><td>to ISS</td>
</td>no<td>
</td>no<td>
</td>no<td>
</td>most<td>
</tr>
</table>
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
You can see Spaceballs playing on Chris Sembroski's tablet during the
landing video.
<p>
<img src="%(image_url)s/inspiration4-spaceballs-movie.png" height="120">
<p>

Source:
<ul>
<li>This youtube video of the landing: https://youtu.be/dpFKNNl47AM?t=789
</ul>

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
<ul>
<li>https://en.wikipedia.org/wiki/History_of_Linux#Official_mascot
</ul>
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
<img src="%(image_url)s/bus-human-waste.jpeg" height="60">
<p>
Recent work by the University of Bristol's Robotics Laboratory,
has taken existing Microbial Fuel Cells technology, and has
minituarized it to demonstrate MFCs that are smaller than
a AA battery, with similar performance.  (The MFCs powering the bus
are bigger.)
<p>
The 'banana peels and beer' is from a scene where Doc Brown is filling
a "Mr. Fusion" device in the movie "Back to the Future".

<p>
Source:
<ul>
<li>
https://robohub.org/robot-stomachs-powering-machines-with-garbage-and-pee/
</ul>

<p align="center">
<i>Important Note: "Mr. Fusion" is a fictional device.</i>
""",
],

19: [
"""
A record size for chip feature density was announced in May
by IBM.  The feature density was described as:

<p>
<img src="%(image_url)s/ibm-2nm-chip.jpeg" height="100">

""",
"4 nanometers",
"2 nanometers",
"",
"red",
"""
Individual physical elements on the chip are larger than 2 nanometers, but
due to 3-D stacking the effective density of a demonstration wafer
had about 333 million transistors per square millimeter.

<p>
Source:
<ul>
<li>
https://www.anandtech.com/show/16656/ibm-creates-first-2nm-chip
</ul>
<p align="center">
<i>What will those crazy scientists thing of next!!</i>

""",
],

20: [
"""

What major phone vendor has announced a program to "upcycle" old phones
into useful IOT devices:

<p>

""",
"Samsung",
"Apple",
"Sony",
"green",
"""

Samsung is releasing special firmware updates for old Galaxy phones that
turn them into smart home devices such as a childcare monitor,
a pet care solution, or a light sensor (for home automation control).
<p>
Source:
<ul>
<li>
https://www.zdnet.com/article/samsung-launches-software-update-to-turn-older-galaxy-phones-into-iot-devices/
</ul>
<p align="center">
<i>Another win for embedded Linux!</i>

""",
],

21: [
"""

What large tech company is headquartered in Seattle?

""",
"Amazon",
"Microsoft",
"",
"green",
"""

Amazon's headquarters are in downtown Seattle.
<p>
<img src="%(image_url)s/amazon-spheres.jpg" height="150">
<p>
Microsoft's headquarters are in Redmond Washington, about 12 miles away
<p>
Sources:
<ul>
<li>
https://en.wikipedia.org/wiki/Amazon_(company)
</ul>
<p align="center">
<i>Just a few blocks from where I'm standing! (I think)</i>
""",
],

22: [
"""
What is the Beowulf project?

<p>
<img src="%(image_url)s/beowulf.png" height="100">

""",
"the name of a new quantum computer by Google",
"one of the earliest uses of Linux in supercomputer clusters",
"",
"red",
"""
Beowulf was developed by NASA researchers in 1994, to provide supercomputer
performance using commodity hardware.
<p>
Google's quantum computer is named "Sycamore".
<p>
Sources:
<ul>
<li>
https://en.wikipedia.org/wiki/Beowulf_cluster
</ul>
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
Free Guy is a movie staring Ryan Reynolds about an NPC becoming a
true Artificial Intelligence.  It's also a fairly insightful comedy
about the state of modern video games.
<p>
<img src="%(image_url)s/free-guy.jpg" height="150">
<p>
<p>
Source:
<ul>
<li>
https://en.wikipedia.org/wiki/Free_Guy
</ul>
<p align="center">
<i>
""",
],

24: [
"""
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
<ul>
<li>https://www.fsf.org/blogs/licensing/FSF-copyright-handling
</ul>
<p align="center">
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
Dune
</td><td>
<img src="%(image_url)s/dune-movie-poster.jpg" height="100">
</td><td>
<font size="+1">&nbsp;&nbsp; <b>Foundation</b> &nbsp;&nbsp;</font>
</td><td>
<img src="%(image_url)s/foundation-image.jpg" height="100">
</td></tr></table>

""",
],
}

