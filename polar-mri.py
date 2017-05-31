#!/usr/bin/python

# default colors:
dflt_color_norm = 'grey'
dflt_color_dev  = '#2E6DA4'     # bluish
groups = \
[
    {
        'color_dev': '#5cb85c',     # greenish
        'White matter':
        [
            {
                'Frontal': [ 'RightInsulaWhiteMatter', 'RightFrontalWhiteMatter', 'LeftFrontalWhiteMatter' ],

                # Override default group color for each subgroup like this:
                #   'color_dev': '#5cb85c',      # greenish
                #   'color_norm': '#5cb85c',     # greenish
            },
            {
                'Temporal': [ 'RightTemporalWhiteMatte', 'LeftTemporalWhiteMatter' ],
            },
            {
                'Parietal': [ 'RightParietalWhiteMatter', 'LeftParietalWhiteMatter' ],
            },
            {
                'Occipital': [ 'RightOccipitalWhiteMatter', 'LeftOccipitalWhiteMatter' ],
            },
            {
                'Insula': [ 'LeftInsulaWhiteMatter' ],
            },
            {
                'Cingulate': [ 'RightCingulateWhiteMatter', 'LeftCingulateWhiteMatter' ],
            },
            {
                'Corpus\nCallosum': [ 'CorpusCallosum' ], 
            }
        ],
    },
    {
        'color_dev': '#d9534f',     # redish
        'Cerebellum':
        [
            {
                'Vermis': [ 'Vermis' ],
            },
            {
                'Deep nuclei': [ 'Deep_nuclei' ],
            },
            {
                'Anterior': [ 'Anterior' ],
            },
            {
                'Posterior': [ 'Posterior' ],
            },
            {
                'Superior Posterior': [ 'Superior_Posterior' ],
            },
            {
                'Inferior Posterior': [ 'Inferior_Posterior' ],
            },
        ],
    },
    {
        'color_dev': '#f0ad4e',     # orangy
        'Subcortical Regions' :
        [
            {
                'Accumbens': [ 'RightAccumbensArea', 'LeftAccumbensArea' ],
            },
            {
                'Amygdala': [ 'RightAmygdala', 'LeftAmygdala' ],
            },
            {
                'Pons': [ 'Pons' ],
            },
            {
                'BrainStem': [ 'BrainStem' ],
            },
            {
                'Caudate': [ 'RightCaudate', 'LeftCaudate' ],
            },
            {
                'Hippocampus': [ 'RightHippocampus', 'LeftHippocampus' ],
            },
            {
                'Pallidum': [ 'RightPallidum', 'LeftPallidum' ],
            },
            {
                'Putame': [ 'RightPutame', 'LeftPutamen' ],
            },
            {
                'Thalamus': [ 'RightThalamusProper', 'LeftThalamusProper' ],
            },
            {
                'Ventral DC': [ 'Right Ventral DC', 'Left Ventral DC' ],
            },
            {
                'Basal\nForebrain': [ 'Left Basal Forebrain', 'Right Basal Forebrain' ],
            },
        ],
    },
    {
        'color_dev': '#2E6DA4',     # bluish
        'Cortical Regions' :
        [
            {
                'Frontal': [ 'Frontallobevolume', 'FRP' ],
            },
            {
                'Temporal': [ 'Temporallobevolume' ],
            },
            {
                'Parietal': [ 'Parietallobevolume' ],
            },
            {
                'Occipital': [ 'Occipitallobevolume' ],
            },
            {
                'Cingulate': [ 'Cingulatevolume' ],
            },
            {
                'Insula': [ 'Insulavolume' ],
            }
        ],
    },
]

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import itertools
import csv,sys
import numpy as np
csv.register_dialect('tab', delimiter='\t', quoting=csv.QUOTE_NONE)

def usage():
    print 'Usage: polar-mri.py [OPTIONS] <in.txt> <out.png|pdf|svgz>'
    print 'Options:'
    print '   -a, --abs-dev         Preserve sign of the deviation'
    sys.exit(1)

def usage_example():
    print "\nExample of valid input:"
    print "\tRightAccumbensArea  LeftAccumbensArea   RightAmygdala  etc.."
    print "\t0.5%                2.9%                33.1%          etc..\n"


abs_dev  = False
in_file  = None
out_file = None
if len(sys.argv) < 2: usage()
args = sys.argv[1:]
while len(args):
    if args[0]=='-a' or args[0]=='--abs-dev': 
        abs_dev = True
    elif in_file == None: in_file = args[0]
    elif out_file == None: out_file = args[0]
    else: usage()
    args = args[1:]

lines = open(in_file, 'rb').readlines()

if len(lines) != 2: 
    print "Error: expected two lines on input, got: ",len(lines)
    usage_example()
    sys.exit(1)

