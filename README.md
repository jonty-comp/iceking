IceKing
=======

Icecast log file parser / database logging software.   It just parses your icecast log file and logs the details to a PostgreSQL database.
I created this little script as it was always a pain in the backside trying to calculate listener-hour statistics for the radio station I volunteer for, RaW (http://radio.warwick.ac.uk/).  The only open-source software for calculating listener-hours is a port of Webalizer that hasn't been updated for years and requires a complicated script to concatenate many icecast logs together, which fails often.  As long as you have a reliable database server, this script should make the calculations much easier.

Dependencies
============

* Python3
* Psycopg2
