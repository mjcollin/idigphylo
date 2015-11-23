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

## Good test case

1. Sequence ID in iDigBio
2. Search that returns the records w/ sequences
3. Not too many sequences or a filterable amount
4. Sequences types match and can be aligned
5. Tree availible for comparision in treebase