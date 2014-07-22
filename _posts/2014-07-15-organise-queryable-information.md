---
layout: post
title:  "Organise queryable information"
---

By now, we have all we need on the 'search engine' side of things: a list of topics covered by the node, an index recording the main topics of each page, and a bag-of-words representation of each page. We will now transfer that information to one of our *pears* (i.e. a raspberry pi on the peer-to-peer network). 

{% highlight ruby %}
mkdir Pi1/
mkdir Pi1/pages
cp domains/wikipedia-pagereps/* Pi1/pages/
cat ~/mallet-2.0.7/wikipedia.doc.topics.index >> Pi1/doc.topic.index
cat ~/mallet-2.0.7/wikipedia.topic.keys|sed "s/^/Pi1: /" > Pi1/topic.keys 
{% endhighlight %}

Note that we are adding the name of the pear at the beginning of each line in the topic.keys file. This is to ensure that we know where the topic is stored.
