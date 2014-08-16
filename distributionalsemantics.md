---
layout: page
title: Distributional semantics
permalink: /distributionalsemantics/
---

### What is distributional semantics?

Semantics is the study of meaning. It investigates questions such as: What is meaning? How come words and sentences have meaning? What *is* the meaning of words and sentences? How can the meanings of words combine to form the meaning of sentences? Do two people *mean* the same thing when they utter the word 'cat'? How do we communicate? Etc, etc.

As a proficient language user, you don't have to think about meaning much in your everyday life, and you can effortlessly ascertain, for example, that a cat is more like a dog than a coconut. How do you do this?

Distributional semantics is a theory of meaning which is computationally implementable and very, very good at modelling what humans do when they make similarity judgements. Here is a typical output for a distributional similarity system asked to quantify the similarity of cats, dogs and coconuts. The values are between 0 and 1, with 0 indicating no similarity at all and 1 indicating identity.

{% include image.html url="http://minimalparts.github.io/PeARS/assets/cat-coconut.png" description="The similarity of cats, dogs and coconuts" %} 

As you see, cats and dogs are much more similar (close to 1) than cats and coconuts (close to 0).

In order to make such predictions, distributional semantics relies on a specific view of meaning, i.e. that meaning comes from usage, or in other words, that the meaning of 'cat' comes from the way we use the word in everyday life. This approach to meaning is in no way the only one, but has come from a particular philosophical tradition involving linguists and philosophers such as [Leonard Bloomfield](https://en.wikipedia.org/wiki/Leonard_Bloomfield), [Zellig Harris](https://en.wikipedia.org/wiki/Zellig_Harris), [J.R. Firth](https://en.wikipedia.org/wiki/John_Rupert_Firth) or again [Ludwig Wittgenstein](https://en.wikipedia.org/wiki/Wittgenstein) (in his later work) and [Margaret Masterman](https://en.wikipedia.org/wiki/Margaret_Masterman).

If we say that meaning comes from use, we can derive a model of meaning from observable uses of language. This is what distributional semantics does, in a somewhat constrained fashion. A typical way to get an approximation of the meaning of words in distributional semantics is to look at their linguistic context in a very large corpus, for instance Wikipedia. The linguistic context of a word is simply the other words that appear next to it. So for example, the following might be a context for 'coconut':

*found throughout the tropic and subtropic area, the --- is known for its great versatility*

Let's now assume that we collect every single instance of the word 'coconut' in Wikipedia, and start counting how many times it appears next to 'tropic', 'versatility', 'the', 'subatomic', etc. We would probably find that coconuts appear many more times next to 'tropic' than next to 'subatomic': this is a good indication of what coconuts are about. But counting is not enough. The word 'coconut' appears thousands of times next to 'the', which doesn't mean that 'the' tells us very much about what coconuts are. So usually, the raw counts are combined into statistical measures which help us define more accurately which words are 'characteristic' for a particular term. Pointwise Mutual Information is one such measure, which gives higher values to words that are really defining for a term: for instance, 'tropic', 'food', 'palm' for 'coconut'.

Once we have such measures, we can build a simulation of how the words in a particular language relate to each other. This is done in a so-called 'semantic space' which, mathematically, corresponds to a vector space. The dimensions of the vector space are context words like 'tropic' or 'versatility' and words are defined as points (or vectors) in that space. Here is a very simplified example, where I define the words 'dragon', 'lion' and 'democracy' with respect to only two dimensions: 'dangerous' and 'political'.

{% include image.html url="http://minimalparts.github.io/PeARS/assets/semantic-space.png" description="A semantic space with only two dimensions" %} 

Because dragons and lions have much to do with being dangerous but very little with political systems, their vectors have a high value along the 'dangerous' axis and a small value along the 'political' axis. The opposite is true for 'democracy'. Note that very naturally, the vectors for 'dragon' and 'lion' have clustered together in the space, while 'democracy' is much further from them. By calculating the distance between two vectors in a semantic space, we can deduce the similarity of two words: this is what allows us to say that cats and dogs are more alike than cats and coconuts.

In real life, semantic spaces are built with thousands, or even hundreds of thousands of dimensions. Techniques such as dimensionality reduction are used to make the space more computationally tractable.

PeARS uses distributional semantics at two stages of its algorithm:

* the [comparison of a user query with the topics curated by one pear](http://minimalparts.github.io/PeARS/2014/07/15/topicalising-queries/) (raspberry pi) on the network: this allows the system to route the user query to the most appropriate node(s) on the network instead of querying them all;
* the comparison of the user query with individual documents in a topic: this step acts as a scoring system for all potentially relevant documents, only keeping those which are similar enough to the query.

The description above only discusses the basic idea behind distributional semantics. In order to compare groups of words, or words with sentences, or even documents, we need a model of how the meaning of words combine together. This is an area of active research. For those interested, the following paper is a good introduction to the topic:

Clark. Forthcoming. [Vector Space Models of Lexical Meaning](http://www.cl.cam.ac.uk/%7Esc609/pubs/sem_handbook.pdf). To appear in the forthcoming Wiley-Blackwell Handbook of Contemporary Semantics — second edition, edited by Shalom Lappin and Chris Fox.
