# iDigPhylo Project Proposal

## Team Members

Matthew Collins

## Abstract

The iDigBio project is a 10 year National Science Foundation funded project to
digitize the natural history museum collections in the United States. The hub
of the project is hosted at the Florida Museum of Natural History at the
University of Florida.

There are currently over 45 million specimen records in the central database.
Many of these records include genetic sequence information in their comments
and metadata. This project aims to create 
an automated interface for generating phylogentic trees from genetic sequence 
data linked from specimen records in iDigBio. 

## Action Plan

Genetic sequences for building trees will be sourced from GenBank sequences.
Limited work has been done to link specimen and sequence information in iDigBio
so that will be a significant part of the data collection effort.

Appropriate phylogentic tree building tools will be used to align the sequences
and build trees. One candidate software package is MEGA which is freely available
and scriptable. Processing will be paralellized to the extent possible in the
packages and run on the most appropriate server hardware available from EC2 or
similar resources.

A web service will be constructed that accepts searches for specimen records in
the same format as the iDigBio API and returns constructed trees in a format 
suitable for viewing in existing phylogentic tree viewing software used by 
biologists.

Constructed trees will be compared to published trees from www.treebase.org or
phylomedb.org, online repositories for published trees, both visually and 
numerically using  geodesic distance. An explanation of differences due to 
differing input data and computation methods will be made.

## Workload Distribution

All work will be performed by Matthew Collins.

## References

GitHub, 'idigbio-api-hackathon/idigbio_sequences', 2015. [Online]. Available: https://github.com/idigbio-api-hackathon/idigbio_sequences. [Accessed: 11- Oct- 2015].

B. Hall, 'Building Phylogenetic Trees from Molecular Data with MEGA', *Molecular Biology and Evolution*, vol. 30, no. 5, pp. 1229-1235, 2013.

G. Jolley-Rogers, T. Varghese, P. Harvey, N. dos Remedios and J. Miller, 'PhyloJIVE: Integrating biodiversity data with the Tree of Life', *Bioinformatics*, vol. 30, no. 9, pp. 1308-1309, 2014.

A. Matsunaga, A. Thompson, R. Figueiredo, C. Germain-Aubrey, M. Collins, R. Beaman, B. MacFadden, G. Riccardi, P. Soltis, L. Page and J. Fortes, 'A Computational- and Storage-Cloud for Integration of Biodiversity Collections', *2013 IEEE 9th International Conference on e-Science*, 2013.