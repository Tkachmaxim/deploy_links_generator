# Here Implementions a service to shorten provided links.
## Service was realized using Python 3.9.6 and Django 3.2.6. All reqiriments in file requirements.txt.
## May be possible implement this service using lighter Flask, but I have not experience with it.
## The number of input links is infinite, but the set of 6-symbols shortcuts is finite. If in database tehere are two links with same shortcod query return earliest link and redirect if it is not expired. 