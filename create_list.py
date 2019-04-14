"""
Create a csv list of candidates to do a certificate
"""


import yaml
from pathlib import Path
import unicodedata

filenames = {"Activity": None,
             "Attendee": None,
             "Collaborator": None,
             "Installer": None}

def searchfiles():
    data_dir = Path().cwd().joinpath("data")


    for file in data_dir.iterdir():
        if file.suffix == ".yaml":
            for key in filenames.keys():
                if file.name.startswith(key):
                    filenames[key] = file


class MyList():
    def __init__(self):
        self.list = {}
        self.add_to_list("Attendee", "Asistente")
        self.add_to_list("Installer", "Instalador")
        self.add_to_list("Collaborator", "Colaborador")
        self.activity("Disertante")

    def extract_event_user(self, item):
        user = {}
        prefix = "event_user__user__"
        for key, value in item.items():
            if key.startswith(prefix):
                user[key[len(prefix):]] = value
            else:
                user[key] = value
        return user

    def add_to_list(self, filename, category):
        with open(filenames[filename]) as fh:
            for item in yaml.safe_load(fh.read()):
                self.add_person(item, category)

    def add_person(self, item, category):
        user = self.extract_event_user(item)
        if user["email"] in self.list:
            person = self.list[user["email"]]
            person["category"].append(category)

        else:
            user["category"] = [category]
            user["name"] = self.unaccented(user.get("first_name", ""), user.get("last_name", ""))
            self.list[user["email"]] = user

    def activity(self, category):
        with open(filenames["Activity"]) as fh:
            for item in yaml.safe_load(fh.read()):
                for speaker in item["speakers_names"].split(","):
                    search_key = self.unaccented(speaker)
                    if not self.match_speakers(search_key, category):
                        key = search_key.replace(" ", "_")
                        person = {
                            "category": [category],
                            "last_name": speaker.strip(),
                            "name": search_key,
                            "email": key,
                            "registration_date": item["updated_at"]
                        }

                        self.list[key] = person

    def match_speakers(self, key, category):
        for email, item in self.list.items():
            name = item["name"].split()
            j = 0
            for word in key.split():
                if word in name:
                    j += 1
            if j > 1:
                self.list[email]["category"].append(category)
                return True
        return False

    def unaccented(self, *parts):
        s = " ".join(parts)
        s = s.lower()

        unaccented = ''.join(c for c in unicodedata.normalize('NFD', s)
                             if unicodedata.category(c) != 'Mn')
        return unaccented

if __name__ == "__main__":
    import pprint
    searchfiles()
    do = MyList()
    pprint.pprint(do.list)



