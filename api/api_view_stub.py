from __future__ import absolute_import

import sys
sys.path.append("../lib")

from subprocess import call, check_output
from database import Database, Result
from ete2 import PhyloTree


t = '(1[&prob=1.00000000e+00,prob_stddev=0.00000000e+00,prob_range={1.00000000e+00,1.00000000e+00},prob(percent)="100",prob+-sd="100+-0"]:3.446601e-01[&length_mean=3.64555202e-01,length_median=3.44660100e-01,length_95%HPD={2.15232100e-01,5.50883100e-01}],3[&prob=1.00000000e+00,prob_stddev=0.00000000e+00,prob_range={1.00000000e+00,1.00000000e+00},prob(percent)="100",prob+-sd="100+-0"]:3.321322e-01[&length_mean=3.46470962e-01,length_median=3.32132200e-01,length_95%HPD={2.23491200e-01,5.48587200e-01}],(2[&prob=1.00000000e+00,prob_stddev=0.00000000e+00,prob_range={1.00000000e+00,1.00000000e+00},prob(percent)="100",prob+-sd="100+-0"]:4.987927e-02[&length_mean=5.12340896e-02,length_median=4.98792700e-02,length_95%HPD={1.81164700e-03,9.17682200e-02}],4[&prob=1.00000000e+00,prob_stddev=0.00000000e+00,prob_range={1.00000000e+00,1.00000000e+00},prob(percent)="100",prob+-sd="100+-0"]:5.190217e-02[&length_mean=5.44534209e-02,length_median=5.19021700e-02,length_95%HPD={9.63370400e-03,1.03071000e-01}])[&prob=1.00000000e+00,prob_stddev=0.00000000e+00,prob_range={1.00000000e+00,1.00000000e+00},prob(percent)="100",prob+-sd="100+-0"]:5.373589e-01[&length_mean=5.59541552e-01,length_median=5.37358900e-01,length_95%HPD={3.29338500e-01,8.63095700e-01}]);'
#t = '((1,2),3,4);'
t = '(00060e1b_9ca1_4e55_bb8a_1852bf6e85c0:3.446601e-01,00041678_5df1_4a23_ba78_8c12f60af369:3.321322e-01,(00087574_9941_49b2_a3db_92a48ceea3aa:4.987927e-02,00072caf_0f24_447f_b68e_a20299f6afc7:5.190217e-02):5.373589e-01);'

# Load a result
db = Database()
job_id = "7f63fc71-4a0f-4b91-a9f3-909bf95c1ae0"
trees = db.sess.query(Result).\
        filter(Result.job_id==job_id).\
        filter(Result.prog=="mrbayes").first()
aligned = db.sess.query(Result).\
          filter(Result.job_id==job_id).\
          filter(Result.prog=="clustalo").first()

if trees is not None:
    # Convert NEXUS tree to Newick format with BioPerl script, was the only
    # thing I could find that would parse a MrBayes tree file.
    t = check_output("echo '{0}' | /usr/bin/bp_nexus2nh".format(trees.result), shell=True) 

    s = aligned.result

    # Create tree, have to use a process call to run PhyloTree.render()
    # inside an X framebuffer since it uses Qt4 to render.
    # https://github.com/jhcepas/ete/issues/101
    #pt = PhyloTree(t)
    #pt.render('/var/www/html/treeview/test.svg')
    call("/usr/bin/xvfb-run bin/ete_render.py '{0}' '{1}' '{2}'".format(t, s, '/var/www/html/treeview/test.svg'), shell=True)

# Look


# Generate SVG to web dir
