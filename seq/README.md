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