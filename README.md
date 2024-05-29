# phyluce-techniques

A dump of scripts and techniques used for working with phyluce and its output files.



# Processing of UCE alignment for SWSC

## Generate the concatenated alignment in nexus format

**Phyluce 1.6.x**

```bash
phyluce_align_format_nexus_files_for_raxml \
    --alignments mafft-nexus-min-70per-taxa \
    --output mafft-nexus-min-70per-taxa/ \
    --charsets \
    --nexus
```

**Phyluce 1.7.x**

```bash
phyluce_align_concatenate_alignments \
    --alignments mafft-nexus-min-70per-taxa \
    --output mafft-nexus-min-70per-taxa \
    --nexus
```

```bash
$ ls mafft-nexus-min-70per-taxa
mafft-nexus-min-70per-taxa.nexus
```

`cd` in to the output directory

```bash
cd mafft-nexus-min-70per-taxa
```

## Remove the `charpartition` line from the nexus file

If you don't remove the `charparition` line from the nexus file, SWSCEN.py will give an error about a corrupt nexus file.

```bash
grep -v charpartition mafft-nexus-min-70per-taxa.nexus > mafft-nexus-min-70per-taxa.nexus.tmp
mv mafft-nexus-min-70per-taxa.nexus.tmp mafft-nexus-min-70per-taxa.nexus
```

## Run SWSC on the nexus file

`swsc.job`:

```bash
# /bin/sh
# ----------------Parameters---------------------- #
#$ -S /bin/sh
#$ -q mThC.q
#$ -l mres=8G,h_data=8G,h_vmem=64G
#$ -cwd
#$ -j y
#$ -N swsc
#$ -o swsc.log
#
# ----------------Modules------------------------- #
module load bio/partitionfinder/UCE_SWSC
#
# ----------------Your Commands------------------- #
#
echo + `date` job $JOB_NAME started in $QUEUE with jobID=$JOB_ID on $HOSTNAME
echo + NSLOTS = $NSLOTS

#
SWSCEN.py mafft-nexus-min-70per-taxa.nexus ./

#
echo = `date` job $JOB_NAME done
```

## Convert .cfg `[data_blocks]` section to nexus partitions

```bash
$ cfg_to_nex.sh mafft-nexus-min-70per-taxa.nexus_entropy_partition_finder.cfg
Converts the .cfg output from SWSC to a nexus partition file for use in
IQTREE or raxml
Input: mafft-nexus-min-70per-taxa.nexus_entropy_partition_finder.cfg
Output: partitions.nex
Done

$ head -n 5 partitions.nex
#nexus
begin sets;
charset uce-10.nexus_left = 1-79;
charset uce-10.nexus_core = 80-129;
charset uce-10.nexus_right = 130-382;

$ tail -n 5 partitions.nex
charset uce-2144.nexus_right = 109157-109369;
charset uce-2148.nexus_left = 109370-109422;
charset uce-2148.nexus_core = 109423-109473;
charset uce-2148.nexus_right = 109474-109688;
end;
```
