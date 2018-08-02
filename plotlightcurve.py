#This program plots the light curves resulting from the lcsbo.pro

import numpy as np
from astropy.io import ascii
import matplotlib.pyplot as plt
import pdb
import os
import sys
import math
import astropy
import argparse


#Function fo plot the results
def plotlc(resultsname, output_filename,plot_title, saveplot=False, numfig=1):
	
	#Hack to ignore the intial and final apostrophes
	if resultsname[0]=="'":
		resultsname=resultsname[1:]
		resultsname=resultsname[:len(resultsname)-1]	
		
	while True:
		try:
			tbl=ascii.read(resultsname)
			break
		except astropy.io.ascii.core.InconsistentTableError:
			print('Problems with the light curve '+resultsname)
			return
			

	########################################################

	#Prepare the time axis.
	#If all the observations happen on the same night,
	#then minutes timescale. Otherwise MJD.

	time=[]
	
	#Sort the table by MJD
	indexsort=np.argsort(tbl["MJD"])
	tbl=tbl[indexsort]

	#Do you want to decide the starting MJD?
	myownMJD=False
	
	#################
	#DEFAULT: The initial time is the earliest MJD data
	if myownMJD==False:
		if ((tbl["MJD"][-1]-tbl["MJD"][0]) < 1):
			MJD0=tbl["MJD"][0]
			for MJD in tbl["MJD"]:
				time.append(  (MJD-MJD0)*24*60  )
				timename="Minutes since MJD="+str(MJD0)	
		else:
			MJD0=int(tbl["MJD"][0])-1  
			for MJD in tbl["MJD"]:
				time.append(  (MJD-MJD0)  )
				timename="MJD-"+str(MJD0)	
	
	
	if myownMJD==True:
		#What is the starting MJD?
		myMJD0=57789.3296963
		
		#Time axis in minutes or days? (timeax='minutes'/'days')
		timeax='minutes'
		
		if (timeax=='minutes'):
			MJD0=myMJD0
			for MJD in tbl["MJD"]:
				time.append(  (MJD-MJD0)*24*60  )
				timename="Minutes since MJD="+str(MJD0)	
		else:
			MJD0=myMJD0 
			for MJD in tbl["MJD"]:
				time.append(  (MJD-MJD0)  )
				timename="MJD-"+str(MJD0)
	
	
	#Set the limits of the plot axis
	xmin=min(time)-1
	xmax=max(time)+1

##########################################################
#########################################################
	#Go through the whole table and divide detections
	#from upper limits (5sigma, emag>0.198).
	#The upper limits are defined as the magnitude value minus its error.

	#Initialise the arrays
	magarr=[]
	emagarr=[]
	ularr=[]

	#Also initialise arrays for the plot axis limits
	ymin0=[]
	ymax0=[]
	
	

	for mag,emag,ulmag in zip(tbl["MAG"],tbl["EMAG"],tbl["ULMAG"]):
		detection=(emag <= 0.2 and emag !=0)
		
		#Check for NaN values and bring them to zero
		if math.isnan(mag):
			mag=0
		if math.isnan(emag):
			emag=0
		if math.isnan(ulmag):
			ulmag=99

		
		#Is the UL value infinite? If so, bring it down to 0. It will be ignored, but leaving an empty space in the time axis.

		if detection:
			magarr.append(mag)
			emagarr.append(emag)
			ularr.append(0)
			ymin0.append(mag+emag)
			ymax0.append(mag-emag)

		if (detection == False and ulmag < 50):
			magarr.append(0)
			emagarr.append(0)
			ularr.append(ulmag)
			ymin0.append(ulmag+ulmag/100.)
			ymax0.append(ulmag-ulmag/100.)
		
		if (detection == False and ulmag > 50):
			ulmag=0
			magarr.append(0)
			emagarr.append(0)
			ularr.append(ulmag)
	

	#Limits for the y axis
	 
	ymin=np.amax(ymin0)
	ymax=np.amin(ymax0)
	
	##Print the table
	##for t in range(len(tbl["MJD"])):
		##print tbl[t]

#########################################	
	
	
	#Plot
	plt.figure(numfig, figsize=(9,6))
	plt.errorbar(time, magarr, yerr=emagarr, fmt="bo")
	plt.plot(time, magarr, 'bo',color='black')
	plt.plot(time, ularr, "rv")
	plt.xlabel(timename, fontsize=19)
	plt.ylabel('g mag', fontsize=19)
	plt.axis([xmin,xmax,ymin,ymax])
	plt.tick_params(labelsize=18)
	##titlename0=resultsname.replace(".txt", "")
	##titlename1=titlename0.replace("results_", "")
	plt.title(plot_title,fontsize=19)
	
	if saveplot:
		#Is the output filename provided?
		if output_filename == ' ':
			output_filename=resultsname
		#Replace everything found after the last dot in the filename
		output_filename2=output_filename.split('.')
		return plt.savefig(output_filename2[0] + ".png")
	
	else: 
		return plt.show()

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1', 'Yes', 'True'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', 'No', 'False'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main(args):
	input_filename=args.input_filename
	output_filename=args.output_filename
	saveornot=args.saveornot
	plot_title=args.plot_title
	
	#Call the plotting function
	plotlc(input_filename,output_filename,plot_title,saveplot=saveornot,numfig=1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot light curves, \
            with theader in the format: \
	    #MJD	MAG	EMAG	ULMAG - \
	    where MJD is the modifies Julian Date,\
	    MAG is the magnitude and EMAG its error, and \
	    ULMAG is the magnitude upper limit. ')
    parser.add_argument('-i', dest='input_filename', type=str, required=True, \
    help='Light curve filename')
    parser.add_argument('-s', dest='saveornot', type=str2bool, required=False, \
    help='Save the plot (PNG format)')
    parser.add_argument('-o', dest='output_filename', type=str, required=False, default=' ', \
    help='Output light curve file name if saved (-s) ')
    parser.add_argument('-t', dest='plot_title', type=str, required=False, default=' ', \
    help='Plot title')
	    
    args = parser.parse_args()

    main(args)
