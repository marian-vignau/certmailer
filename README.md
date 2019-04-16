Install
-------
git clone https://github.com/marian-vignau/certmailer.git
cd certmailer
git clone https://github.com/facundobatista/certg.git

![Bilby Stampede](doc/certmail.png)


Create an account in MailJet, to send SMTP

Create a work directory

> python -m certmail.py init

Edit config.yaml and add public and private key

Edit email.yaml and create the template of email

Edit certificate.svg and create the template of certificates

Go to the **EventoL** instance, login, and choose https://eventol.domain.com/admin

Select Activity, Attendees, Collaborators and Installers,
and export one by one to yaml format.

Put this files on «work/data» folder, created with init command

> python -m certmail.py makecsv

this will parse the yaml files exported from **EventoL**, and create a csv.

If you don't want that somebody receives an email, clear «send mail?» cell.

If you want to add some certificate, add **yes** to the corresponding cell.

And if you don't want to send a certificate, clear the corresponding cell.

> python -m certmail.py makepdf

This will create the certificates pdf to send, and yaml files with
all the info of every mail that will be sent.
All the information will be stored on the «work/outbox» directory.

> python -m certmail.py sendmails

This will send every mail. If an email is successfully sent, all it's data'll
move to «work/sent» folder, and a json with information of resulting
email will be stored.

Enjoy












