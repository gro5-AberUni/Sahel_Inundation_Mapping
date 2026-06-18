
import os
import gc
import numpy as np
import rsgislib
from rsgislib import imageutils
import fuzzy
from fuzzy import fuzzy_lt, fuzzy_gt
from rios import applier


def _applyFuzzy(info, inputs, output, otherargs):
    # print(inputs.inputImg.shape)
    waterFraction = inputs.inputImg[0] / 100
    vegFraction = inputs.inputImg[1] / 100
    bareFraction = inputs.inputImg[2] / 100
    burnFraction = inputs.inputImg[3] / 100

    slopeArr = np.nan_to_num(inputs.slope[0].astype(np.float32))
    handArr = np.nan_to_num(inputs.hand[0].astype(np.float32))  ## Modification to address no data areas

    wvSumImg = waterFraction + vegFraction
    wbSumImg = waterFraction + bareFraction
    # vbSumImg = vegFraction + bareFraction
    bbvSumImg = bareFraction + vegFraction + burnFraction

    #### Open Water ####

    ow1_water_frac = fuzzy.fuzzy_gt(waterFraction, low_bound=65, up_bound=80)
    # print(ow1_water_frac.shape)
    ow1_slope = fuzzy.fuzzy_lt(slopeArr, low_bound=2, up_bound=4)
    # print(ow1_slope.shape)
    ow1_hand = fuzzy.fuzzy_lt(handArr, low_bound=25, up_bound=35)
    # print(ow1_hand.shape)
    ow1 = fuzzy.fuzzy_and([ow1_water_frac, ow1_slope, ow1_hand])

    del ow1_water_frac
    del ow1_slope
    del ow1_hand
    gc.collect()

    #### Flooded Veg ####
    # ]efv = np.where(wvSumImg>=70,np.where((vegFraction >= 25) & (vegFraction < 75),np.where((waterFraction >= 25) & (waterFraction < 75),np.where(slopeArr<2.5,1,0),0),0),0)

    efv_sum = fuzzy.fuzzy_gt(wvSumImg, low_bound=55, up_bound=70)
    efv_veg_gt = fuzzy.fuzzy_gt(vegFraction, low_bound=10, up_bound=25)
    efv_veg_lt = fuzzy.fuzzy_lt(vegFraction, low_bound=65, up_bound=75)
    efv_veg = fuzzy.fuzzy_and([efv_veg_gt, efv_veg_lt])

    del efv_veg_gt
    del efv_veg_lt
    gc.collect()

    efv_water_gt = fuzzy.fuzzy_gt(waterFraction, low_bound=30, up_bound=10)
    efv_water_lt = fuzzy.fuzzy_lt(waterFraction, low_bound=75, up_bound=75)
    efv_water = fuzzy.fuzzy_and([efv_water_gt, efv_water_lt])

    del efv_water_gt
    del efv_water_lt
    gc.collect()

    efv_slope = fuzzy.fuzzy_lt(slopeArr, low_bound=1, up_bound=3)

    efv = fuzzy.fuzzy_and([efv_sum, efv_veg, efv_water, efv_slope])

    del efv_sum
    del efv_veg
    del efv_water
    del efv_slope
    gc.collect()

    #### Wet Bare Sand /  Turbid Water ####
    # wbs = np.where(wbSumImg>=75,np.where((waterFraction >= 25) & (waterFraction < 75),np.where((bareFraction >= 25) & (bareFraction < 75),np.where(slopeArr<=2.5,1,0),0),0),0)

    wbs_sum = fuzzy.fuzzy_gt(wbSumImg, low_bound=65, up_bound=80)
    wbs_water_gt = fuzzy.fuzzy_gt(waterFraction, low_bound=25, up_bound=30)
    wbs_water_lt = fuzzy.fuzzy_lt(waterFraction, low_bound=65, up_bound=75)
    wbs_water = fuzzy.fuzzy_and([wbs_water_gt, wbs_water_lt])

    del wbs_water_gt
    del wbs_water_lt
    gc.collect()

    wbs_bare_gt = fuzzy.fuzzy_gt(bareFraction, low_bound=20, up_bound=30)
    wbs_bare_lt = fuzzy.fuzzy_lt(bareFraction, low_bound=65, up_bound=75)
    wbs_bare = fuzzy.fuzzy_and([wbs_bare_gt, wbs_bare_lt])

    del wbs_bare_gt
    del wbs_bare_lt
    gc.collect()

    wbs_hand = fuzzy.fuzzy_lt(handArr, low_bound=8.14301279649998, up_bound=40)
    wbs_slope = fuzzy.fuzzy_lt(slopeArr, low_bound=2, up_bound=3)

    wbs = fuzzy.fuzzy_and([wbs_sum, wbs_water, wbs_bare, wbs_hand, wbs_slope])

    del wbs_sum
    del wbs_water
    del wbs_bare
    gc.collect()

    #### Bare Earth ####
    ## Part 1 ##
    # bbvP1 = np.where(bbvSumImg>=60,np.where((vegFraction >= 25) & (vegFraction < 75),np.where((burnFraction >= 20) & (burnFraction < 75),1,0),0),0)

    bbvp1_sum = fuzzy.fuzzy_gt(bbvSumImg, low_bound=65, up_bound=80)

    bbvp1_veg_gt = fuzzy.fuzzy_gt(vegFraction, low_bound=10, up_bound=22.9958995187748)
    bbvp1_veg_lt = fuzzy.fuzzy_lt(vegFraction, low_bound=60.7087890735419, up_bound=85)

    bbvp1_veg = fuzzy.fuzzy_and([bbvp1_veg_gt, bbvp1_veg_lt])

    del bbvp1_veg_gt
    del bbvp1_veg_lt
    gc.collect()

    bbvp1_burn_gt = fuzzy.fuzzy_gt(burnFraction, low_bound=10, up_bound=20)
    bbvp1_burn_lt = fuzzy.fuzzy_lt(burnFraction, low_bound=64.8405077807786, up_bound=75)
    bbvp1_burn = fuzzy.fuzzy_and([bbvp1_burn_gt, bbvp1_burn_lt])

    del bbvp1_burn_gt
    del bbvp1_burn_lt
    gc.collect()

    bbvp1 = fuzzy.fuzzy_and([bbvp1_sum, bbvp1_veg, bbvp1_burn])

    del bbvp1_sum
    del bbvp1_veg
    del bbvp1_burn
    gc.collect()

    # bbvP2 = np.where(bbvSumImg>=75,np.where((vegFraction >= 25) & (vegFraction < 75),np.where((bareFraction >= 25) & (bareFraction < 75),np.where(slopeArr>=2.5,1,0),0),0),0)

    bbvp2_sum = fuzzy.fuzzy_gt(bbvSumImg, low_bound=54.4905589754301, up_bound=75)

    bbvp2_veg_gt = fuzzy.fuzzy_gt(vegFraction, low_bound=10, up_bound=30)
    bbvp2_veg_lt = fuzzy.fuzzy_lt(vegFraction, low_bound=66.8533402937843, up_bound=75)

    bbvp2_veg = fuzzy.fuzzy_and([bbvp2_veg_gt, bbvp2_veg_lt])

    del bbvp2_veg_gt
    del bbvp2_veg_lt
    gc.collect()

    bbvp2_bare_gt = fuzzy.fuzzy_gt(bareFraction, low_bound=10, up_bound=25)
    bbvp2_bare_lt = fuzzy.fuzzy_lt(bareFraction, low_bound=70.2574806945563, up_bound=75)

    bbvp2_bare = fuzzy.fuzzy_and([bbvp2_bare_gt, bbvp2_bare_lt])

    del bbvp2_bare_gt
    del bbvp2_bare_lt
    gc.collect()

    bbvp2 = fuzzy.fuzzy_and([bbvp2_sum, bbvp2_veg, bbvp2_bare])

    del bbvp2_sum
    del bbvp2_veg
    del bbvp2_bare
    gc.collect()

    bbv = fuzzy.fuzzy_or([bbvp1, bbvp2])

    del bbvp1
    del bbvp2
    gc.collect()

    #### Green Veg ####
    # gv = np.where(vegFraction>=60,1,0)

    gv = fuzzy.fuzzy_gt(vegFraction, low_bound=70, up_bound=85)

    #### Bare Earth ####

    bs = fuzzy.fuzzy_gt(bareFraction, low_bound=65, up_bound=65)

    #### Burned Land ####

    burn = fuzzy.fuzzy_gt(burnFraction, low_bound=34.2861877847087, up_bound=80)

    del waterFraction
    del vegFraction
    del bareFraction
    del burnFraction
    gc.collect()

    #### Topo Unsuit ####

    topoSlope = fuzzy.fuzzy_gt(slopeArr, low_bound=3, up_bound=5)
    topoHnd = fuzzy.fuzzy_gt(handArr, low_bound=35, up_bound=49.9957150211596)
    topoUnsuit = fuzzy.fuzzy_or([topoSlope, topoHnd])

    #### Label Classes ####

    """""
    Flooded Veg = 1 - '45AE90'
    Turbid Water = 2 - '2250CA'
    Open Water = 3 - '603114'
    Spase Bare/Burnt Veg = 4 - 'E5CB71'
    Green Veg = 5 - '328536'
    Bare Earth = 6 - 'CBBF7C'
    Burnt Land = 7 - '000000'
    """""

    ## Stack Fuzzy Membership ##

    stackedMembership = np.stack([np.zeros_like(efv), efv, wbs, bbv, ow1, gv, bs, burn, topoUnsuit], axis=2)

    del efv
    del ow1
    del wbs
    del bbv
    del gv
    del bs
    del burn
    gc.collect()

    # print(stackedMembership.shape)

    maxMemberShipIdx = np.array([np.argmax(stackedMembership, axis=2)])

    recode = np.where(maxMemberShipIdx == 5, 3, np.where(maxMemberShipIdx == 6, 3,
                                                         np.where(maxMemberShipIdx == 7, 3,
                                                                  np.where(maxMemberShipIdx == 8, 3,
                                                                           maxMemberShipIdx))))

    # print(maxMemberShipIdx.shape)

    output.outimage = recode.astype(np.int8)




