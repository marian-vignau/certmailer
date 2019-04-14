
from mailjet_rest import Client
import base64
import json
import pprint

with open("data/credentials.json") as cred:
    config = json.load(cred)

def load_attachment():
    file_name = 'deer.gif'
    with open("data/" + file_name, 'rb') as fh: #open binary file in read mode
        file_64_encode = base64.standard_b64encode(fh.read())
    return {"ContentType": "IMAGE/GIF",
                "Filename": file_name,
                "Base64Content": file_64_encode.decode("ascii")
            }


def format_mail():
    data = {
      'Messages': [
                    {
                            "From": config["from"],
                            "To": [
                                    {
                                            "Email": "ariadnepoemas@gmail.com",
                                            "Name": "passenger 1"
                                    }
                            ],
                            "Subject": "Your email flight plan!",
                            "TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!",
                            "HTMLPart": "<h3>Dear passenger 1, welcome to Mailjet!</h3><br />May the delivery force be with you!",
                            'Attachments': [load_attachment()]
                    }
            ]
    }
    return data


def sendmail(data):
    keys = (config["keys"]["api_key"], config["keys"]["api_secret"])
    mailjet = Client(auth=keys, version='v3.1')
    result = mailjet.send.create(data=data)
    return result


if __name__ == "__main__":
    data = format_mail()
    result = sendmail(data)
    pprint.pprint(result.status_code)
    pprint.pprint(result.json())