Certificates Mailer
===================

[![License](https://img.shields.io/github/license/marian-vignau/certmailer.svg)](https://pypi.python.org/pypi/certmailer)
[![PyPI Version](http://img.shields.io/pypi/v/certmailer.svg)](https://pypi.python.org/pypi/certmailer)
[![Twitter Follow](https://img.shields.io/twitter/follow/mavignau?style=social)](https://twitter.com/mavignau)
![GitHub last commit](https://img.shields.io/github/last-commit/marian-vignau/certmailer)

**Automate** sending event's certificates by email.
---------------------------------------------------


Uses exported information from **EventoL**,
generate **certificates in PDF**, and **mail them** to the
corresponding receiver.


![CheatSheet](https://raw.githubusercontent.com/marian-vignau/certmailer/master/doc/cheatsheet.png)


Install
=======


> virtualenv -p python3 *somewhere*
> cd *somewhere*
> source bin/activate
> pip install certmailer


or using fades

> fades -d certmailer -x certmail

or add to your ~/.bashrc

> certmail() { fades -d certmailer -x certmail $@; }

Usage
=====

Create an account in MailJet, to send SMTP.

Configure

> certmail config

Type the api key and the secret key give to you by MailJet service

Create a new job

> certmail job new

Add data
--------

Go to the **EventoL** instance, login, and choose
https://eventol.domain.com/admin

Select Activity, Attendees, Collaborators and Installers,
and export one by one to yaml format.

Add them using

> certmail data add \*.yaml

Create the list of recipients

> certmail import

this will parse the yaml files exported from **EventoL**, and create a
csv.

Check the list of receivers

> certmail edit list

It'll open the default editor on every case.

If you don't want that somebody receives an email, clear «send mail?»
cell.

If you want to add some certificate, add **yes** to the corresponding
cell.

And if you don't want to send a certificate, clear the corresponding
cell.

Add attachments and edit format
-------------------------------

Add attachments using

> certmail attach add

Edit email's text part

> certmail edit text

Edit email's HTML part

> certmail edit html

Edit certificate in InkScape

> certmail edit certificate


Run everything
==============

> certmail send

This will create the certificates pdf to send, 
All the information will be stored on the «cache//outbox» directory.

This will send every mail. Every mail sent will be logged. 

If for some reason any mail isn't sended, it will

In linux systems, uses memory to store intermediate results, to speed up and 
to better use hard disks.

> certmail send --flag <flag>

The flag is used to send **only** the emails that are flagged in the send column
with the word <flag>. 

Requirements
============

-  Python 3
-  PyYaml
-  mailjet-rest
-  click

Dev Instructions
================


> git clone git@github.com:marian-vignau/certmailer.git
> virtualenv env
> source env/bin/activate
> pip install -e .

Contributing
============

1. Fork it!

2. Create your feature branch: ``git checkout -b my-new-feature``

3. Commit your changes: ``git commit -am 'Add some feature'``

4. Push to the branch: ``git push origin my-new-feature``

5. Submit a pull request :D

TODO
====

-  Extend documentation
-  Digital signature

Credits
=======

-  María Andrea Vignau