slopeRe = './Slope_Sahel_COG.tif'
handRe = './HAND_Sahel_COG.tif'
datatype = rsgislib.TYPE_8INT
numpyDT = rsgislib.get_numpy_datatype(datatype)

progress_bar = rsgislib.TQDMProgressBar()

img = './UnmixImage_Bi-Monthly-Tile-0_Year-2025_Kenya_Sep_Oct.kea'
classifiedOutImg = img.replace('.kea','_Classified.tif')

infiles = applier.FilenameAssociations()
infiles.inputImg = img
infiles.slope = slopeRe
infiles.hand = handRe
outfiles = applier.FilenameAssociations()
outfiles.outimage = classifiedOutImg
otherargs = applier.OtherInputs()
otherargs.npDT = numpyDT
aControls = applier.ApplierControls()
aControls.progress = progress_bar
aControls.creationoptions = rsgislib.imageutils.get_rios_img_creation_opts(
    'GTIFF'
)
aControls.drivername = 'GTIFF'
aControls.omitPyramids = True
aControls.calcStats = False
aControls.windowxsize = 1024
aControls.windowysize = 1024


applier.apply(
    _applyFuzzy, infiles, outfiles, otherargs, controls=aControls
)

classPalette = dict()
classPalette[0] = 'ffffff'
classPalette[1] = '45AE90'
classPalette[2] = '603114'
classPalette[3] = 'E5CB71'
classPalette[4] = '2250CA'

rsgislib.imageutils.define_colour_table(classifiedOutImg, classPalette)



