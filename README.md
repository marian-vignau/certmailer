Certificates Mailer
-------------------

### **Automate** sending event's certificates by email.

Uses exported information from  **EventoL**,
generate **certificates in PDF**, and **mail them** to the corresponding
receiver.

![Bilby Stampede](https://raw.githubusercontent.com/marian-vignau/certmailer/master/doc/cheatsheet.png)

## Install

pip install certmailer

## Usage

Create an account in MailJet, to send SMTP.

Configure

> certmail config

Type the api key and the secret key give to you by MailJet service

Create a new job

> certmail job new <name>

### Add data

Go to the **EventoL** instance, login, and choose https://eventol.domain.com/admin

Select Activity, Attendees, Collaborators and Installers,
and export one by one to yaml format.

Add them using

> certmail data add *.yaml

Create the list of recipients

> certmail do list

this will parse the yaml files exported from **EventoL**, and create a csv.

Check the list of receivers

> certmail edit receivers

It'll open the default editor on every case.

If you don't want that somebody receives an email, clear «send mail?» cell.

If you want to add some certificate, add **yes** to the corresponding cell.

And if you don't want to send a certificate, clear the corresponding cell.


### Add attachments and edit format

Add attachments using

> certmail attach add <filename>

Edit email's text part

> certmail edit text

Edit email's HTML part

> certmail edit html

Edit certificate in InkScape

> certmail edit certificate

Create the template

> certmail do template

## Run everything

> certmail do certificates

This will create the certificates pdf to send, and yaml files with
all the info of every mail that will be sent.
All the information will be stored on the «cache/<job>/outbox» directory.

> certmail do send

This will send every mail. If an email is successfully sent, all it's data'll
move to «cache/<job>/sent» folder, and a json with information of resulting
email will be stored.

## Requirements

- Python 3
- PyYaml
- certg
- mailjet-rest
- click

## Dev Instructions
```
- git clone git@github.com:marian-vignau/certmailer.git
- virtualenv env
- source env/bin/activate
- pip install -e .
```

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## TODO

* Extend documentation
* Digital signature

## Credits

* María Andrea Vignau












