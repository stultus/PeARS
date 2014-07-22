---
layout: post
title:  "P1: Retrieving browsing history from Firefox"
date: 2014-07-13 00:00:00
---
The idea behing PeARS is that people share some part of their search history. In this first entry, we will look at obtaining a list of visited pages from Firefox.

(This blog entry is the first one in a series of ten, all starting with the prefix P+number.)

### Procedure

Let’s start by creating a copy of our search history. This is possible using sqlite3 (install in Ubuntu with sudo apt-get install sqlite3).

I am assuming we have a directory for our PeARS experiments located at ~/PeARS.

First, let’s find the location of the places.sqlite file in our Firefox installation. It should be something like ~/.mozilla/firefox/vd15j24z.default/places.sqlite. Let’s run: 

{% highlight bash %}
sqlite3 places.sqlite "SELECT url FROM moz_places" > ~/PEAR/history.txt
{% endhighlight %}

You probably want to get rid of funny pages in the list (queries and such likes), so clean history.txt:

{%highlight bash %}
less history.txt |egrep -v "\?|\&|\#"|egrep "^http" > history.pages
{%endhighlight%}

NB: I’m afraid I haven’t looked into getting a search history from other browsers yet. Feel free to add instructions in the comments. If the worst comes to the worst and you can’t get your history, fake yourself a history file containing URLs, one on each line, and call it history.pages.
