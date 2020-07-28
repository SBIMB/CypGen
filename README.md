# CypGen
Calling human cytochrome P450 star alleles by leveraging genome graph-based variant detection.

Model gene: CYP2D6 (Support for more CYP genes to be added soon)

CypGen is built using [Nextflow](https://www.nextflow.io), a workflow management system that facilitates parallelisation, scalability, reproducibility and portability of pipelines via [`Docker`](https://docs.docker.com) and [`Singularity`](https://sylabs.io/) technologies.

Maintainer: David Twesigomwe (twesigomwedavid@gmail.com)

## Getting started

The following are required to run the CypGen pipeline;

1. Prerequisite software
    - [`Nextflow`](https://nf-co.re/usage/installation) (preferably v18.x or higher)
    - [`Singularity`](https://sylabs.io/) (v2.3.x or higher) or [`Docker`](https://docs.docker.com)
    
Singularity is highly recommended especially for running the pipeline in an HPC environment running Linux OS. Docker desktop is recommended for MacOS users intending to run the pipeline on a local machine.

2. Whole genome sequence (WGS) data
    - Indexed BAM/CRAM files
    
3. Reference genome
    - hg19, b37, or hg38
    
Note: For a full description of the differences among reference genomes, please check out this [`Documentation`](https://gatk.broadinstitute.org/hc/en-us/articles/360035890711-GRCh37-hg19-b37-humanG1Kv37-Human-Reference-Discrepancies) by the GATK team. For the purpose of using this pipeline, if the GRCh37 reference genome you are using has contigs that start with 'chr' (i.e. chr1, chr2, ..., chrX, chrM, ...), use the hg19 option. You should use the b37 option if the contigs in the reference genome do not have 'chr' (i.e. 1, 2, ..., X, MT). For GRCh38, the hg38 option is sufficient.

### Installation

##### Nextflow:

Install Nextflow by running the following command (Skip if you have Nextflow installed already):

```bash
curl -fsSL get.nextflow.io | bash
```

Move the `nextflow` launcher (installed in your current directory) to a directory in your $PATH e.g. $HOME/bin

```bash
mv nextflow $HOME/bin
```

(The full Nextflow documentation can be found [here](https://www.nextflow.io))

##### Singularity or Docker:

For Singularity installation, please refer to the excellent documentation [here](https://sylabs.io/guides/3.0/user-guide/installation.html)). Ensure that your Singularity installation allows user defined binds - set by system administrator (See [Singularity config file](https://sylabs.io/guides/3.0/user-guide/installation.html) documentation) 


For Docker installation, please refer to the excellent documentation [here](https://docs.docker.com/get-docker))

##### CypGen:

Clone the CypGen repository by running the following command:

```bash
git clone https://github.com/twesigomwedavid/CypGen.git && cd CypGen
```


### Running CypGen on the provided test dataset(s) using Singularity

The following steps assume that;
    - CypGen is your current working directory
    - Nextflow and Singularity are already installed


##### For execution on local machine or single cluster node

```bash
nextflow run main.nf -profile standard -c tests/config/test.config
```

##### For execution on SLURM scheduler 

```bash
nextflow run main.nf -profile slurm -c tests/config/test.config
```


#### Expected output

The expected output file (SIM001_2d6.alleles) for test dataset SIM001.bam will be found in the ./results directory. It should contain the following; 

```
--------------------------------------------

CYP2D6 Star Allele Calling with CypGen

--------------------------------------------

CN = 2


Core variants:
42126611~C>G~1/1;42127608~C>T~0/1;42127941~G>A~1/1;42129132~C>T~0/1;42129770~G>A~0/1


Candidate alleles:
['17.v1_29.v1']


Result:


*17/*29

```
