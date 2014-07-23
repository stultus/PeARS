---
layout: post
title:  "P2: Lemmatising web pages"
---

When a user types in the query 'dogs' in our PeARS search engine, we want to be able to retrieve not only pages containing 'dogs', but also 'dog', in the singular form. To achieve this, we will apply so-called 'lemmatisation' to our files.

(This blog entry is part of a series starting [here](http://minimalparts.github.io/PeARS/2014/07/13/retrieving-browsing-history/))

### Procedure

[Lemmatising](https://en.wikipedia.org/wiki/Lemmatisation) is the process of retrieving the base form of words (i.e. their non-inflected form). The idea is to convert all forms of a word to a unique, so-called *lemma*: e.g. *eating, ate, eats, eaten* all get converted to *eat*. 

In what follows, I will demonstrate the lemmatisation process for pages from a particular domain -- Wikipedia. We need the following installed:

* lynx, a text-only web browser  (*sudo apt-get install lynx-cur*)
* the Stanford POS tagger, which can be downloaded [here](http://nlp.stanford.edu/software/tagger.shtml) The basic version will suffice. After downloading the file, we unpack it with *unzip stanford-postagger-2014-06-16.zip*.

We have our cleaned browsing history, [*history.pages*](http://minimalparts.github.io/PeARS/2014/07/13/retrieving-browsing-history/), in the ~/PEAR directory. First, let's isolate the wikipedia pages and record them in a separate file, *wikipedia.pages*:


{%highlight bash %}
less history.txt |grep "en.wikipedia.org" > wikipedia.pages
{%endhighlight%}

Then, let's dump those pages in a wikipedia directory, and while we're at it, let's already create a directory to receive the lemmatised versions of the files:

{%highlight bash %}
mkdir domains/
mkdir domains/wikipedia/
mkdir domains/wikipedia-lemmas/
c=0	#initialise counter
while read l; 
do 
echo "### $l" > domains/wikipedia/$c.lynx;	#Record URL of the page
lynx -dump $l|sed "s/\[.\+\]//g"|egrep -v "[0-9]*\. http" >> domains/wikipedia/$c.lynx; 
c=`expr $c + 1`
done < wikipedia.pages
{%endhighlight%}

Now, we'll move to the directory where we have unpacked the Stanford POS tagger, and lemmatise all pages in the ~/PeARS/domains/wikipedia/ folder:

{%highlight bash %}
cd ~/stanford-postagger-2014-06-16
for f in ~/PeARS/domains/wikipedia/*; 
do
flemmas=`echo $f|sed "s/wikipedia/wikipedia-lemmas/"`;
cat $f|sed '1d' > postag.tmp
head -1 $f > $flemmas	#Record URL in lemmatised file
java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-left3words-distsim.tagger -textFile postag.tmp  -outputFormatOptions lemmatize -outputFormat inlineXML|egrep "pos.*lemma|<.sentence>"|sed "s/.*pos=.\([^\"]*\). lemma=.\([^\"]*\).*/\2_\1/"|tr '\n' ' '|sed "s/<.sentence>/\n/g"|sed "s/^ //" >> $flemmas
done
rm -f postag.tmp
{%endhighlight%}

The output of a file's lemmatisation should be something like the following, i.e. a file with one sentence per line, words converted into lemmas and followed by their parts-of-speech.

{%highlight bash %}
with_IN a_DT lower_JJR case_NN ``_`` p_NN ''_'' ,_, ``_`` platonism_NN ''_'' refer_VBZ to_TO the_DT philosophy_NN that_WDT affirm_VBZ the_DT existence_NN of_IN abstract_JJ object_NNS ,_, which_WDT be_VBP assert_VBN to_TO ``_`` exist_VB ''_'' in_IN a_DT ``_`` third_JJ realm_NN ''_'' distinct_JJ both_CC from_IN the_DT sensible_JJ external_JJ world_NN and_CC from_IN the_DT internal_JJ world_NN of_IN consciousness_NN ,_, and_CC be_VBZ the_DT opposite_NN of_IN Lower_NNP case_NN ``_`` platonist_NNS ''_'' need_MD not_RB accept_VB any_DT of_IN the_DT doctrine_NNS of_IN Plato_NNP ._. 
{%endhighlight%}
