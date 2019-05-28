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
    "Subject": "Tu certificado por la participación en Flisol 2019",
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
<img src="cid:PIE"> 

<p style="font-size:14.0pt;line-height:106%;color:#ED7D31"> 
Agradecemos tu participación en Flisol 2019, sede Resistencia, el día 27 de abril de 2019.
</p>
<p>
Esta es tú oportunidad para conocer más, conocer a otros usuarios, resolver dudas e interrogantes, 
intercambiar opiniones y experiencias, asistir a charlas, talleres y otras actividades programadas 
para hacer de la jornada una verdadera fiesta de la emancipación tecnológica.
</p>
<p>
Es un placer anunciar que el día 29 de junio de 2019 10:00, en la sede Resistencia 
de la Universidad Tecnológica Nacional, Frech 414, se desarrollará el PyDayNEA 2019.
</p>
<p>
Un día completo de charlas y talleres sobre el lenguaje de programación Python.
</p>
<p>
¿Tienen algún tema y desean desarrollarlo? 
</p>
<p>
¿Les gusta el lenguaje python y quieren mostrar sus usos? ¡Esperamos sus propuestas! 
</p>
<p>
Registralas en https://eventos.python.org.ar/events/pydaynea2019/activity/proposal/
</p><p>
¡Te esperamos!
</p>


"""

data[
    "TextPart"
] = """
Agradecemos tu participación en Flisol 2019, sede Resistencia, el día 27 de abril de 2019.

Esta es tú oportunidad para conocer más, conocer a otros usuarios, resolver dudas e interrogantes, 
intercambiar opiniones y experiencias, asistir a charlas, talleres y otras actividades programadas 
para hacer de la jornada una verdadera fiesta de la emancipación tecnológica.

Es un placer anunciar que el día 29 de junio de 2019 10:00, en la sede Resistencia 
de la Universidad Tecnológica Nacional, Frech 414, se desarrollará el PyDayNEA 2019.

Un día completo de charlas y talleres sobre el lenguaje de programación Python.

¿Tienen algún tema y desean desarrollarlo? 

¿Les gusta el lenguaje python y quieren mostrar sus usos? ¡Esperamos sus propuestas! 

Registralas en https://eventos.python.org.ar/events/pydaynea2019/activity/proposal/

¡Te esperamos!

"""


with open("email.yaml", "w", encoding="utf-8") as fh:
    fh.write(yaml.safe_dump(data))
