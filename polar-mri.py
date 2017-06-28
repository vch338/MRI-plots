#!/usr/bin/python

# default colors:
dflt_color_norm = 'grey'
dflt_color_dev  = '#2E6DA4'     # bluish
groups = \
[
    {
        'color_dev': '#2E6DA4',     # bluish
        'Cortex' :
        [
            {
                'Frontal': [ 'Frontallobevolume' ],
            },
            {
                'Cingulate': [ 'Cingulatevolume' ],
            },
            {
                'Temporal': [ 'Temporallobevolume' ],
            },
            {
                'Insula': [ 'Insulavolume' ],
            },
            {
                'Parietal': [ 'Parietallobevolume' ],
            },  
            {
                'Occipital': [ 'Occipitallobevolume' ],
            },
	   ],
    },
    {
        'color_dev': '#5cb85c',     # greenish
        'White matter':
        [   
            {
                'Frontal': [ {'RightFrontalWhiteMatter':'R'}, {'LeftFrontalWhiteMatter':'L'} ],

                # Override default group color for each subgroup like this:
                #   'color_dev': '#5cb85c',      # greenish
                #   'color_norm': '#5cb85c',     # greenish
            },
            {
                'Cingulate': [ {'RightCingulateWhiteMatter':'R'}, {'LeftCingulateWhiteMatter':'L'} ],
            },
            {
                'Corpus\nCallosum': [ 'CorpusCallosum' ], 
            },
            {
                'Temporal': [ {'RightTemporalWhiteMatte':'R'}, {'LeftTemporalWhiteMatte':'L'} ],
            },
            { 
                'Insula': [ {'RightInsulaWhiteMatter':'R'}, {'LeftInsulaWhiteMatter':'L'} ],
            },
            {
                'Parietal': [ {'RightParietalWhiteMatter':'R'}, {'LeftParietalWhiteMatter':'L'} ],
            },
            {
                'Occipital': [ {'RightOccipitalWhiteMatter':'R'}, {'LeftOccipitalWhiteMatter':'L'} ],
            },
        ],
    },
    {
        'color_dev': '#f0ad4e',     # orangy
        'Subcortical Regions' :
        [
            {
                'Caudate': [ {'RightCaudate':'R'}, {'LeftCaudate':'L'} ],
            },
            {
                'Accumbens': [ {'RightAccumbensArea':'R'}, {'LeftAccumbensArea':'L'} ],
            },
            {  
                'Putamen': [ {'RightPutame':'R'}, {'LeftPutame':'L'} ],
            },
            {
                'Pallidum': [ {'RightPallidum':'R'}, {'LeftPallidum':'L'} ],
            },
            {    
                'Basal\nForebrain': [  {'Right Basal Forebrain':'R'}, {'Left Basal Forebrain':'L'} ],
            },
            {
                'Amygdala': [ {'RightAmygdala':'R'}, {'LeftAmygdala':'L'} ],
            },
            {
                'Hippocampus': [ {'RightHippocampus':'R'}, {'LeftHippocampus':'L'} ],
            },
            {
                'Ventral DC': [ {'Right Ventral DC':'R'}, {'Left Ventral DC':'L'} ],
            },
            {
                'Thalamus': [ {'RightThalamusProper':'R'}, {'LeftThalamusProper':'L'} ],
            },
            {
                'Brain Stem': [ 'BrainStem' ],
            },
            {
                'Pons': [ 'Pons' ],
            },
        ],
    },
    {
        'color_dev': '#d9534f',     # redish
        'Cerebellum':
        [
            {
                'Anterior': [ 'Anterior' ],
            },
            {
                'Superior Posterior': [ 'Superior_Posterior' ],
            },
            {
                'Posterior': [ 'Posterior' ],
            },
            {
                'Inferior Posterior': [ 'Inferior_Posterior' ],
            },
            {
                'Vermis': [ 'Vermis' ],
            },
            {
                'Deep nuclei': [ 'Deep_nuclei' ],
            },
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
    print '   -a, --abs-dev             Preserve sign of the deviation'
    print '   -c, --config <file>       Config file'
    print '   -d, --deviation <num>     Highlight deviations bigger than this [0.05]'
    print '   -h, --help                This help message'
    sys.exit(1)

def usage_example():
    print "\nExample of valid input:"
    print "\tRightAccumbensArea  LeftAccumbensArea   RightAmygdala  etc.."
    print "\t0.5%                2.9%                33.1%          etc..\n"


abs_dev  = False
in_file  = None
out_file = None
config   = None
dev      = 0.05
if len(sys.argv) < 2: usage()
args = sys.argv[1:]
while len(args):
    if args[0]=='-a' or args[0]=='--abs-dev': 
        abs_dev = True
    elif args[0]=='-?' or args[0]=='-h' or args[0]=='--help': 
        usage()
    elif args[0]=='-c' or args[0]=='--config': 
        args = args[1:]
        config = args[0]
    elif args[0]=='-d' or args[0]=='--deviation': 
        args = args[1:]
        dev  = float(args[0])
    elif in_file == None: in_file = args[0]
    elif out_file == None: out_file = args[0]
    else: usage()
    args = args[1:]

if config!=None: execfile(config)
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

ltmp   = []  # labels, can repeat multiple times
lbls   = []
xlbls  = []
lbls2  = []
xvals  = []
yvals  = []
cols   = []
sgrp   = []
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
                    lbl2 = None
                    if type(column).__name__ == 'dict':
                        for cname in column:
                            #if key=='Thalamus' or key=='Parietal' or key=='Pallidum' or key=='Putame': lbl2 = column[cname]
                            lbl2 = column[cname]
                            column = cname
                            break
                    if column not in cols_hash: continue
                    lbls2.append(lbl2)
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
#ax.set_rlabel_position(0)
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

# Legend
leg_rect = []
leg_lbl  = []
for col in leg:
    rect = patches.Rectangle((0,0), 0.1, 0.1, color=col)
    leg_rect.append(rect)
    leg_lbl.append(leg[col])
leg_rect.append(patches.Rectangle((0,0), 0.1, 0.1, color='grey', alpha=0.4))
leg_lbl.append('Not statistically significant')
plt.legend(leg_rect,leg_lbl,prop={'size':9},frameon=False,bbox_to_anchor=(0.98,0.98),bbox_transform=plt.gcf().transFigure)

# Radial text labels
for i in range(len(xlbls)):
    angle_rad = xlbls[i]
    angle_deg = angle_rad*180/np.pi
    ha  = "left"
    rot = angle_deg
    if angle_rad > np.pi/2 and angle_rad < np.pi*3/2.: 
        ha  = "right"
        rot = angle_deg - 180
    plt.text(angle_rad, yticks[-1]+0.05, lbls[i], size=9, horizontalalignment=ha, 
        verticalalignment="center", rotation=rot, rotation_mode='anchor')

# L/R sub-labels
for i in range(len(lbls2)):
    if lbls2[i]==None: continue
    angle_rad = i*width+width*0.5
    angle_deg = angle_rad*180/np.pi - 90
    ha  = "left"
    rot = angle_deg
    plt.text(angle_rad, yticks[-1]-0.08, lbls2[i], size=9, horizontalalignment=ha, verticalalignment="center", rotation=rot, rotation_mode='anchor',color='#555555')

for x,y,color,bar in zip(xvals, yvals, cols, bars):
    if abs(y-1) > dev:
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


