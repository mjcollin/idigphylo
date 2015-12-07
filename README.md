# idigphylotree
Phylogenetic tree building based on gene sequences linked in iDigBio specimen records


## MrBayes Installation on Ubuntu 14.04

http://downloads.sourceforge.net/project/mrbayes/mrbayes/3.2.5/mrbayes-3.2.5.tar.gz?r=http%3A%2F%2Fmrbayes.sourceforge.net%2Fdownload.php&ts=1447378701&use_mirror=skylineservers

Do later when need parallel - git clone https://github.com/beagle-dev/beagle-lib.git


sudo apt-get install openmpi-bin openmpi-doc libopenmpi-dev
cd src/
autoconf
./configure --with-beagle=no --enable-mpi=yes
make
mv mb ../bin/

And test with the first tutorial from the manual

FIXME: This still runs as one thread - might be compilation, might be libraries, might be model

### Ref

http://sourceforge.net/p/mrbayes/mailman/message/34509537/
https://pascualanaya.wordpress.com/2014/09/08/compiling-and-working-with-mpi-version-of-mrbayes-3-2-2/

## Good test case

1. Sequence ID in iDigBio
2. Search that returns the records w/ sequences
3. Not too many sequences or a filterable amount
4. Sequences types match and can be aligned
5. Tree availible for comparision in treebase

## Directory Structure

1) seq/ - Spark code used for extracting GenBank sequence identifiers from iDigBio data dumps. Builds the uuid:seqid linking table used by the genbank worker
1) workers/
  1) sequence/ - Celery worker that accepts iDigBio uuids and enqueues tasks 
  for the align worker with sequences
  1) align/ - Celery worker that accepts sequences and aligns them and enqueues
  tasks for the tree worker
  1) tree/ - Celery workder that accepts aligned sequences and constructs trees
  that are then stored in Postgresql
1) api/ - Python API code
1) web/ - Web root of site (put on gh-pages branch?)

# For ClustalOmega building
sudo apt-get install libargtable2-0 libargtable2-dev

iDigBio Python package pulled from github, fixes beta issue:
git clone git@github.com:iDigBio/idigbio-python-client.git
cd idigbio-python-client
sudo python setup.py install


# Api

pip install flask

tree/build

tree/view

Visualization
apt-get install python-numpy python-qt4 python-lxml
 sudo pip install ete2
 
 Need X server to render:
     https://github.com/jhcepas/ete/issues/101
     sudo apt-get install xvfb
     then run `xvfb-run python api_view_stub.py`
     
Trouble parsing nexus files
apt-get install bioperl

