import glob
import os

from osgeo import gdal
from osgeo import osr
import gc
import numpy as np
import argparse
import rsgislib
from rsgislib import imageutils
from rios import applier

rsgislib.imageutils.set_env_vars_lzw_gtiff_outs(True)

parser = argparse.ArgumentParser(prog='Post Classification Refinement of Classified Products')
parser.add_argument('-i',metavar='',type=str,help='Input Class Image')

parser.add_argument('-w',metavar='',type=str,help='Input Water Time Series Image')
parser.add_argument('-p',metavar='',type=str,help='Pekel Water Occurence')

parser.add_argument('-b',metavar='',type=str,help='Water Burn Mask')

parser.add_argument('-f',metavar='',type=str,help='Input Global Forest Change Image')

parser.add_argument('-o',metavar='',type=str,help='OutputFileName')

args = parser.parse_args()

classImg = args.i
waterImg = args.w
pekelWater = args.p
burnWaterMask = args.b
forestCoverImg = args.f
classifiedOutImg = args.o

datatype = rsgislib.TYPE_8INT
numpyDT = rsgislib.get_numpy_datatype(datatype)

progress_bar = rsgislib.TQDMProgressBar()

infiles = applier.FilenameAssociations()
infiles.classImg = classImg
infiles.waterImg = waterImg
infiles.pekelImg = pekelWater
infiles.burnWaterMask = burnWaterMask
infiles.forestCoverImg = forestCoverImg
outfiles = applier.FilenameAssociations()
outfiles.outimage = classifiedOutImg

otherargs = applier.OtherInputs()
otherargs.npDT = np.uint8
aControls = applier.ApplierControls()
aControls.progress = progress_bar
aControls.creationoptions = rsgislib.imageutils.get_rios_img_creation_opts(
    'GTIFF'
)
aControls.drivername = 'GTIFF'
aControls.omitPyramids = True
aControls.calcStats = False
# aControls.creationoptions = ['ot=Byte']

def _applyFuzzy(info,inputs,output,otherargs):



    classArr = inputs.classImg
    pekelArr = inputs.pekelImg
    waterArr = inputs.waterImg
    burnWaterArr = inputs.burnWaterMask
    forestCoverArr = inputs.forestCoverImg

    classOut = np.where(classArr==2,np.where(pekelArr>0,2,np.where(waterArr>0,2,3)),classArr)

    classOutInun = np.where(classOut==1,np.where(burnWaterArr!=1,1,3),classOut)

    classOutForest = np.where(forestCoverArr>50,3,classOutInun)

    output.outimage = classOutForest.astype(np.uint8)

applier.apply(_applyFuzzy, infiles, outfiles, otherargs, controls=aControls)

#rsgislib.imageutils.gdal_translate(classifiedOutImg, classifiedOutImgCOG, 'COG', 1, '-co COMPRESS=LZW -ot Byte')

#os.remove(classifiedOutImg)

classPalette = dict()
classPalette[0] = 'ffffff'
classPalette[1] = '45AE90'
classPalette[2] = '603114'
classPalette[3] = 'E5CB71'
classPalette[4] = '2250CA'
# classPalette[5] = 'ff2800'
# classPalette[6] = '7DF9FF'

rsgislib.imageutils.define_colour_table(classifiedOutImg, classPalette)