import json
import time
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True)
    job_id = Column(String(64))
    prog = Column(String(24))
    fn = Column(String(24))
    result = Column(Text)
    timestamp = Column(DateTime, nullable=False)
    starttime = Column(DateTime)

class Sequence(Base):
    __tablename__ = "sequences"
    id = Column(Integer, primary_key=True)
    idb_uuid = Column(String(36))
    gb_id = Column(String(36))
    seq = Column(Text)
    can_use = Column(Boolean)

class Test(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Database:

    def __init__(self):
        with open("/home/mcollins/db.json", "r") as cred_file:
            creds = json.load(cred_file)
        self.conn = create_engine(creds["connection_str"])
        Base.metadata.create_all(self.conn)
        Base.metadata.bind = self.conn
        DBSession = sessionmaker(bind=self.conn)
        self.sess = DBSession()

    def mk_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    db = Database()
    new_test = Test(id=123, name="Test is ok")
    db.sess.add(new_test)
    db.sess.commit()
    test = db.sess.query(Test).all()[0]
    print test.name
    db.sess.delete(test)
    db.sess.commit()
