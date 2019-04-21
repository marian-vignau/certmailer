#!/usr/bin/env python3

# Copyright 2019 María Andrea Vignau

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check

__author__ = "María Andrea Vignau"

# guide in https://dev.mailjet.com/guides/?python#send-with-attached-files

import yaml
import pathlib
import base64

CONFIGPATH = pathlib.Path("../work/config")

data = {
    "From": {
        "Email": "mavignau@gmail.com",
        "Name": "Organización Flisol Resistencia 2019",
    },
    "To": [{"Email": "{email}", "Name": "{name}"}],
    "Subject": "test",
    "TextPart": "",
    "HTMLPart": "",
    "InlinedAttachments": [],
}


attached = data["InlinedAttachments"]
for file in CONFIGPATH.iterdir():
    if file.suffix == ".png":
        with file.open("rb") as fh:  # open binary file in read mode
            file_64_encode = base64.standard_b64encode(fh.read())
        newinline = {
            "ContentType": "image/png",
            "Filename": file.name,
            "ContentID": file.stem,
            "Base64Content": file_64_encode.decode("ascii"),
        }
        attached.append(newinline)

data[
    "HTMLPart"
] = """
<img src="cid:LOGO"> 

<p style="font-size:14.0pt;line-height:106%;color:#ED7D31"> 

Te invitamos a participar del evento de difusión del software libre más grande en su tipo.</p>

<p> 
Te esperamos el sábado 27 de abril, desde las 10:00 en Arturo Illia 1055 (Resistencia-Chaco) para que 
puedas disfrutar de las 11 charlas, 3 talleres y un panel sobre trabajo remoto que tenemos preparado 
para que conozcas más sobre software libre.
</p>
<p>
Esta es tú oportunidad para conocer más, conocer a otros usuarios, resolver dudas e interrogantes, 
intercambiar opiniones y experiencias, asistir a charlas, talleres y otras actividades programadas 
para hacer de la jornada una verdadera fiesta de la emancipación tecnológica.
</p>
<p>
Podés ver todas las actividades en https://eventol.flisol.org.ar/events/flisol-resistencia-2019/.
</p>
<p>
Si te registrás en la página, entregamos certificados al e-mail que ingreses.
</p>
<p>
¡Te esperamos!
</p>

<img src="cid:PIE"> 
"""

data[
    "TextPart"
] = """
Te invitamos a participar del evento de difusión del software libre más grande en su tipo.

 

Te esperamos el sábado 27 de abril, desde las 10:00 en Arturo Illia 1055 (Resistencia-Chaco) 
para que puedas disfrutar de las 11 charlas, 3 talleres y un panel sobre trabajo remoto que 
tenemos preparado para que conozcas más sobre software libre.


Esta es tú oportunidad para conocer más, conocer a otros usuarios, resolver dudas e interrogantes, 
intercambiar opiniones y experiencias, asistir a charlas, talleres y otras actividades programadas 
para hacer de la jornada una verdadera fiesta de la emancipación tecnológica.

 

Podés ver todas las actividades en https://eventol.flisol.org.ar/events/flisol-resistencia-2019/.

 

Si te registrás en la página, entregamos certificados al e-mail que ingreses.

 

¡Te esperamos!"""

data["Subject"] = "Te invitamos a participar en el nuevo Flisol 2019"

with open("email.yaml", "w", encoding="utf-8") as fh:
    fh.write(yaml.safe_dump(data))
