---
layout: post
title:  "Adding pear profiles"
---

The PeARS framework allows the raspberry pis ('pears') on the network to be anything from anonymous to completely personalised. An anonymous pear shares only its ip address with the world -- ideally, it might also regularly exchange topics with other anonymous pears to ensure that its shared content cannot be linked to its owner. A personalised pear, like a social media platform, will allow its owner to set up a profile and become recognisable as a permanent authority on particular topics.

Personalising our pear is far from a priority at this stage of development, of course, but I believe that fun and pretty things are more likely to be played with and improved. So let's make some tiny changes to the system to personalise our pear with a picture, and perhaps a message to the queryer (for instance, a website recommendation).

We'll assume that on each pi, we have a *pear.profile* file looking like this: 

{% highlight bash %}
name = "sleepy_doggie"
img = "sleepy_doggie.jpg"
message = "My recommendation of the month: https://www.adafruit.com/category/105"
{% endhighlight %}

The name entry is a recognisable 'name' for that pear on the network, 'img' is a 100x100px image that will appear on the queryer's search results page, and 'message' is a short text that will pop up when going over the image with the mouse. *pear.profile* is situated at the root of the shared folder, so in /var/www/ on the Pi (or ~/PeARS/Pi1 if you are still playing with local folders). There is a generic profile for the anonymous pears, available from the *Pi-template* folder in the repository.

I have put some CSS in the *~/PeARS/query/static/* folder to allow for the query page to display the pears' profiles appropriately. I have also changed the topicaliseQueryBrowser.py script to return whole pear profiles to the queryer, rather than just their ip address. The relevant code is under the 'Output helpful pears' heading.

The new search results page looks like this:


{% include image.html url="http://minimalparts.github.io/PeARS/assets/pretty-pears.png" description="PeARS search results page" %} 
