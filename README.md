Steps
Configure MailJet
--------------------
- create an account in MailJet
- create data directory
- create credentials.json file:
{"keys": {
    "api_key": "################################",
    "api_secret": "################################"},
"from":  {
    "Email": "yourmail@domain.com",
    "Name": "Your Name"
  }
}

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









