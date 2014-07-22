---
layout: post
title:  "P8: Document retrieval"
---

At the query topicalisation stage, we produced a list of pis that may hold the answer to the user query, together with a list of topics, for each pi, which may be relevant to the search. The topicaliseQueryBrowser.py script produced a little file, pi-topics.tmp, which holds this information. Now, we know exactly which pears on the network we should query, and which of the pages we should process to try and find the most relevant ones. compareQuerySentenceBrowser.py (available here) deals with all of this and returns results to the main mkQueryPage.py script, which will display them in our browser.


