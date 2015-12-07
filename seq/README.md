# Finding sequences in iDigBio

Prior work in the hackathon by Mike 

https://github.com/idigbio-api-hackathon/idigbio_sequences/

He only applied a regex to the data.dwc:associatedSequences field which 
currently has ~23,441 records but not all have sequence ids:
    
http://search.idigbio.org/v2/search/records/?rq={%22data.dwc:associatedSequences%22:{%22type%22:%22exists%22}}

So what would happen if we tried his regex on other fields?

pattern = re.compile("[a-zA-Z]{1,2}\-?_?\d{5,6}")

Probably a lot of false positives. What else could we look for? 

1. www.ncbi.nlm.nih.gov/nuccore
2. Primary knowledge: http://www.ncbi.nlm.nih.gov/Sitemap/samplerecord.html

## Just build a regex evaluator?

Input: JSON with list of fields and list of sequences
Output: record ID, regex, field, matching value (can be multiples)

What recordset to test it on?

http://search.idigbio.org/v2/summary/top/records/?top_fields=%22recordset%22&rq=%7B%22data.dwc:associatedSequences%22:%7B%22type%22:%22exists%22%7D%7D

Try http://portal.idigbio.org/portal/recordsets/edbd0bc4-c292-426b-9a6c-44bbccab2d11

## Status

Runs on small data sets ~8 MB but with large data sets, Spark builds a stage for each 128MB of input and runs them sequentially. Not sure what it's up to.

time spark-submit --executor-cores 5 --num-executors 18 --executor-memory 9G idb_regex.py "hdfs://cloudera0.acis.ufl.edu:8020/user/mcollins/test_data/occurrence_md.csv" "id" "dwc:associatedSequences" "all_raw_ass_seq.csv" '([a-zA-Z]+)'

time spark-submit --executor-cores 5 --num-executors 18 --executor-memory 9G idb_regex.py "hdfs://cloudera0.acis.ufl.edu:8020/user/mcollins/test_data/occurrence_raw_edbd.csv" "coreid" "dwc:associatedSequences" "edbd0bc4-c292-426b-9a6c-44bbccab2d11.sample" '[a-zA-Z]{1,2}\-?_?\d{5,6}'
