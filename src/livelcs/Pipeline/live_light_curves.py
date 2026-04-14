'''main file for pipeline'''

import sys
from livelcs.Util.util import (
    parse_arguments,
    open_tap_service,
    prepare_butler
)
from astropy.time import Time
import time
#import Lightcurver
#import Starred
#import PYCS
#import pyvo
#import os
#import subprocess
#import argparse
import sys
#import CCE/HME detection
import numpy as np

import lsst.sphgeom as sphgeom



#print(sphgeom.Region.from_ivoa_pos("CIRCLE 53.076 -28.110 2.0"))



### read in file of coordinates
# the targets parameter holds a dictionary of all objects in the provided file
if len(sys.argv) == 0:
    print("please provide a file holding a list of objects when calling this script")
all_arguments = sys.argv[1:]
targets, other_args = parse_arguments(all_arguments)



### open up a tap service
# requires token to be stored on the machine

rsp_tap = open_tap_service()


query = "SELECT * FROM tap_schema.schemas"
results = rsp_tap.run_sync(query)
results.to_table()
print(results)

exit()


schema='dp1'

### make an LSST butler to get image data
band = 'r'
ra = 44
dec = -2
query = f"band.name = '{band}' AND visit_detector_region.region OVERLAPS POINT ({ra}, {dec})"


from lsst.daf.butler import Butler
butler = Butler(
    "dp02-remote",
)


exit()


butler = prepare_butler()
butler.get_dataset_type('visit_image')
exit()

### query given coordinates

# we now have the coordinates for object [ii] defined as
# (targets[ii]['ra'], targets[ii]['dec'])



query = "SELECT TOP 25 * FROM "+schema+".Object"

results = rsp_tap.run_sync(query)
output = results.to_table()

print(output)


# import sources from live_light_curves.source_list using some json interface
# for each observation:
    # check if any coordinates in sources lay within FOV
    # follow notebooks/tutorials/DP1/300_Science_Demos/307_AGN on RSP (gets cutout)
# initialize live_light_curves.Classes.cutout for each cutout




### run Lightcurver steps 4-6 to get PSF from nearby stars

# pass each newly generated cutout to Lightcurver stamp extraction and PSF modeling
# initialize live_light_curves.Classes.stellar_cutouts with the Lightcurver outputs



### have "Narrow PSF"

# initialize live_light_curves.Classes.narrow_psf so it works with this pipeline



### Lightcurver step 7 for stellar photometry (opt)
# initialize live_light_curves.Classes.stellar_photometry if we want to push stellar light curves


### Starred to get deconvolved sources (requires point source initial positions)
# deconvolve cutouts with computed PSF (this could just be done within the cutout object)
# Q: does this get all sources (e.g. plus stars, host galaxy), or just lensed point sources?


### Starred returns calibrated light curve data point
# load current object light curves and append the new data point



### When enough data is collected, run PYCS3 or SBI to get time delays
# if a source's light curve passes some critical threshold (e.g. in time), run PYCS



### While collecting, run RNN detection to test for imminent HMEs
# if a source's light curve passes a critical threshold, run caustic crossing detection software



### Send alerts when detected
# if an alert is triggered, send the alert



### Update HTML interface
# always send updated light curves to the web interface daily
# perhaps we could be inspired by some code here https://github.com/duxfrederic/lightcurver/blob/main/lightcurver/plotting/plot_curves_template.html













