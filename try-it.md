---
layout: page
title: Try PeARS
permalink: /install/
---

Before anything else: a little warning note. The PeARS blog and associated code were written in the space of a few days, which leaves much room for errors and improvement. I am sharing my files in their current state – do feel free to point at the shortcomings.

In this little experiment, we are going to find out which pages we have visited on the Internet, and make some of them available for searching from a raspberry pi on our local network (or, if you don’t have a pi at hand, a directory on our computer simulating the pi’s file system).

###Requirements

I am running all this on an Ubuntu machine, so you may have to adapt things for your OS.

*    install sqlite3: *sudo apt-get install sqlite3*

*    install lynx: *sudo apt-get install lynx-cur*

*    install Stanford POS tagger: Download the ‘basic’ Stanford POS Tagger from [http://nlp.stanford.edu/software/tagger.shtml#Download](http://nlp.stanford.edu/software/tagger.shtml#Download) and unpack it: *unzip stanford-postagger-2014-06-16.zip*. I assume you are unpacking in your home directory, so you end up with a ~/stanford-postagger-2014-06-16/ folder or similar.

*    download MALLET from [http://mallet.cs.umass.edu/download.php](http://mallet.cs.umass.edu/download.php) and unpack it, also in your home directory: tar -xzvf mallet-2.0.7.tar.gz. You should have a ~/mallet-2.0.7/ folder.

*    download and install DISSECT: [http://clic.cimec.unitn.it/composes/toolkit/installation.html](http://clic.cimec.unitn.it/composes/toolkit/installation.html)

*    install web.py: sudo easy_install web.py (if you don't have easy_install on your machine, do *sudo apt-get install python-setuptools*)

*    create a directory for your PeARS experiments: *mkdir ~/PeARS/*

*    get the PeARS scripts from my repository and save them in your ~/PeARS directory, keeping the directory structure intact.

### Get search history

First, we want to access our search history to find out which pages we have visited. Our record will help us decide which pages we want to share with the world. Read this blog entry to find out how to do this.
Process pages we want to share

In this step, we will choose a website that we visit often, and process all the pages in our history for that website, so that they become searchable. For the sake of example, I will assume that everybody has a fair chunk of Wikipedia in their history, and we will start with those pages.

Run the following:


{%highlight bash %}
cd ~/PeARS
./getDomainPages http://en.wikipedia.org wikipedia
{%endhighlight%}

(Your Wikipedia search history might be mostly under the secure https://en.wikipedia.org -- check your history to know which to use.) The getDomainPages script will take care of grabbing the relevant pages from the Internet and processing them, including lemmatising them and producing bags-of-words as well as distributional representations for each sentence on each page.

### Organising a searchable folder

To keep it simple, we will first test the system by creating a Pi1/ folder in ~/PeARS, supposed to simulate a real raspberry pi on the network. I have added a little script to the PeARS repository, called *./addLocalPearFolder*, which you can run to simulate a pi on your local machine. To use it, run:

{%highlight bash %}
./addLocalPearFolder Pi1 wikipedia
{%endhighlight%}

If you want to straight away experiment with a real pi, see [this blog entry](http://minimalparts.github.io/PeARS/2014/07/21/set-up-pi-server/).

### Searching

We are ready to search our local directory, ~/PeARS/Pi1/. Let’s move to the query/ directory of the ~/PeARS folder and start a web server to display the search page:

{%highlight bash %}
cd ~/PeARS/query/
python ./mkQueryPage &
{%endhighlight%}

You can now open your browser and type in the address bar: http://localhost:8080/. This should open a window looking like this:

{% include image.html url="http://minimalparts.github.io/PeARS/assets/pears-homepage.png" description="PeARS search page" %} 

Search your very own search engine! At this point, you may want to be nice to your pear, and search for something that is actually there. Don’t forget: your pear is supposed to be one amongst thousands of others, and you have only saved a few Wikipedia pages on it – don’t expect it to find things that are not there! My own Wikipedia search history includes quite a few pages about dogs, so I’ll search for terrier dog. Here are the results:

{% include image.html url="http://minimalparts.github.io/PeARS/assets/results-terrier-dog.png" description="PeARS search page" %} 

(Note that I get results from other sites too, because I have already processed other domains. You should only get results from Wikipedia at this stage.)

### Closing the search server

The PeARS server will run until you explicitely stop it. Type fg to bring the process back in the foreground, and CTRL+X to kill it. You will also have to close port 2020, where the Stanford POS tagger is running. lsof -w -n -i tcp:2020 will let you find out which process number runs on that port. You can then kill it with kill -9 [pidnumber].
