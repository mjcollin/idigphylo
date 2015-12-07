#!/usr/bin/python
from __future__ import absolute_import

import sys
from ete2 import PhyloTree

if __name__ == "__main__":
    t = sys.argv[1]
    s = sys.argv[2]
    out = sys.argv[3]

    pt = PhyloTree(t)
#    pt.link_to_alignment(alignment=s)
    pt.render(out)
