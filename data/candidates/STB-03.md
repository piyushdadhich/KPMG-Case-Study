PORTFOLIO NOTE — what I built and what it taught me

I didn't come to this through a computer science degree. I run operations for a regional courier business, and I got tired of watching our dispatcher spend the first ninety minutes of every morning copying driver availability out of text messages into a route spreadsheet.

So I built the thing myself. I taught myself Python from the standard library docs and a long trail of failed attempts. The system today is a WhatsApp check-in bot connected to a route sheet generator. Drivers reply to one morning message; the bot reads their availability, drafts the day's route sheet, and posts it to the dispatch channel.

All nine drivers have used it every morning since March. It saves us roughly an hour of dispatcher time every day, which during peak season is the difference between answering the phone and not.

The part I'm most proud of is what I removed. My first version tried to fully automate route assignment. Drivers ignored it within a week because it didn't know what they knew about traffic, loading docks, and which customers tolerate a late window. I rebuilt it so the bot drafts the route sheet and our dispatcher rearranges it by hand before sending. Draft, don't decide. Adoption followed almost immediately.

I learn by keeping my mistakes visible. When the bot gets an address wrong I screenshot it into a folder I review on Sundays, and the worst ones become test cases for the parser. It is not a formal evaluation process, but it is the reason the address errors have nearly stopped.

What I'd build next: the bot still has no guardrail for a driver replying with something ambiguous, and right now it guesses. It should ask. That is the next thing I fix.
