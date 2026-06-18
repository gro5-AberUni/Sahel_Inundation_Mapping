import glob
import os

listCmds = []

# targetThreshold = 'GT0'
# year = '2023'
#2018,2019,2020,2021,2022,
for year in [2014,2015,2016,2017,2018]:
#for year in [2023]:
    for i in [1,3,5,7,9,11]:
    #for i in [1]:
        classImg = os.path.abspath(glob.glob('./Class/{0}/Sahel_Classified*Month-{1}-{2}*{0}*.tif'.format(year,i,i+1))[0])
        print(classImg)

        waterImg = os.path.abspath('./Sahel_Water_Count_2014-2018.tif')
        pekelImg = os.path.abspath('./JRC_Water/Africa_Europe_Water_COG_Sahel_COG_GT0_COG_Re_COG.tif')

        burnWaterImg = os.path.abspath('./Burn_Water_Mask/{0}/Sahel_BurnWaterMask_Month-{1}-{2}_Year-{0}.tif'.format(2023,i,i+1))

        globalForestCover = os.path.abspath('./Hansen_Forest_Cover/Sahel_Global_Forest_Cover_2000_COG_Re.tif')

        outputImg = classImg.replace('.tif','_Post_Class_Lvl2.tif')

        cmd = 'python 03_apply_PostClassificationRefinement.py -i {0} -w {1} -o {2} -p {3} -b {4} -f {5}\n'.format(classImg,waterImg,outputImg,pekelImg,burnWaterImg,globalForestCover)

        listCmds.append(cmd)

print(listCmds)


with open('recodeJobDev.sh', 'w') as f:
    for cmd in listCmds:
        f.write(cmd)