all_cols = lines[0].split('\t')
all_vals = lines[1].split('\t')

if len(all_cols) != len(all_vals): 
    print "Error: different number of fields in the two lines: ",len(all_cols)," vs ",len(all_vals)
    usage_example()
    sys.exit(1)

cols_hash = {}
for i in range(len(all_cols)):
    key = all_cols[i].strip()
    val = all_vals[i].strip().rstrip('%')
    try:
        val = float(val)/100.
    except:
        pass
        continue
    if abs_dev: val += 1
    else: val = 1 - abs(val)
    cols_hash[key] = val

ltmp  = []  # labels, can repeat multiple times
lbls  = []
xlbls = []
xvals = []
yvals = []
cols  = []
sgrp  = []
for hash in groups:
    color_dev  = dflt_color_dev
    color_norm = dflt_color_norm
    if 'color_dev' in hash: color_dev   = hash['color_dev']
    if 'color_norm' in hash: color_norm = hash['color_norm']
    for grp in hash:
        if grp=='color_dev': continue
        if grp=='color_norm': continue
        for shash in hash[grp]:
            for key in shash:
                for column in shash[key]:
                    if column not in cols_hash: continue
                    ltmp.append(key)
                    yvals.append(cols_hash[column])
                    sgrp.append(grp)
                    color = []
                    if 'color_dev' in shash: color.append(shash['color_dev'])
                    else: color.append(color_dev)
                    if 'color_norm' in shash: color.append(shash['color_norm'])
                    else: color.append(color_norm)
                    cols.append(color)

if len(yvals)==0: 
    print "No valid columns found!"
    usage_example()
    sys.exit()

width = 2*np.pi/len(yvals)
for i in range(len(yvals)):
    xvals.append(i*width)
beg = 0
while beg<len(ltmp):
    lbl = ltmp[beg]
    end = beg
    while end<len(ltmp) and ltmp[end]==lbl: end += 1
    xval = (xvals[beg]+xvals[end-1]+width)*0.5
    xlbls.append(xval)
    lbls.append(lbl)
    if beg==end: beg = end + 1
    else: beg = end


ax = plt.subplot(111, projection='polar')
bars = ax.bar(xvals, yvals, width=width, bottom=0.0)

ax.axes.get_xaxis().grid(False)
#ax.grid(False)
ax.spines['polar'].set_visible(False)       # do not draw axis border
ax.set_xticks([])
ax.set_rlabel_position(0)
ax.tick_params(axis='both', which='major', labelsize=9)

# Highlight tick at 1?
#   for g,t,l in zip(ax.get_ygridlines(),ax.get_yticks(),ax.get_yticklabels()):
#       if t==1:
#           #l.set_color('#D43F3A')
#           g.set_color('#D43F3A')
#           g.set_linewidth(2)
#           g.set_linestyle(':')

yticks = ax.get_yticks()    # to get the distance of labels right

# hide the outer grid circle and replace it with segments
leg = {}
g = ax.get_ygridlines()
g[-1].set_linestyle('none')
for i in range(len(yvals)):
    beg = i*width
    end = (i+1)*width
    ax.plot(np.linspace(beg, end, 10), np.ones(10), color=cols[i][0], linestyle='-', linewidth=4)
    leg[cols[i][0]] = sgrp[i]

leg_rect = []
leg_lbl  = []
for col in leg:
    rect = patches.Rectangle((0,0), 0.1, 0.1, color=col)
    leg_rect.append(rect)
    leg_lbl.append(leg[col])
plt.legend(leg_rect,leg_lbl,prop={'size':9},frameon=False,bbox_to_anchor=(0.98,0.98),bbox_transform=plt.gcf().transFigure)

for i in range(len(xlbls)):
    angle_rad = xlbls[i]
    angle_deg = angle_rad*180/np.pi
    ha  = "left"
    rot = angle_deg
    if angle_rad > np.pi/2 and angle_rad < np.pi*3/2.: 
        ha  = "right"
        rot = angle_deg - 180
    plt.text(angle_rad, yticks[-1]+0.1, lbls[i], size=9, horizontalalignment=ha, 
        verticalalignment="center", rotation=rot, rotation_mode='anchor')

for x,y,color,bar in zip(xvals, yvals, cols, bars):
    if abs(y-1) > 0.05:
        bar.set_facecolor(color[0])
        bar.set_edgecolor(color[0])
        bar.set_alpha(0.7)
    else:
        bar.set_facecolor(color[1])
        bar.set_edgecolor(color[1])
        bar.set_alpha(0.4)

plt.subplots_adjust(left=0.0,right=0.85,bottom=0.15,top=0.85)
plt.savefig(out_file)
plt.close()


