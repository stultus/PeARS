---
layout: post
title:  "P10: Set up the raspberry pi server"
---

Finally! We can search for real on a remote raspberry pi. Let’s set things up so that we have a web server running on our pi, ready to answer our queries.

(This blog entry is part of a series starting here)

### Procedure

We first want to enable ssh on our pi. See the Adafruit tutorial on how to do this.

There is also a very good tutorial about setting up your raspberry pi as a web server here.

Now, let’s transfer some pre-processed pages to the pi, like we did before when using a local directory as our ‘virtual pi’. For this example, I have processed some pages from the BBC website, which I will transfer to my pi at the address 192.168.2.10.

The first thing to do is to log into the pi and create appropriate folders in the /var/www/ directory:

{% highlight bash %}
ssh -l pi 192.168.2.10
cd /var/www/
mkdir BBC/
mkdir BBC/pages/
logout
{% endhighlight %}

Then, let’s transfer some files. My username on the pi is the default pi, so we are contacting pi@192.168.2.10 via scp.

{% highlight bash %}
scp BBC-pagereps/* pi@192.168.2.10:/var/www/BBC/pages/
scp ~/mallet-2.0.7/BBC.doc.topics.index pi@192.168.2.10:/var/www/BBC/BBC.doc.topics.index
java -mx300m -classpath ~/stanford-postagger-2014-06-16/stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model ~/stanford-postagger-2014-06-16/models/english-left3words-distsim.tagger -textFile ~/mallet-2.0.7/BBC.topic.keys|sed "s/\([0-9]*\)_CD\( [0-9]*\.*[0-9]*\)_CD/\n\1\2/g"|sed "s/\(_[A-Z]\)[A-Z]*/\1/g"|sed '1d'|sed "s/^/192\.168\.2\.10: BBC-/" > tmp
scp tmp pi@192.168.2.10:/var/www/BBC/BBC.topic.keys
rm -f tmp
{% endhighlight %}

We’re all set. Now, you should be able to search your remote pi. Here is a screenshot showing the pi in use:
