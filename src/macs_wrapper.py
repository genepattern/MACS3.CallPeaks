# Input BAM File, optional control file

#!/usr/bin/env python3

import sys
import argparse
from io import StringIO
import os
import subprocess
from subprocess import PIPE, STDOUT
import time

### Code for Inputs
parser = argparse.ArgumentParser()

### Module Required Arguments
parser.add_argument("-treatment", "--treatment",
                    type = str,
                    help ="Name of the ChIP tag file to be read")

parser.add_argument("-type", "--type",
                    type = str,
                    help = "Type of Analysis")

# ~~~~Optional Arguments~~~~~ #
parser.add_argument("-control", "--control",
                    type = str,
                    help ="Name of the control file to be read")
parser.add_argument("-name", "--name",
                    type=str,
                    help="The name string of the experiment used as the basename for output files")
# parser.add_argument("-od", "--outdir",
#                     type=str,
#                     help="Specified Folder for Output Files to be saved to")
parser.add_argument("-format", "--format",
                    type=str,
                    help="Format of the tag file")
parser.add_argument("-gsize", "--gsize",
                    type=str,
                    help="Mappable Genome Size")
parser.add_argument("-tsize", "--tsize",
                    type=int,
                    help="Size of Sequencing Tags")
parser.add_argument("-qvalue", "--qvalue",
                    type=float,
                    help="The q-value (minimum FDR) cutoff to call significant regions")
parser.add_argument("-pvalue", "--pvalue",
                    type=float,
                    help="The p-value cutoff to call significant regions. If specified, MACS3 will use p-value instead of q-value")              

# min-length to minlength
parser.add_argument("-minlength", "--minlength",
                    type=int,
                    help="Specifies the minimum length if a called peak")

# max-gap to maxgap
parser.add_argument("-maxgap", "--maxgap",
                    type=str,
                    help="Specifies the maximum gap between nearby peaks, where two nearby peaks smaller than max-gap will be merged as one")

parser.add_argument("-nolambda", "--nolambda",
                    type=str,
                    help="Specifies if MACS uses background lambda as local lambda")
parser.add_argument("-slocal", "--slocal",
                    type=int,
                    help="This parameter checks the small local region around peak regions to calculate maximum lambda as local lambda")
parser.add_argument("-llocal", "--llocal",
                    type=int,
                    help="This parameter checks the large local region around peak regions to calculate maximum lambda as local lambda")
parser.add_argument("-nomodel", "--nomodel",
                    type=str,
                    help="While on, MACS bypasses building the shifting model")

# ext-size to extsize
parser.add_argument("-extsize", "--extsize",
                    type=str,
                    help="While on, MACS extends reads in the 5'->3' direction to fix-sized fragments. This option is only valid when '--nomodel' is set or when MACS fails to build model and '--fix-bimodal' is on")
parser.add_argument("-shift", "--shift",
                    type=int,
                    help="Sets an arbitrary shift in base pairs. If '--nomodel' is set, MACS will use this value to move cutting ends (5') then apply '--extsize' in the 5'->3' direction or 3'->5' direction if the value is negative")

# KEEP-DUP, TO KEEPDUP
parser.add_argument("-keepdup", "--keepdup",
                    type=str,
                    help="Specifies the number of duplicate tags kept at the exact same location")
parser.add_argument("-broadregion", "--broad",
                    type=str,
                    help="While on, MACS will try to composite broad regions by putting nearby highly enriched regions into a broad region with a loose cutoff controlled by '--broad-cutoff'")

# broad-cutoff to broadcutoff
parser.add_argument("-broadcutoff", "--broadcutoff",
                    type=float,
                    help="Cutoff for broad region. If '-p' is set, this is the p-value cutoff")

# scale-to to scaleto
parser.add_argument("-scaleto", "--scaleto",
                    type=str,
                    help="Specifies which dataset is scaled, where 'large' linearly scales the smaller dataset to the same depth as the large dataset and 'small' scales the larger dataset towards the smaller dataset")

parser.add_argument("-bdg", "--bdg",
                    type=str,
                    help="While on, MACS stores fragment pileup and control lambda in bedGraph files")

# call-summits to callsummits
parser.add_argument("-callsummits", "--callsummits",
                    type=str,
                    help="While on, MACS will reanalyze the shape of the signal profile to deconvolve subpeaks within each peak. The output subpeaks of a big peak region will have the same peak boundaries, different scores and peak summit position")

# buffer-size to buffersize
parser.add_argument("-buffersize", "--buffersize",
                    type=int,
                    help="MACS uses a buffer size for incrementally increasing array size to store read alignment information for each chromosome.")

parser.add_argument("-seed", "--seed",
                    type=int,
                    help="Set random seed while sampling data")

args = parser.parse_args()

buff = StringIO()

buff.write("macs3 callpeak -t")

file_list = args.treatment

# Treatment
if file_list.endswith(".txt"):
    with open(file_list) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for x in content:
        buff.write(" ")
        buff.write(x)
else:
    buff.write(" ")
    buff.write(file_list)

# Control
if args.control:
    buff.write(" -c ")
    buff.write(args.control)

# Output Name
if args.name:
    buff.write(" -n ")
    buff.write(args.name)

# Tag File Format
if (args.format) or (args.type):
    buff.write(" -f ")
    if args.format:
        pass
    else:
        args.format = "BAM"
    buff.write(args.format)

# Genome Size
if args.gsize:
    buff.write(" -g ")
    buff.write(args.gsize)

# Tag Size
if args.tsize:
    buff.write(" -s ")
    buff.write(str(args.tsize))

# Q-value
if (args.qvalue) or (args.type):
    buff.write(" -q ")
    if args.qvalue:
        pass
    else:
        args.qvalue = 0.01
    buff.write(str(args.qvalue))

# P-value
if args.pvalue:
    buff.write(" -p ")
    buff.write(str(args.pvalue))

# Min-length
if args.minlength:
    buff.write(" --min-length=")
    buff.write(str(args.minlength))

# Max-Gap
if args.maxgap:
    buff.write(" --max-gap=")
    buff.write(str(args.maxgap))

# No Lambda
if args.nolambda:
    buff.write(" --nolambda")

# Small Local
if args.slocal:
    buff.write(" --slocal=")
    buff.write(str(args.slocal))

# Large Local
if args.llocal:
    buff.write(" --llocal=")
    buff.write(str(args.llocal))

# No Model
if (args.nomodel) or (args.type):
    buff.write(" --nomodel")

# Extension Size
if args.extsize:
    buff.write(" --extsize=")
    buff.write(str(args.extsize))

# Shift
if (args.shift) or (args.type):
    buff.write(" --shift=")
    if args.shift:
        pass
    else:
        args.shift = -100
    buff.write(str(args.shift))

# Keep Dup
if (args.keepdup) or (args.type):
    buff.write(" --keep-dup=")
    if args.keepdup:
        pass
    else:
        args.keepdup = "all"
    buff.write(str(args.keepdup))

# Broad Peaks
if args.broad:
    buff.write(" --broad")

# Broad Cutoff
if args.broadcutoff:
    buff.write(" --broad-cutoff=")
    buff.write(str(args.broadcutoff))

# Scale To
if args.scaleto:
    buff.write(" --scale-to=")
    buff.write(str(args.scaleto))

# Bdg file
if (args.bdg) or (args.type):
    buff.write(" -B")

# Call Summits
if (args.callsummits) or (args.type):
    buff.write(" --call-summits")

# Buffer Size
if args.buffersize:
    buff.write(" --buffer-size=")
    buff.write(str(args.buffersize))

# Set Seed
if args.seed:
    buff.write(" --seed=")
    buff.write(str(args.seed))

command_str = buff.getvalue()
print(command_str)

subprocess = subprocess.Popen(command_str, shell = True, stdout=PIPE)
subprocess_return = subprocess.stdout.read()
print(subprocess_return)
