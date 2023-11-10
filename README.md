# Geometric-distortion correction for the MIRI imager

This is a Python tool that applies a geometric-distortion correction to a list of (x,y) raw coordinates obtained from data taken with the Mid-InfraRed Instrument (MIRI) Imager of *JWST*. The current version includes corrections for F560W, F770W and F1000W data only.


## Referencing

If you use this tool in your research, please cite [Libralato et al. 2023](TBD).


## Requirements

The following packages are needed to run the code: *numpy*, *pandas*, *astropy*.


## Instructions

Once the file has been downloaded and all packages installed, users can run the tool as follows:

$ python miri_raw2corr.py FILTER_NAME INPUT_CATALOG OUTPUT_CATALOG

- FILTER_NAME = [F560W, F770W, F1000W]

- INPUT_CATALOG = Input catalog in ascii format (space-separated columns). The first two columns must be the (x,y) raw coordinates. Positions must be defined in a 1-index reference frame. Positions in a 0-index Python-like frame would need to offset by one pixel in each coordinate before applying the geometric-distortion correction.

- OUTPUT_CATALOG = Output catalog in ascii format (space-separated columns). The file will containt two columns with the (x,y) positions corrected for geometric distortion.


## Notes on Version 1.0

- The geometric-distortion correction has been obtained with images in F560W, F700W or F1000W filters only. Users can run the code for other filters (using one of the three allowed filter entries), but the systematics resulting from applying this correction to longer-wavelength filters have not been studied yet.
- The geometric-distortion correction is not applied to stars measured in regions other then the Imager and the Lyot, and the pair (0,0) is returned in this case.
- Positions must be defined in a 1-index reference frame. Positions in a 0-index Python-like frame would need to offset by one pixel in each coordinate before applying the geometric-distortion correction.  
