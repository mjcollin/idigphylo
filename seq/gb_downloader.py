from __future__ import absolute_import
import sys
sys.path.append("../lib")
import urllib2
from database import Database, Sequence


db = Database()
to_do = db.sess.query(Sequence).\
        filter(~Sequence.gb_id.like("EU%")).\
        filter(Sequence.seq == None).first()
id = to_do.gb_id
print id

#id = "EU180285"
try:
    response = urllib2.urlopen('http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={0}&rettype=fasta&retmode=text'.format(id))
    fasta = response.read()
    #print (fasta)
    seq = "".join(fasta.split('\n')[1:])
    #print seq
    to_do.seq = seq
except:
    to_do.seq = "failed"

db.sess.commit()
