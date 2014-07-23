---
layout: post
title:  "P4: Web page representation: the bag-of-words model"
---
For now, we will just represent our pages in a very simplified way, using a bag-of-words for each sentence in the file, that is, we simply output the lemmas for each sentence.

(This blog entry is part of a series starting [here](http://minimalparts.github.io/PeARS/2014/07/13/retrieving-browsing-history/))

### Procedure

The script mkPageRepresentations, called by getDomainPages (both available [here](https://github.com/minimalparts/PeARS/)), does the work of producing the relevant files. We can run mkPageRepresentations as a standalone over our wikipedia pages:



{% highlight bash %}
de ~/PeARS/
./mkPagesRepresentations wikipedia
{% endhighlight %}

The output, located in the domains/wikipedia-pagereps/ directory, should look like this (for each page):

{% highlight bash %}
<page>
        <url=https://en.wikipedia.org/wiki/Aardvark/>
        <sentences>
                <sentence id=1>
                <BOW>the_D aardvark_N -lrb-_- /_: ard-vark_N ,_, Orycteropus_N afer_N \
		-rrb-_- be_V a_D medium-sized_J ,_, burrow_V ,_, it_P be_V the_D only_R \
		live_V species_N of_I the_D order_N although_I other_J prehistoric_J species_N \
		and_C genus_N of_I Tubulidentata_N be_V know_V ._.</BOW>
                </sentence>
                <sentence id=2>
		<BOW>it_P resemble_V a_D pig_N with_I a_D long_J snout_N ,_, which_W be_V use_V \
		to_T sniff_V out_R food_N ._.</BOW>
                </sentence>
	...
	</sentences>
</page>
{% endhighlight %}
