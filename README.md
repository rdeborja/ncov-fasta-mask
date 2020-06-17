# ncov-fasta-mask

The `ncov-fasta-mask` package provides a suite of tools for the
of consensus FASTA files for the nCoV project.

The package was used to investigate potential sample swaps from
contaminated primer pools.  The tool takes a BED file containing
primer regions, the FASTA file to mask, and patterns for the pool
of interest.

## Installation
After downloading the repository, the package can be installed using `pip`:
```
git clone git@github.com:rdeborja/ncov-fasta-mask.git
cd ncov-fasta-mask
pip install .
```


## Usage
The library consists of several functions that can be imported.
```
import ncov.fasta.mask as mask
```


### Top level scripts
The `bin` directory has an executable wrapper script that can be used to
create masked FASTA files.

```
bin/mask_fasta_from_bed.py --fasta <sample>.consensus.fa
                           --bed <primer>.bed
                           --pool <pattern in ID identifying pool>
                           --output <name of output>.fa
```


# License
MIT
