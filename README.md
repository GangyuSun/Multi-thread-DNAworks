# Multi-thread-DNAworks
 DNAworks -- Mutithreads processing on single node.

### Requirement
- [DNAworks v3.2.4 David Hoover May 04, 2017](https://github.com/davidhoover/DNAWorks)
- Add dnaworks in your environment variables. 
- python2.7 or later

### Usage
Firstly, we need to prepare an input file in fasta format containing all the protein sequences we needed.
 And run the following command：
```shell
python [PATH]/dnaworks_multiSeq.py -j<number of threads> -i <INPUT> --codon "E. coli" -a <OUTPUT in fasta format> -d <OUTPUT only dna sequence> -g <OUTPUT log file>
```
Notice: The content indicated by the --codon directive MUST be enclosed in quotation marks.The quotes can be single or double. You can also specify your own DNAworks' directives under the [dnaworks_proc] function, in this script I just specified the basic directives for simply using. 

For more complete information：```python [PATH]/dnaworks_multiSeq.py -h ```
