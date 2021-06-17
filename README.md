# Multi-thread-DNAworks
 DNAworks mutithread processing on single node.

### Requirement
- [DNAworks v3.2.4 David Hoover May 04, 2017](https://github.com/davidhoover/DNAWorks)
- Add dnaworks in your environment variables. 
- python2.7 or later

### Usage
Firstly, we need to prepare an input file in fasta format containing all the protein sequences we needed.
```shell
python [PATH]/dnaworks_multiSeq.py -j<number of threads> -i <INPUT> -a <OUTPUT in fasta format> -d <OUTPUT only dna sequence> -g <OUTPUT log file>
```
For more complete information：```python [PATH]/dnaworks_multiSeq.py -h ```
