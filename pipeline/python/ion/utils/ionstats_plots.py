#!/usr/bin/python
# Copyright (C) 2012 Ion Torrent Systems, Inc. All Rights Reserved
import os
import json

from matplotlib import use
use("Agg",warn=False)
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import traceback
from ion.utils.blockprocessing import printtime

''' Generate a small 300x30 read length histogram "sparkline" for display in barcode table '''

def read_length_sparkline(ionstats_basecaller_filename, output_png_filename, max_length):

    try:
        printtime("DEBUG: Generating plot %s" % output_png_filename)
        
        f = open(ionstats_basecaller_filename,'r')
        ionstats_basecaller = json.load(f);
        f.close()

        histogram_x = range(0,max_length,5)
        num_bins = len(histogram_x)
        histogram_y = [0] * num_bins
    
        for read_length,frequency in enumerate(ionstats_basecaller['full']['read_length_histogram']):
            current_bin = min(read_length/5,num_bins-1)
            histogram_y[current_bin] += frequency

        max_y = max(histogram_y)
        max_y = max(max_y,1)
        
        fig = plt.figure(figsize=(3,0.3),dpi=100)
        ax = fig.add_subplot(111,frame_on=False,xticks=[],yticks=[],position=[0,0,1,1])
        ax.bar(histogram_x,histogram_y,width=6.5, color="#2D4782",linewidth=0, zorder=2)
    
        for idx in range(0,max_length,50):
            label_bottom = str(idx)
            ax.text(idx,max_y*0.70,label_bottom,horizontalalignment='center',verticalalignment='center',
                    fontsize=8, zorder=1)
            ax.axvline(x=idx,color='#D0D0D0',ymax=0.5, zorder=0)
            ax.axvline(x=idx,color='#D0D0D0',ymin=0.9, zorder=0)
    
        ax.set_ylim(0,max_y)
        ax.set_xlim(-10,max_length)
        fig.patch.set_alpha(0.0)
        fig.savefig(output_png_filename)

    except:
        printtime('Unable to generate plot %s' % output_png_filename)
        traceback.print_exc()


''' Generate read length histogram for the report page '''

def read_length_histogram(ionstats_basecaller_filename, output_png_filename, max_length):

    try:
        printtime("DEBUG: Generating plot %s" % output_png_filename)
        
        f = open(ionstats_basecaller_filename,'r')
        ionstats_basecaller = json.load(f);
        f.close()

        histogram_x = range(0,max_length,1)
        num_bins = len(histogram_x)
        histogram_y = [0] * num_bins
        
        for read_length,frequency in enumerate(ionstats_basecaller['full']['read_length_histogram']):
            current_bin = min(read_length,num_bins-1)
            if read_length < num_bins:
                histogram_y[current_bin] += frequency
        
        max_y = max(histogram_y)
        max_y = max(max_y,1)
        
        fig = plt.figure(figsize=(4,3.5),dpi=100)
        ax = fig.add_subplot(111,frame_on=False,yticks=[],position=[0,0.15,1,0.88])
        ax.bar(histogram_x,histogram_y,width=2.5, color="#2D4782",linewidth=0, zorder=2)
    
    
        ax.set_ylim(0,1.2*max_y)
        ax.set_xlim(-5,max_length+15)
        plt.xlabel("Read Length")
        fig.patch.set_alpha(0.0)
        fig.savefig(output_png_filename)

    except:
        printtime('Unable to generate plot %s' % output_png_filename)
        traceback.print_exc()


''' Generate old-style read length histogram for display in classic report and dialog box in new report '''

