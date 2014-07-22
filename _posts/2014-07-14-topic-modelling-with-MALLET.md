---
layout: post
title:  "P3: Topic modelling with MALLET"
---

[Topic modelling](http://en.wikipedia.org/wiki/Topic_model) is the process of discovering the topics a text is made of. For instance, a text about house pets might be made of the topics cats, dogs and parrots, the first two being much more prominent in the text than the third. We will apply topic modelling to our collection of documents, so that we know roughly what they are about.

Note that the code described in this entry is part of a script, mkDomainPages, available in my repository. If you would like to run the code without learning about each step separately, please consult this page.

(This blog entry is part of a series starting [here]({{ site.baseurl }}/2014/07/13/retrieving-browsing-history/))

Requirements
------------

Install MALLET from http://mallet.cs.umass.edu/download.php:

{%highlight bash %}
wget http://mallet.cs.umass.edu/dist/mallet-2.0.7.tar.gz
tar -xzvf mallet-2.0.7.tar.gz
{%endhighlight%}

Procedure
---------


For the topic modelling stage, we only need coarse parts-of-speech, i.e. we only want to know whether something is a noun or a verb, not whether it is a plural or a singular, or a past or a 3rd person singular. Also, MALLET doesn't like underscores, so we want to convert them into hyphens. We process the files accordingly, copying the new version into the MALLET directory:


{%highlight bash %}
cd mallet-2.0.7/
mkdir data/
mkdir data/wikipedia
for f in ~/PEARS/wikipedia-lemmas/*;  
do  
f2=`echo $f|sed "s/.*\///"`;  
head -1 $f > data/wikipedia/$f2; 
cat $f|sed '1d'|sed "s/_\(.\)[^ ]*/-\1/g" >> data/wikipedia/$f2;  
done
{%endhighlight%}

Still in the MALLET folder, import the data from the data/wikipedia folder:

{%highlight bash %}
bin/mallet import-dir --input data/wikipedia/ --output wikipedia.mallet \
--keep-sequence --remove-stopwords
{%endhighlight%}

Next, launch the topic modelling. The number of topics to model will depend on the number of web pages in your collection. As a rule of thumb, I go for a tenth of the number of pages. So with 546 pages in my Wikipedia folder, I choose 50 topics.

{%highlight bash %}
bin/mallet train-topics --input wikipedia.mallet \
  --num-topics 50 --output-state topic-state.gz \
  --output-doc-topics wikipedia.doc.topics \
  --output-topic-keys wikipedia.topic.keys
{%endhighlight%}

If we now look at the file wikipedia.topic.keys, we will find our 50 topics, one per line, looking like this:

{%highlight bash %}
14      1       fish salmon species octopus catfish carp tissue pacific trout marine fishing fin cell water group sea atlantic family body
{%endhighlight%}

As we see, a topic is a list of words related to a particular concept -- here, *fish*.

It would also be nice to have an index telling us what the main topics are for each web page. Let's construct such an index:

{%highlight bash %}
cat wikipedia.doc.topics|sed '1d' > doc.topics.tmp
while read l; 
do 
f=`echo $l|sed "s/[0-9]* file://"|sed "s/ .*//"`;	#Record file on system 
fn=`echo $f|egrep -o "[0-9]*\.lynx"`;	#Record file name
w=`head -1 $f|sed "s/### //"`;	#Record URL
#Record 5 top topics for each document
topics=`echo $l|sed "s/ \([0-9]\+ [0-9]*\.[0-9]*\)/\n\1/g"|egrep "^[0-9]* [0-9]\."|sed "s/ [0-9]\..*//"|head -5|tr '\n' ' '|sed "s/ $//"`; 
echo "FILE: $fn URL: $w TOPICS: $topics"; 
done < doc.topics.tmp > wikipedia.doc.topics.index
rm -f doc.topics.tmp
{%endhighlight%}
