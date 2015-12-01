import json
import sqlalchemy as sqla

class Db:

    def connect(self):
        try:
            with open("../db.json", "r") as cred_file:
                creds = json.load(cred_file)
                self.conn = sqla.create_engine(creds["connection_str"])
            return True
        except:
            return False

if __name__ == "__main__":
    db = Db()
    print db.connect()
