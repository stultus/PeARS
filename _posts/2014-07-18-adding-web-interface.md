---
layout: post
title:  "P7: Adding a web interface"
---

It all looks good so far, but I know a lot of people who won’t be happy with a command-line search engine. So let’s design a local web page to take user input and display search results.

(This blog entry is part of a series starting [here]())

### Requirements

To build a search page which interacts with our other Python scripts, we will need web.py, which we install in the following way:


{%highlight bash %}
sudo easy_install web.py
{%endhighlight%}

### Procedure

The script mkQueryPage.py in the query folder of my repository deals with everything we need to start a local web search server. It is a slight modification to the sample script offered by the web.py team. It simply presents a search form to the user and executes query topicalisation and document retrieval in response to a submitting event. The actual design of the webpage is included in a templates folder, where some HTML and CSS files tell the browser what the page should look like.

Running the server is easy. We simply type the following on the command line, in the query folder:


{%highlight bash %}
python mkQueryPage.py &
{%endhighlight%}

We can now open our browser and visit http://localhost:2020/. We will be presented with the search page:

mkQueryPage.py is also responsible for sending the query to http://duckduckgo.com if no document on the available pears is relevant.
