#!/usr/bin/python
from __future__ import absolute_import

import sys
from ete2 import PhyloTree

if __name__ == "__main__":
    t = sys.argv[1]
    pt = PhyloTree(t)
    pt.render(sys.argv[2])
