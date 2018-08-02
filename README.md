# Plot-light-curves

# plotlightcurve.py

Python 2.7 

Plot light curves (magnitude against time).  Files including the light curve must have a header in the format:

#MJD MAG EMAG ULMAG 

where MJD is the modifies Julian Date, MAG is the magnitude and EMAG its error, and ULMAG is the magnitude upper limit.

Optional arguments:

  -h, --help          show this help message and exit
  
  -i INPUT_FILENAME   Light curve filename
  
  -s SAVEORNOT        Save the plot (PNG format)
  
  -o OUTPUT_FILENAME  Output light curve file name if saved (-s)
  
  -t PLOT_TITLE       Plot title
