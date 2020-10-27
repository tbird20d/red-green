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
# todo:
#  - replace '' with '
#

tdata = {
1: [
      """
          [Warmup question] What is the latest official Linux kernel?
      """,

"v5.9.3",
"v5.10-rc1",
"",
"red",
"""

The latest official kernel available is the latest release candidate
from Linus Torvalds.
<p>
Release candidates aren''t  "released" kernels, but they are official.
Besides - the current release kernel is 5.9.1, not 5.9.4
""",
],

2: [
"""
Microsoft has begun shipping the Linux kernel to many of their
Windows customers.
""",
"True",
"False",
"",
"green",
"""
Microsoft's Windows Subsystem for Linux (WSL) version 2 includes a "real",
Linux kernel, and can be used to run Linux apps on Windows 10.
<p>
Source:
<ul>
<li>https://www.howtogeek.com/424886/windows-10s-linux-kernel-is-now-available/
</ul>
""",
],

3: [
"""
The famous Book of Kells is an "Illuminated Manuscript" created in the
9th century.  Where can you view it today?
""",

"Abbey of Kells",
"Trinity College Library",
"National Museum of Ireland",
"red",
"""


The Book of Kells is famous for its elaborate artwork, and is
considered one of Ireland''s greatest cultural treasures.
<p>
Source:
<ul>
<li>https://www.tcd.ie/visitors/book-of-kells/
</ul>
""",
],

4: [
"""
There has been work recently to remove what obnoxious code
pattern from the Linux kernel?

""",
"comma separated statements (e.g. a=1,b=2;)",
"variable length arrays (u8 s[bsize * 2];)",
"",
"green",
"""

In August 2020, some coccinelle scripts were written to find examples
of these, and a set of patches produced to try to eliminate these from
the kernel.  For the record, VLAs were eliminated in 2018 (making them
old news)
<p>
Sources:
<ul>
<li>https://lore.kernel.org/lkml/alpine.DEB.2.22.394.2008201856110.2524@hadrien/
<li>https://www.phoronix.com/scan.php?page=news_item&px=Linux-Kills-The-VLA
</ul>
""",
],

5: [
"""
What noted science fiction author created the 3 laws of robotics?
""",
"Arthur C. Clark",
"Isaac Asimov",
"John W. Campbell",
"red|both",
"""

Isaac Asimov attributed the Three Laws to John W. Campbell, from a
conversation that took place on 23 December, 1940.  But I can''t in
good conscience exclude Asimov from the answer.
<p>
Source:
<ul>
<li>https://en.wikipedia.org/wiki/Three_Laws_of_Robotics
</ul>

""",
],

6: [
"""

Isaac Asimov wrote which epic science fiction series of novels?

""",
"Dune",
"Foundation",
"",
"red",
"""

The Foundation series describes the fall of the galactic empire.
Frank Herber wrote Dune.  Both series will be available in video form
in 2021!
<p>
Source:
<ul>
<li>https://en.wikipedia.org/wiki/Foundation_(TV_series)
</ul>

""",
],

7: [
"""

The 5.8 kernel consists of 69,325 files and 28442673 lines of code.
How many files were in the first release of Linux in 1991?

""",
"37 files",
"88 files",
"",
"red",
"""
The first release of Linux had 88 files.
<p>
Source:
<ul>
<li>2020 Kernel History Report:
https://www.linuxfoundation.org/wp-content/uploads/2020/08/2020_kernel_history_report_082720.pdf
</ul>
""",

],

8: [
"""

Scientists recently demonstrated a device that harvests usable
electricity from "Brownian current" at room temperature, with no
moving parts and no heat transfer.

""",
"True",
"False",
"",
"green",
"""

In a demonstration of "stochastic thermodynamics", the
scientists use one-way diodes and the ripple of Brownian current in
graphene to produce an electrical charge capable of putting a load on
a resistor.
<p>


Source:
<ul>
<li>https://phys.org/news/2020-10-physicists-circuit-limitless-power-graphene.html
</ul>

""",
],

9: [
"""
How many emails were sent to the Linux Kernel Mailing List (LKML) in 2019?

""",
"more than 400,000",
"less than 400,000",
"",
"red",
"""

There were "only" about 350,000 emails on LKML for the calendar year 2019.
<p>

Source:
<ul>
<li>2020 Kernel History Report:
https://www.linuxfoundation.org/wp-content/uploads/2020/08/2020_kernel_history_report_082720.pdf
</ul>

""",
],

10: [
"""

What is the official name of the character that "The
Mandalorian" protects?

""",
"Baby Yoda",
"The Child",
"Kuill",
"red",
"""

Although fans named the character "Baby Yoda", the child is never
referred to by that name in the series.
<p>
Source:
<ul>
<li>https://www.starwars.com/news/quiz-how-well-do-you-know-the-mandalorian-season-one
</ul>

""",
],

11: [
"""

In a computing breakthrough, a group of scientists recently
constructed a half-adder computer circuit using only 3 nanowires,
rather than transistors.  The circuit uses about 1/10th the power of
one using electrons.
<p>
What is the name of the quantum item that the circuit uses to carry signals?

""",
"Phonon",
"Magnon",
"",
"red",
"""

A magnon is a quasi-particle, and is a quanta of spin-wave. The waves
are formed by distortions in the magnetic order of a solid material on
the quantum level.
<p>


Source:
<ul>
<li>https://techxplore.com/news/2020-10-circuit-pure-magnons.html
</ul>
""",
],

12: [
"""
What is the closest that Linux has gotten to the planet Mars?

""",
"0 kilometers (on the surface)",
"250 kilometers",
"7.4 million kilometers",
"red",
"""

Cubesats running Linux deployed in low Mars orbit in November of 2018.
A Tesla car (running Linux?) has an orbit that occasionally gets close
to Mars.  It recently passed within 8 million kilometers of the
planet.
<p>
None of the Mars landers have incorporated Linux.
<p>

Sources:
<ul>
<li>http://linuxgizmos.com/cubesats-that-confirmed-mars-insight-landing-feature-embedded-linux-com/
<li>https://www.livescience.com/starman-tesla-mars-approach.html
</ul>

""",
],

13: [
"""

In 2019, there were over 4,200 contributors to the Linux kernel.  In
what year did the number of contributors first surpass 1000?

""",
"2005",
"2010",
"",
"green",
"""

The total number of contributors to the Linux kernel since 1991 is
over 15,000, with about 4000 developer participating in each
individual release
<p>
Source:
<ul>
<li>2020 Kernel History Report:
https://www.linuxfoundation.org/wp-content/uploads/2020/08/2020_kernel_history_report_082720.pdf
</ul>
""",
],

14: [
"""

The movie Tenet incorporates elements from which of these ancient
puzzle devices?

""",
"the Sator square",
"the Scriptum cube",
"the Antikythera mechanism",
"green",
"""

All of the words of the Sator square are used in the movie.  The
square can be read  forwards and backwards, which ties in with the
theme of the movie.

""",
],

15: [
"""

What language, besides C and assembly, has recently been discussed as
being possibly supported for kernel development?

""",
"Go",
"Rust",
"C++",
"red",
"""

Linus said that kernel developers are looking at having interfaces so
that a driver could be written in Rust.  The kernel core would
continue to only allow C and assembly.
<p>
Source
<ul>
<li>https://www.theregister.com/2020/06/30/hard_to_find_linux_maintainers_says_torvalds/
<li>https://lwn.net/Articles/829858/
</ul>
""",
],

16: [
"""

The Civil Infrastructure Platform intends to maintain their Super Long
Term Support Linux kernel for how many years?

""",
"10 years",
"20 years",
"",
"green",
"""

The CIP project currently plans 10 years of support. However, there is
talk of needing to maintain some kernels deployed in civil
infrastructure for up to 50 years.
<p>

Source:
<ul>
<li>https://www.cip-project.org/wp-content/uploads/sites/17/2018/10/CIP_Whitepaper_10.19.18.pdf
<li>Upstream first is our principle - session at ELCE
https://static.sched.com/hosted_files/osseu2020/4e/Oct26_UpstreamFirstIsOurPrincipleTowardSuperLongTermSupport.pdf
</ul>
""",
],

17: [
"""
The original RoboCop used what operating system?

""",
"DOS",
"Amiga OS",
"",
"green",
"""

As can be seen in the 1987 movie, the boot sequence includes
command.com, config.sys, and other DOS-related files.
<p>
Source:
<ul>
<li>	This screenshot:
</ul>
""",
],

18: [
"""
When is the millionth commit expected to be accepted into the Linux kernel?

""",
"before March 2021 ",
"after March 2021",
"",
"green",
"""

It already happened, in August of 2020
<p>
Source:
<ul>
<li> https://www.zdnet.com/article/commit-1-million-the-history-of-the-linux-kernel/
</ul>

""",
],

19: [
"""

In September it was announced that ARM Holdings was set to be acquired
by what company?

""",
"SoftBank",
"NVidia",
"",
"red",
"""
NVidia has offered to acquire ARM Holdings <i>from</i> SoftBank
for $40 billion.
<p>
Source
<ul>
<li>https://arstechnica.com/gadgets/2020/09/nvidia-reportedly-to-acquire-arm-holdings-from-softbank-for-40-billion/
</ul>
""",
],

20: [
"""

After many years of mostly-successful fundraising, in 2020 Wikipedia
broke down and accepted government funding, under strict policy that
it not interfere with editorial decision-making.

""",
"True",
"False",
"",
"red",
"""

Wikipedia still does not accept government funding.  However, several
companies have matching gifts programs that donate substantial support
to the Wikimedia foundation.  Also, they did announce some changes to
their page design coming in the near future (before their 20th
anniversary in 2021).
<p>
Source
<ul>
<li>https://diff.wikimedia.org/2020/09/23/wikipedia-is-getting-a-new-look-for-the-first-time-in-10-years-heres-why/
</ul>

""",
],

21: [
"""

Google has announced a new thing that seems pertinent to our times.
Which is it?

""",
"A new device that will automatically record audio and video and notify your emergency contacts, if you are involved in a traffic stop",
"A service to stay on hold and alert you when a live operator comes on a telephone call",
"",
"red",
"""

Google''s service is called "Hold for Me".  Amazon is releasing a
product called the Ring Dash Cam, which has a "Traffic Stop",
feature as described.
<p>
Sources:
<ul>
<li>https://www.theverge.com/2020/9/25/21454772/amazon-ring-car-cam-traffic-stop-police-accountability
<li>https://techcrunch.com/2020/09/30/a-new-google-assistant-feature-hold-for-me-waits-on-hold-so-you-dont-have-to/
</ul>
""",
],

22: [
"""

A glasses-free "holographic" display, which uses eye tracking
and the Unreal game engine to present a 3-dimensional view to the
user, just came on the market.

""",
"True",
"False",
"",
"green",
"""

The Sony "Spatial Reality Display" costs $5000, and is targeted at
industrial and commercial designer.  It does both parallax and
occlusion based on eye position, and shows different images for each
eye using a lenticular display.
<p>

Sources:
<ul>
<li>https://www.theverge.com/circuitbreaker/2020/10/15/21518679/sony-spacial-reality-display-hands-on-holographic-elf-sr1
<li>https://www.engadget.com/sony-spatial-reality-display-3d-glasses-free-010029316.html
</ul>
""",

],

23: [
"""

Microsoft has announced plans to allow users to convert their Windows
System for Linux into a standalone product capable of running Windows
applications. This product would still require a Windows license by
the consumer.

""",
"True",
"False",
"",
"red",
"""

There have recently been stories that Microsoft would base future
versions of Windows on Linux, but they are currently just speculation.
<p>
Source:
<ul>
<li>https://www.computerworld.com/article/3438856/call-me-crazy-but-windows-11-could-run-on-linux.html
</ul>
""",
],

24: [
"""

Which Sith Lord said: "I am altering the deal. Pray I don''t alter it
any further"?

""",
"Darth Vader",
"Darth Sidious",
"",
"green",
"""

Darth Vader breaks his word to Lando Calrisian about letting Princess
Leia and Wookie stay in cloud city under Lando''s supervision.

""",
],

25: [
"""
How old is the Yocto Project?

""",
"10 years old",
"12 years old",
"",
"green",
"""

The official announcement of the Yocto Project was made at ELC Europe
in Cambridge, UK in October of 2010.
<p>


Source:
<ul>
<li>Tim Bird - I was there
<li>Also, it was announced in this ELCE''s keynote address on Monday
</ul>
	
""",
],

26: [
"""
Who has the most code in the linux kernel?
""",
"Linus Torvalds",
"Alex Duecher",
"Hawking Zhang",
"red",
"""

According to cregit for 5.7, it is Alex.  Linus said he doesn''t do
much programming anymore (he''s more like a manager), and even these
stats for pre-git probably include lots of source from other people.
<p>

Source:
<ul>
<li>https://cregit.linuxsources.org/code/5.7/
</ul>

""",
],

27: [
"""

A significant security exploit in the "spectre" family is called what?

""",
"Zombieland",
"Zombieload Attack",
"",
"red",
"""

ZombieLand is a movie

""",
],

28: [
"""
One of the interesting features of the Dublin Convention Center is:

""",
"The facility has breakout rooms can be rotated into the main keynote auditorium",
"The conference center was the first carbon-neutral constructed event center in the world",
"",
"red",
"""

The conference center was built with sustainability in mind and is
very energy efficient.  Low-carbon cement was used during its
construction, and carbon offsets were purchased for all unavoidable
carbon use.  The conference center in Edinburgh Scotland has rotating
breakout rooms.
<p>
Source:
<ul>
<li> https://www.theccd.ie/news?i=188
</ul>
""",
],

29: [
"""

Can the Linux scheduler can take into account the thermal status of a
processor?

""",

"Yes",
"No",
"",
"green",
"""

As of kernel v5.7, there is a new "Thermal Pressure" API and
thermal governors in the kernel, which can help shift processing from
overheated CPUs.
<p>
Source:
<ul>
<li>http://lwn.net/Articles/788380
</ul>

""",
],

30: [
""" 

After 13 long years out-of-tree, the PREEMPT_RT patch set is now
poised to be accepted into mainline.  The initial kconfig entry has
already been accepted.

""",

"True",
"False",
"",
"green",
"""

The kconfig entry for PREEMPT_RT was added in the 5.3 kernel.  See
kernel/Kconfig.preempt.

""",
],

31: [
"""

Despite being bitten by a penguin, Linus Torvalds likes penguins. 

""",
"True",
"False",
"",
"green",
"""

Linus was bitten by a penguin
in 1993 while in Australia for a
speaking engagement.  But he''s OK with them now.
<p>
Source:
<ul>
<li>https://fossbytes.com/why-is-the-penguin-tux-the-official-mascot-of-linux-because-torvalds-had-penguinitis/
</ul>

""",
],

32: [
"""
Linux was first called:

""",
"Linus'' Unix",
"Freax",
"",
"red",
"""

Yeah.  Really.
<p>
Source:
<ul>
<li>https://en.wikipedia.org/wiki/History_of_Linux
</ul>

""",
],

33: [
"""

Which of the following quotes did Rusty Russel have in his e-mail
signature?

""",
"\"There are those who do and those who hang on and you don''t see too many doers quoting their contemporaries.\" -- Larry McVoy",
"\"Anyone who quotes me in their sig is an idiot.\" -- Rusty Russell",
"",
"red|green",
"""

Both answers are acceptable.  Rusty has had both of these as his
signatures at different times.

""",
],

34: [
"""

The Linux Foundation has become the home to many open source projects.
How many LF projects are there currently?

""",

"about 120",
"about 180",
"",
"red",
"""
It''s hard to count, since new projects are created regularly. 
<p>
There are 177 projects listed here:
https://www.linuxfoundation.org/projects/directory/ and there are some
I''m aware of that are not listed.

""",
],

35: [
"""

On average, how many patches per hour were contributed to the Linux
5.7 release?

""",
"about 9",
"about 12",
"",
"green",
"""

The actual patches-per-hour for 5.7 was: 9.2 per hour.  This was a
little less than the max of 9.7 for kernel version 4.9.
<p>
Source:
<ul>
<li>https://github.com/gregkh/kernel-history/blob/master/kernel_stats.ods
</ul>

""",
],

36: [
"""

A patch to add Syscall User Dispatch was accepted into the Linux
kernel in version 5.8.

""",
"True",
"False",
"",
"red",
"""

Syscall User Dispatch is a feature that allow a process to direct some
syscalls to user-space, and it is useful for an OS compatibility
layers, like WINE.  A patch has been sent to LKML, but it has not been
accepted into Linux mainline yet.
<p>
Source:
<ul>
<li>https://lkml.org/lkml/2020/9/4/1122
</ul>
""",
],

37: [
"""

The year 2020 will be noted for the Coronavirus pandemic, fires, civil
unrest, and economic hardship. What unexpected additional problem did
2020 have?

""",
"Plague",
"Locusts",
"Both",
"both",

"""
The Bubonic plague was reported in China and California this year.
And locusts swarmed in many countries in Africa.
<p>
Sources:
<ul>
<li>https://www.sciencealert.com/california-has-just-reported-a-case-of-human-plague
<li>https://www.bbc.com/future/article/20200806-the-biblical-east-african-locust-plagues-of-2020
</ul>
""",
]
}

