---
layout: page
title: About
permalink: /about/
---

Imagine a new kind of Internet search. When you have a query, instead of going to a big, centralised search engine, well, you just ask someone! "Nicole, where can I find some cool fabric for my new dress?", "James, how do I get from Orly airport to the Gare du Nord in Paris?", "Jane, what is a cruck barn?" Of course, Nicole, James and Jane are not waiting in front of their computer, ready to answer your queries. Instead, they each own a raspberry pi where they store some of their (processed) search history. When you send your query over the Internet, a bunch of pis take care of it and send you search results based on the knowledge, expertise and preferences of their owners – all of this, of course, entirely anonymously. The PeARS project is a little experiment investigating how this would all work in practice. 


A little story
--------------

Imagine a possible world. In that world, we are going to meet three people:

* ![A clothes designer!]("{{ "/assets/clothes-design.png" | prepend: site.baseurl }}") Lea: Lea has a special talent for designing clothes. She can make something new and exciting out of an old recycled T-shirt and some found bits and bobs. She’s always on the lookout for interesting accessories. Last year, while on holiday, she discovered a little shop in a little village, that specialises in extravagant buttons. The little shop in the little village is not well known at all. It does have a website, but you really need to have the shopkeeper’s card to find it on the web.

* ![An instrument maker!]("{{ "/assets/instrument-maker.png" | prepend: site.baseurl }}")Nasrin: Nasrin is an instrument-maker by profession. Not only does she sell beautiful string instruments with perfect sound to lucky musicians, but she also had an interest in forgotten medieval instruments, which she tries to revive by painstakingly reading old manuscripts, and making hypotheses about their original design. She records her thoughts on a little homepage, in a rather irregular manner.

* ![Bird watching!]("{{ "/assets/bird-watching.png" | prepend: site.baseurl }}")Yue: Yue is an enthusiastic birdwatcher who spends all his weekends out and about, no matter the weather, to catch a glance of beautiful and rare species. He shares his bird pictures with others on the Internet.

This week, Yue's friend Kim is celebrating her  birthday. Kim is really good at making clothes, and Yue would like to buy her something special, perhaps related to her hobby. He decides to go on the Internet to try and find cool sewing accessories. While he's at it, he also wants to find out a bit more about some weird musical instrument that cropped up in a novel he's reading.

In another place and another time, Yue would have typed his queries in the web interface of a big search engine and got straight to the page of a large site for sewing materials, as well as some general encyclopaedic page on the instrument he is interested in. This would have satisfied his immediate needs, but without providing a special experience: Kim probably knows of the large site for sewing materials, and has spent hours browsing through its pages. Yue's knowledge about the instrument might have been a little enriched, but might have left him with still many more questions.

In our possible world, Yue bypasses the big search engine and goes instead to the specialists: Aisha and Lea. He doesn't know them, but his personal search engine knows how to find them. By accessing information Aisha is sharing about her favourite websites, Yue finds the little button shop in the little village and orders from them. No need to say, Kim is dead impressed... As for finding out more about the weird instrument, Lea happens to have several pages of information on it, together with hypothetical plans and references to old manuscripts. Yue is over the moon!


How it works
------------

Search is distributed over a network of peers (or 'pears', as I prefer to call them). Each pear is a raspberry pi connected to the Internet and making available a representation of the pages that the raspberry pi's owner has visited (and is willing to share with the world). So in our little story above, Aisha's raspberry pi probably stores lots of pages about clothes design, as well as pages related to Aisha's other interests. Instead of relying on a big search engine developed and maintained by a company, we have a little piece of software running on everyone's computer. When someone queries his or her personal search engine (I call it 'pear-picking', or in short, 'picking'), the engine tries to find the pears most likely to know about that query – that is, the raspberry pis that belong to people interested in the topic. This is how we get access to people's best Internet tips!

Advantages:

*    Privacy: by distributing your queries to thousands of different individual computers, you avoid the situation where one large company accumulates information about your searches.

*    Digital self-sufficiency: it is well-known that pears from your own garden taste better. They also ensure that you are in control of your food supply. PeARS does the same for web search.

*   No crawl necessary: the shared pages are those that people visit anyway.

*    Access to pages that would be lost in the results of an aggregated search engine.

*    Social aspect: it is possible to make one’s pear(s) more or less anonymous. The social network buffs out there will like building their own search communities.