def old_read_length_histogram(ionstats_basecaller_filename, output_png_filename, max_length):
    
    try:
        printtime("DEBUG: Generating plot %s" % output_png_filename)
        
        f = open(ionstats_basecaller_filename,'r')
        ionstats_basecaller = json.load(f);
        f.close()

        histogram_x = range(0,max_length,1)
        num_bins = len(histogram_x)
        histogram_y = [0] * num_bins
    
        for read_length,frequency in enumerate(ionstats_basecaller['full']['read_length_histogram']):
            current_bin = min(read_length,num_bins-1)
            if read_length < num_bins:
                histogram_y[current_bin] += frequency
    
        fig = plt.figure(figsize=(8,4),dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(histogram_x, histogram_y, width=2, color="#2D4782",linewidth=0)
        ax.set_title('Read Length Histogram')
        ax.set_xlabel('Read Length')
        ax.set_ylabel('Count')
        fig.savefig(output_png_filename)

    except:
        printtime('Unable to generate plot %s' % output_png_filename)
        traceback.print_exc()



''' Generate cumulative read length plot of called vs aligned read length '''

def alignment_rate_plot(alignStats, ionstats_basecaller_filename, output_png_filename,graph_max_x):
    
    if not os.path.exists(alignStats):
        printtime("ERROR: %s does not exist" % alignStats)
        return
    
    def intWithCommas(x):
        if type(x) not in [type(0), type(0L)]:
            raise TypeError("Parameter must be an integer.")
        if x < 0:
            return '-' + intWithCommas(-x)
        result = ''
        while x >= 1000:
            x, r = divmod(x, 1000)
            result = ",%03d%s" % (r, result)
        return "%d%s" % (x, result)
    
    try:
        f = open(alignStats,'r')
        alignStats_json = json.load(f);
        f.close()
        read_length = alignStats_json["read_length"]
        #nread = alignStats_json["nread"]
        aligned = alignStats_json["aligned"]       
    except:
        printtime("ERROR: problem parsing %s" % alignStats)
        traceback.print_exc()
        return


    try:
        f = open(ionstats_basecaller_filename,'r')
        ionstats_basecaller = json.load(f);
        f.close()
    except:
        printtime('Failed to load %s' % (ionstats_basecaller_filename))
        traceback.print_exc()
        return

    histogram_x = range(0,graph_max_x)
    histogram_y = [0] * graph_max_x
    
    try:
        for read_length_bin,frequency in enumerate(ionstats_basecaller['full']['read_length_histogram']):
            current_bin = min(read_length_bin,graph_max_x-1)
            histogram_y[current_bin] += frequency
    except:
        printtime('Problem parsing %s' % (ionstats_basecaller_filename))
        traceback.print_exc()
        return


    for idx in range(graph_max_x-1,0,-1):
        histogram_y[idx-1] += histogram_y[idx]
    
    nread = histogram_y[1:]

    fig = plt.figure(figsize=(4,3),dpi=100)
    ax = fig.add_subplot(111,frame_on=False,yticks=[], position=[0.1,0.15,0.8,0.89])

    max_x = 1
    if len(read_length) > 0:
        max_x = max(read_length)
    max_x = min(max_x,graph_max_x)

    max_y = max(nread)

    plt.fill_between(histogram_x[1:], nread, color="#808080", zorder=1)
    plt.fill_between(read_length, aligned, color="#2D4782", zorder=2)

    plt.xlabel('Position in Read')
    plt.ylabel('Reads')

    if sum(nread) > 0:
        map_percent = int(round(100.0 * float(alignStats_json["total_mapped_target_bases"]) 
                                / float(sum(nread))))
        unmap_percent = 100 - map_percent
    else:
        map_percent = 0.0
        unmap_percent = 0.0

    color_blue = "#2D4782"
    color_gray = "#808080"
    fontsize_big = 15
    fontsize_small = 10
    fontsize_medium = 8

    ax.text(0.8*max_x,0.95*max_y,'Aligned Bases',horizontalalignment='center',verticalalignment='center', fontsize=fontsize_small, zorder=4, color=color_blue,weight='bold',stretch='condensed')
    ax.text(0.8*max_x,1.05*max_y,' %d%%'%map_percent,horizontalalignment='center',verticalalignment='center', fontsize=fontsize_big, zorder=4, color=color_blue,weight='bold',stretch='condensed')
    ax.text(0.8*max_x,0.7*max_y,'Unaligned',horizontalalignment='center',verticalalignment='center',
            fontsize=fontsize_small, zorder=4, color=color_gray,weight='bold',stretch='condensed')
    ax.text(0.8*max_x,0.8*max_y,' %d%%'%unmap_percent,horizontalalignment='center',verticalalignment='center', fontsize=fontsize_big, zorder=4, color=color_gray,weight='bold',stretch='condensed')

    ax.text(-0.06*max_x,1.02*max_y,intWithCommas(max_y),horizontalalignment='left',verticalalignment='bottom',  zorder=4, color="black")
       
    ax.set_xlim(0,max_x)
    ax.set_ylim(0,1.2*max_y)
    #plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    fig.patch.set_alpha(0.0)
    fig.savefig(output_png_filename)


def quality_histogram(ionstats_basecaller_filename,output_png_filename):
    
    try:
        printtime("DEBUG: Generating plot %s" % output_png_filename)
        
        f = open(ionstats_basecaller_filename,'r')
        ionstats_basecaller = json.load(f);
        f.close()
    
        qv_histogram = ionstats_basecaller["qv_histogram"]
        
    
        sum_total = float(sum(qv_histogram))
        if sum_total > 0:
            percent_0_5 = 100.0 * sum(qv_histogram[0:5]) / sum_total
            percent_5_10 = 100.0 * sum(qv_histogram[5:10]) / sum_total
            percent_10_15 = 100.0 * sum(qv_histogram[10:15]) / sum_total
            percent_15_20 = 100.0 * sum(qv_histogram[15:20]) / sum_total
            percent_20 = 100.0 * sum(qv_histogram[20:]) / sum_total
        else:
            percent_0_5 = 0.0
            percent_5_10 = 0.0
            percent_10_15 = 0.0
            percent_15_20 = 0.0
            percent_20 = 0.0
    
        graph_x = [0,5,10,15,20]
        graph_y = [percent_0_5,percent_5_10,percent_10_15,percent_15_20,percent_20]
    
        max_y = max(graph_y)
        
        ticklabels = ['0-4','5-9','10-14','15-19','20+']
    
        fig = plt.figure(figsize=(4,4),dpi=100)
        ax = fig.add_subplot(111,frame_on=False,xticks=[],yticks=[],position=[.1,0.1,1,0.9])
        ax.bar(graph_x,graph_y,width=4.8, color="#2D4782",linewidth=0)
    
        for idx in range(5):
            label_bottom = ticklabels[idx]
            label_top = '%1.0f%%' % graph_y[idx]
            ax.text(idx*5 + 2.5,-max_y*0.04,label_bottom,horizontalalignment='center',verticalalignment='top',
                    fontsize=12)
            ax.text(idx*5 + 2.5,max_y*0.06+graph_y[idx],label_top,horizontalalignment='center',verticalalignment='bottom',
                    fontsize=12)
        
        plt.xlabel("Base Quality")
        
        ax.set_xlim(0,34.8)
        ax.set_ylim(-0.1*max_y,1.2*max_y)
        fig.patch.set_alpha(0.0)
        fig.savefig(output_png_filename)

    except:
        printtime('Unable to generate plot %s' % output_png_filename)
        traceback.print_exc()




''' Generate old AQ10, old AQ17, and new AQ17 plots for all test fragments '''

def tf_length_histograms(ionstats_tf_filename, output_dir):

    try:
        printtime("DEBUG: Generating TF plots:")
        
        f = open(ionstats_tf_filename,'r')
        ionstats_tf = json.load(f);
        f.close()

        for tf_name,tf_data in ionstats_tf['results_by_tf'].iteritems():

            Q10_hist = tf_data['AQ10']['read_length_histogram']
            Q17_hist = tf_data['AQ17']['read_length_histogram']
            sequence = tf_data['sequence']
            
            # Step 1: New AQ17
            
            output_png_filename = os.path.join(output_dir,'new_Q17_%s.png' % (tf_name))
            printtime("DEBUG: Generating plot %s" % output_png_filename)
            
            num_bases_q = len(Q17_hist)
            num_bases_s = len(sequence)
            num_bases = min(num_bases_q,num_bases_s)
            nuc_color = {'A':"#4DAF4A",'C':"#275EB8",'T':"#E41A1C",'G':"#202020"}
            text_offset = -max(Q17_hist) * 0.1
            
            fig = plt.figure(figsize=(8,1),dpi=100)
            ax = fig.add_subplot(111,frame_on=False,xticks=[],yticks=[],position=[0,0.3,1,0.7])
            ax.bar(range(num_bases_q),Q17_hist,linewidth=0,width=1,color="#2D4782")
            for idx in range(num_bases):
                nuc = sequence[idx]
                ax.text(idx+1,text_offset,nuc,horizontalalignment='center',verticalalignment='center',fontsize=8,family='sans-serif',weight='bold',color=nuc_color[nuc])
                if (idx%10) == 0:
                    ax.text(idx+0.5,3*text_offset,str(idx),horizontalalignment='center',verticalalignment='center',fontsize=8,family='sans-serif',weight='bold')
                    
            ax.set_xlim(0,num_bases+2)
            fig.patch.set_alpha(0.0)
            fig.savefig(output_png_filename)
            
            # Step 2: New AQ10
            
            output_png_filename = os.path.join(output_dir,'new_Q10_%s.png' % (tf_name))
            printtime("DEBUG: Generating plot %s" % output_png_filename)
            
            num_bases_q = len(Q10_hist)
            num_bases_s = len(sequence)
            num_bases = min(num_bases_q,num_bases_s)
            nuc_color = {'A':"#4DAF4A",'C':"#275EB8",'T':"#E41A1C",'G':"#202020"}
            text_offset = -max(Q10_hist) * 0.1
            
            fig = plt.figure(figsize=(8,1),dpi=100)
            ax = fig.add_subplot(111,frame_on=False,xticks=[],yticks=[],position=[0,0.3,1,0.7])
            ax.bar(range(num_bases_q),Q10_hist,linewidth=0,width=1,color="#2D4782")
            for idx in range(num_bases):
                nuc = sequence[idx]
                ax.text(idx+1,text_offset,nuc,horizontalalignment='center',verticalalignment='center',fontsize=8,family='sans-serif',weight='bold',color=nuc_color[nuc])
                if (idx%10) == 0:
                    ax.text(idx+0.5,3*text_offset,str(idx),horizontalalignment='center',verticalalignment='center',fontsize=8,family='sans-serif',weight='bold')
                    
            ax.set_xlim(0,num_bases+2)
            fig.patch.set_alpha(0.0)
            fig.savefig(output_png_filename)
            
    except:
        printtime('Unable to generate TF plots')
        traceback.print_exc()



if __name__=="__main__":
    
    #read_length_histogram('basecaller_results/ionstats_basecaller.json','readLenHisto2.png',400)
    #alignment_rate_plot('alignStats_err.json','basecaller_results/ionstats_basecaller.json','alignment_rate_plot.png',300)

    #old_read_length_histogram('readLen.txt','readLenHisto.png', 400)
    #old_read_length_histogram('ionstats_basecaller.json','readLenHisto.png', 400)
    #generate_quality_histogram('ionstats_basecaller.json','quality_histogram.png')

    tf_length_histograms('ionstats_tf.json', '.')

