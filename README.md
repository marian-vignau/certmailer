Install
-------
git clone repo
cd certmail
git clone certg

![Bilby Stampede](doc/certmail.png)


Create an account in MailJet, to send SMTP

Create a work directory

> python -m certmail.py init

Edit config.yaml and add public and private key

Edit email.yaml and create the template of email

Edit certificate.svg and create the template of certificates

Go to the eventol instance, login, and choose evento.domain.com/admin

Select Activity, Attendees, Collaborators and Installers, and export to yaml format.

Put this files on work/data folder, created with init command

> python -m certmail.py makecsv

this will parse the yaml files exported from eventol, and create a csv.

If you don't want that somebody receives an email, clear de send mail? column

If yoy want to add some certificate to someone, add yes to the corresponding column

And if you don't want to send a certificate, clear the corresponding cell.

> python -m certmail.py makepdf

This will create the certificates pdf to send, and yaml files with
all the info of every mail that will be sent.
All the information will be stored on the work/outbox directory.

> python -m certmail.py sendmails

This will send every mail. If an email is succefully sent, all it's data'll
move to sent folder, and a json with information of resulting email will be sent.

Enjoy







Extract data
---------------
- In https://eventol.flisol.org.ar/admin
- Goto to Actividades, Asistentes, Colaboradores, Instaladores
- Select export and export to json
- copy downloaded files to data directory

Process data and create certificates list
------------------------------------------
- add events.yaml to data subdir. Sample
´´´
- name: Rcia18
  title: "Flisol Resistencia 2018"
  date: '2018-04-28'
- name: Rcia19
  title: "Flisol Resistencia 2019"
  date: '2019-04-27'

´´´
python -m create_list.py









