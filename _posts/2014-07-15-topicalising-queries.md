---
layout: post
title:  "Topicalising search queries"
---
It is now time to think about our actual search function. The first thing we have to do is find a way to topicalise the user’s query, i.e. find out roughly what it is about. This step is the most crucial one in the whole PeARS framework: it ensures that we don’t have to go and search all the pears on the network – only the relevant ones. To do this, we will use the topic.keys file we produced at the topic modelling stage.

Requirements:
-------------
Install DISSECT from http://clic.cimec.unitn.it/composes/toolkit/installation.html


Procedure:
----------

In the following, I assume that we have two pis on the network, Pi1 and Pi2. Pi1 has indexed Wikipedia pages, while Pi2 contains stackoverflow Q&As. We have just concatenated their topic.keys files and made the result available to the queryer:

{% highlight ruby %}
mkdir query/
cd query/
cat ../Pi1/wikipedia.topic.keys ../Pi2/stackoverflow.topic.keys > topic.keys
{% endhighlight %}

Obviously, with thousands of Pis on the network, we would need a cleverer way to aggregate the topic.keys files. But for now, we will keep things simple. I have written a little python script, *topicalise-query.py*,  which asks the user to enter a query and identifies which Pi(s) are more likely to provide the answer. The output looks like this:


{% highlight ruby %}
python topicalise-query.py bnc.ppmi.nmf_300.pkl
search: bald eagle
0.496709675873 Pi1: 7	1	rrb lrb moose elk deer crab red hydrangea bull gaur \
hermit okapi species duiker antler north mountain wombat forest 
0.360004187419 Pi1: 6	1	fish shark salmon species tuna pike octopus salamander \
retrieve carp trout pacific fishing fin water sea catshark atlantic freshwater 
0.345197911976 Pi1: 38	1	rrb lrb tiger mongoose cat seal badger fox otter coyote \
civet weasel hyena family genet striped fur american palm 
[['Pi1', '7'], ['Pi1', '6'], ['Pi1', '38']]

{% endhighlight %}
