# What is a Reactive Dog Journal, anyway?
You've seen it before: some poor sucker hanging on for dear life to the end of a leash while her dog barks and snarls and lunges at some innocent bystander/puppy/weirdly-shaped bush (oh, is that just my dog?). Sometimes this behaviour is the fault of bad training early on, other times it's poor or absent socialization from the dog's puppyhood, and other times it's just genetics. Whatever it is, it's embarrassing and overwhelming.

I know, because I live with a (lovely, wonderful, spectacular) reactive dog.

There are a lot of resources online about how to help resolve reactivity in dogs, so I won't go into that here. However, one common recommendation is to create a daily journal to log the dog's successes and failures. I've been doing this on and off for about a year and a half now, and I wanted to create an easy way to create, save, and view these logs, and also generate graphical reports summarizing historical patterns.

# History of Reactive-Dog-Journal
I first started this Reactive Dog Journal (RDJ) at the UBC Local Hack Day in December 2016. I had a vague idea of what I wanted -- a simple app to replace what I was doing in Notepad every day for my dog -- and no idea how to implement. I decided on Python and the wxPython library since a) I liked Python and b) it seemed similar to the little GUIs I had made in Java with Swing in class a year ago.

This was a big mistake.

Although I happily worked on it for about 10 hours in one day, when I later reflected on my progress, I realized it was turning into a big mess: structurally disorganized, tedious to program (so many buttons and menus...), and inelegant to look at.

I asked Reddit what to do, and they answered: Scrap it! Start again with the Django framework and make a way cooler web app.

So that's what I'm doing.

You'll find the Reactive-Dog-Journal-2 repository is much more up-to-date, but I leave this up here just in case I decide to finish it some day or in case somebody else can learn from my mistakes!

# Features to come ...
This is still significantly a work in progress.

TODO:
- refactor!
- fix "Edit" dialog box
- search and sort saved entries
- Report functionality in general

WISHLIST:
- turn into a web app
- database with Django?
