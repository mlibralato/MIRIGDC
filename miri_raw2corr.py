#!/usr/bin/env python
# coding: utf-8

import os
import sys
import numpy as np
import pandas as pd
from astropy.table import Table





# Compute polynomial correction
def poly(xr, yr, filt):

    if (filt=='F560W'):
        a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20 = 0.00000000, 0.00000000, -0.05699776, -5.44597720, -0.29638782, -1.04368229,  0.26172114, -1.89055872,  0.05387521,  1.48452063,  1.62886963,  0.29945154,  1.08537366, -0.08936789,  1.11006137, -0.13041789,  0.94082288,  0.76511794,  0.21556051,  0.12295708
        b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18, b19, b20 = -5.53485360,  3.90017706, -3.46932386, -1.16203929, -0.02126305,  0.33672129, -4.19754043,  0.56120565, -3.98512838,  0.95473439,  0.41044640,  2.23137769, -0.38047274,  1.12033961,  0.27900547,  0.86552220,  0.81859298,  0.50530597,  0.52373109,  0.09081032

    elif (filt=='F770W'):
        a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20 = 0.00000000,   0.00000000,  -0.12984013,  -5.45924966,  -0.30998663,  -1.08015989,   0.26339371,  -1.89274863,   0.11078428,   1.67623079,   1.72214117,   0.36677162,   1.11681643,  -0.08586041,   1.12827193,  -0.37029315,   0.85006231,   0.81614093,   0.20264799,   0.07733847
        b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18, b19, b20 = -5.56519485,   3.89898265,  -3.53680675,  -1.15066067,  -0.05588312,   0.37819470,  -4.19636633,   0.59276542,  -3.93918703,   1.16943985  ,   0.31420272,   2.34571497,  -0.38274056,   1.15966976,   0.37615318,   0.67143191,   0.80862093,   0.45058006,   0.49416314,  0.03708352

    elif (filt=='F1000W'):
        a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20 = 0.00000000,   0.00000000,  -0.02251778,  -5.38936612,  -0.30908362,  -0.95940688,   0.41898030,  -1.86130376,   0.12112129,   1.34224491,   1.66266419,   0.26796601,   1.10563336,  -0.08380422,   1.00162227,  -0.30080805,   0.58447049,   0.58039121,   0.20176272,   0.07514613
        b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18, b19, b20 = -5.54136026,   3.97847939,  -3.55639311,  -1.16696617,  -0.02321280,   0.27542392,  -4.23658223,   0.57505956,  -3.97963174,   1.19202272,   0.46739314,   2.42806233,  -0.38479755,   1.15985360,   0.58046545,   1.10238491,   1.00731906,   0.36590502,   0.48738257,  0.07733359

    else:
        print('')
        print(' FILTER NOT SUPPORTED. STOP!')
        print('')
        sys.exit()

    xref, yref = 693.5, 512.5

    xt = (xr-xref)/xref
    yt = (yr-yref)/yref

    dx = a1*xt + a2*yt + a3*xt**2 + a4*xt*yt + a5*yt**2 + a6*xt**3 + a7*xt**2*yt + a8*xt*yt**2 + a9*yt**3 + a10*xt**4 + a11*xt**3*yt + a12*xt**2*yt**2 + a13*xt*yt**3 + a14*yt**4 + a15*xt**5 + a16*xt**4*yt + a17*xt**3*yt**2 + a18*xt**2*yt**3 + a19*xt*yt**4 + a20*yt**5
    dy = b1*xt + b2*yt + b3*xt**2 + b4*xt*yt + b5*yt**2 + b6*xt**3 + b7*xt**2*yt + b8*xt*yt**2 + b9*yt**3 + b10*xt**4 + b11*xt**3*yt + b12*xt**2*yt**2 + b13*xt*yt**3 + b14*yt**4 + b15*xt**5 + b16*xt**4*yt + b17*xt**3*yt**2 + b18*xt**2*yt**3 + b19*xt*yt**4 + b20*yt**5

    xc = xr + dx
    yc = yr + dy

    return xc, yc





# Compute table of residual correction
def table(xr, yr, filt):

    xc, yc = np.zeros(len(xr)), np.zeros(len(yr))

    if ((filt=='F560W') or (filt=='F770W') or (filt=='F1000W')):

        # X grid points
        tabcor1 = [      0.0000,      0.0000,    236.0000,    236.0000,      0.0000,      0.0000,    236.0000,    236.0000,      0.0000,      0.0000,    236.0000,    236.0000,      0.0000,      0.0000,      0.0000,    141.0000,    141.0000,    141.0000,    282.0000,    282.0000,    282.0000,    350.0000,    350.0000,    350.0000,    350.0000,    350.0000,    350.0000,    350.0000,    350.0000,    350.0000,    350.0000,    350.0000,    350.0000,    477.8750,    477.8750,    477.8750,    477.8750,    477.8750,    477.8750,    477.8750,    477.8750,    477.8750,    477.8750,    477.8750,    477.8750,    563.1250,    563.1250,    563.1250,    563.1250,    563.1250,    563.1250,    563.1250,    563.1250,    563.1250,    563.1250,    563.1250,    563.1250,    648.3750,    648.3750,    648.3750,    648.3750,    648.3750,    648.3750,    648.3750,    648.3750,    648.3750,    648.3750,    648.3750,    648.3750,    733.6250,    733.6250,    733.6250,    733.6250,    733.6250,    733.6250,    733.6250,    733.6250,    733.6250,    733.6250,    733.6250,    733.6250,    818.8750,    818.8750,    818.8750,    818.8750,    818.8750,    818.8750,    818.8750,    818.8750,    818.8750,    818.8750,    818.8750,    818.8750,    904.1250,    904.1250,    904.1250,    904.1250,    904.1250,    904.1250,    904.1250,    904.1250,    904.1250,    904.1250,    904.1250,    904.1250,   1032.0000,   1032.0000,   1032.0000,   1032.0000,   1032.0000,   1032.0000,   1032.0000,   1032.0000,   1032.0000,   1032.0000,   1032.0000,   1032.0000]
        # Y grid points
        tabcor2 = [     18.0000,    244.0000,     18.0000,    244.0000,    244.0000,    470.0000,    244.0000,    470.0000,    470.0000,    696.0000,    470.0000,    696.0000,    746.0000,    885.6667,   1024.0000,    746.0000,    885.6667,   1024.0000,    746.0000,    885.6667,   1024.0000,      0.0000,    127.9583,    213.2917,    298.6250,    383.9583,    469.2917,    554.6250,    639.9583,    725.2917,    810.6250,    895.9583,   1024.0000,      0.0000,    127.9583,    213.2917,    298.6250,    383.9583,    469.2917,    554.6250,    639.9583,    725.2917,    810.6250,    895.9583,   1024.0000,      0.0000,    127.9583,    213.2917,    298.6250,    383.9583,    469.2917,    554.6250,    639.9583,    725.2917,    810.6250,    895.9583,   1024.0000,      0.0000,    127.9583,    213.2917,    298.6250,    383.9583,    469.2917,    554.6250,    639.9583,    725.2917,    810.6250,    895.9583,   1024.0000,      0.0000,    127.9583,    213.2917,    298.6250,    383.9583,    469.2917,    554.6250,    639.9583,    725.2917,    810.6250,    895.9583,   1024.0000,      0.0000,    127.9583,    213.2917,    298.6250,    383.9583,    469.2917,    554.6250,    639.9583,    725.2917,    810.6250,    895.9583,   1024.0000,      0.0000,    127.9583,    213.2917,    298.6250,    383.9583,    469.2917,    554.6250,    639.9583,    725.2917,    810.6250,    895.9583,   1024.0000,      0.0000,    127.9583,    213.2917,    298.6250,    383.9583,    469.2917,    554.6250,    639.9583,    725.2917,    810.6250,    895.9583,   1024.0000]
        # X correction
        tabcor3 = [ -0.0259610,  0.0964780, -0.1195105, -0.1195105, -0.0113855, -0.6051100,  0.2631700,  0.1334410,  0.0520025,  0.0714585, -0.3458305,  0.1579980, -0.0140135,  0.0971025,  0.0570430,  0.1144455,  0.0228485,  0.0602130,  0.1705470,  0.1425735,  0.0592925,  0.2333085,  0.0809205,  0.1670640,  0.1424650,  0.1944155,  0.1519545,  0.1833265,  0.2021595,  0.1883115,  0.1971175,  0.1460445,  0.1236275,  0.1988095,  0.2297960,  0.1994915,  0.2012905,  0.1459360,  0.1488745,  0.1248600,  0.1148460,  0.1307175,  0.1514290,  0.1687810,  0.1786445,  0.1818325,  0.1925755,  0.2302485,  0.2296155,  0.2296715,  0.1885915,  0.1641600,  0.1581580,  0.1352270,  0.1413130,  0.1440185,  0.1454275,  0.2423560,  0.1979490,  0.1893865,  0.1966060,  0.2157585,  0.2290360,  0.2439640,  0.2178210,  0.1986710,  0.1785885,  0.1447990,  0.1491590,  0.2467620,  0.2192925,  0.2090650,  0.2047150,  0.1633600,  0.2149340,  0.2548350,  0.2501475,  0.2428085,  0.2283495,  0.2134400,  0.1782210,  0.2855705,  0.2991625,  0.2854740,  0.2348225,  0.2149370,  0.2300035,  0.2458445,  0.2234405,  0.1989885,  0.2287430,  0.2476845,  0.2140235,  0.2522475,  0.2686355,  0.2703260,  0.2554125,  0.2432780,  0.2272500,  0.2435285,  0.2303420,  0.2195890,  0.2033290,  0.2268040,  0.2411380,  0.2557775,  0.2834985,  0.3091635,  0.2979695,  0.2923780,  0.2682450,  0.3086120,  0.2883970,  0.2849685,  0.2656340,  0.2682875,  0.1969335]
        # Y correction
        tabcor4 = [  0.1975205,  0.2942565,  0.0822160,  0.0822160,  0.1125385, -0.0327915, -0.0103370, -0.2474200, -0.3633220, -0.4723755, -0.0723835, -0.4716765, -0.1556200, -0.0891690, -0.0495665, -0.0674600, -0.1064665, -0.0733875, -0.1167985, -0.1199565, -0.0091325, -0.1657885, -0.2824360, -0.2128465, -0.1035110, -0.1254565, -0.2350820, -0.1290130, -0.1287595, -0.0919250, -0.1664510, -0.1122775, -0.0924955, -0.2052610, -0.2613910, -0.1902970, -0.1828815, -0.1555485, -0.1755545, -0.1588405, -0.1105195, -0.0855255, -0.0992950, -0.0987330, -0.0395805, -0.2364455, -0.2209070, -0.2089660, -0.1587215, -0.1602910, -0.2475070, -0.1560100, -0.0950535, -0.0617595, -0.0930235, -0.0772080, -0.0707280, -0.2025110, -0.2118465, -0.1582615, -0.1354400, -0.1567695, -0.2116860, -0.1605085, -0.1011020, -0.0357945, -0.0908235, -0.0782905, -0.0269685, -0.2400790, -0.2064630, -0.1743300, -0.1194270, -0.1332910, -0.1589720, -0.1411460, -0.1136930, -0.0855460, -0.0819715, -0.1011120,  0.0256650, -0.2223865, -0.2097545, -0.1967535, -0.1523880, -0.0812635, -0.1292495, -0.1316870, -0.1110090, -0.0235760, -0.0823505, -0.0919955,  0.0150775, -0.2071095, -0.1816255, -0.1795240, -0.1685815, -0.0958185, -0.0967395, -0.1027020, -0.1373720, -0.0498485, -0.0313265, -0.0419040, -0.0176220, -0.1480250, -0.1953435, -0.1920595, -0.1599335, -0.1270035, -0.1087825, -0.1061775, -0.0885140, -0.0958725, -0.0199830, -0.0186540, -0.0993460]

        for k in range(len(xr)):

            found = False
            # Lyot
            if ((xr[k]<=282) and (yr[k]>=746)):
                found = False
                ntab = len(tabcor1)
                for i in range(ntab):
                    j = i + 3 + 1
                    if ((i>ntab) or (j>ntab)):
                        continue
                    if ((xr[k]>=tabcor1[i]) and (xr[k]<=tabcor1[j]) and (yr[k]>=tabcor2[i]) and (yr[k]<=tabcor2[j])):
                        xcor1 = tabcor1[i]
                        ycor1 = tabcor2[i]
                        xcor2 = tabcor1[j]
                        ycor2 = tabcor2[j]
                        dxcor1 = tabcor3[i]
                        dycor1 = tabcor4[i]
                        dxcor2 = tabcor3[i+1]
                        dycor2 = tabcor4[i+1]
                        dxcor3 = tabcor3[j-1]
                        dycor3 = tabcor4[j-1]
                        dxcor4 = tabcor3[j]
                        dycor4 = tabcor4[j]
                        found = True
                        break
                        
            # Imager
            if (xr[k]>=350):
                found = False
                ntab = len(tabcor1)
                for i in range(ntab):
                    j = i + 12 + 1
                    if ((i>ntab) or (j>ntab)):
                        continue
                    if ((xr[k]>=tabcor1[i]) and (xr[k]<=tabcor1[j]) and (yr[k]>=tabcor2[i]) and (yr[k]<=tabcor2[j])):
                        xcor1 = tabcor1[i]
                        ycor1 = tabcor2[i]
                        xcor2 = tabcor1[j]
                        ycor2 = tabcor2[j]
                        dxcor1 = tabcor3[i]
                        dycor1 = tabcor4[i]
                        dxcor2 = tabcor3[i+1]
                        dycor2 = tabcor4[i+1]
                        dxcor3 = tabcor3[j-1]
                        dycor3 = tabcor4[j-1]
                        dxcor4 = tabcor3[j]
                        dycor4 = tabcor4[j]
                        found = True
                        break
            if (found):
                fx = (xr[k]-xcor1)/(xcor2-xcor1)
                fy = (yr[k]-ycor1)/(ycor2-ycor1)

                dx = (1-fx)*(1-fy)*dxcor1 + (1-fx)*(fy)*dxcor2 + (fx)*(1-fy)*dxcor3 + (fx)*(fy)*dxcor4
                dy = (1-fx)*(1-fy)*dycor1 + (1-fx)*(fy)*dycor2 + (fx)*(1-fy)*dycor3 + (fx)*(fy)*dycor4

                xc[k] = xr[k] + dx
                yc[k] = yr[k] + dy
    
        return xc, yc

    else:
        print('')
        print(' FILTER NOT SUPPORTED. STOP!')
        print('')
        sys.exit()

    return xc, yc





def miri_gdc(xr, yr, filt):

    if ((filt!='F560W') and (filt!='F770W') and (filt!='F1000W')):
        print('')
        print(' FILTER NOT SUPPORTED. STOP!')
        print('')
        sys.exit()

    xtmp, ytmp = poly(xr, yr, filt)
    dx = xtmp-xr
    dy = ytmp-yr

    xc, yc = table(xr, yr, filt)
    xc += dx
    yc += dy

    # 4QPM regions are excluded. Return 0
    for x, y, xo, yo in zip(xr, yr, xc, yc):
        if (not (((x<=282) and (y>=746)) or (x>=350))):
            xo, yo = 0.0, 0.0

    return xc, yc
    




if (len(sys.argv)!=4):
    print('')
    print(' miri_raw2corr.py FILTER_NAME INPUT_CATALOG OUTPUT_CATALOG')
    print('')
    print(' INPUT_CATALOG needs (xraw,yraw) in the first two columns.')
    print('')
    print(' (xraw,yraw) must be in the 1-index system.')
    print('')
    sys.exit()



filt = sys.argv[1]

if ((filt!='F560W') and (filt!='F770W') and (filt!='F1000W')):
    print('')
    print(' FILTER NOT SUPPORTED. STOP!')
    print('')
    sys.exit()
        


input_file = sys.argv[2]
output_file = sys.argv[3]

data = pd.read_csv(input_file, comment="#", sep="\s+", usecols=[0, 1], names=['x', 'y'])
xraw, yraw = data.x.values, data.y.values

xcorr, ycorr = miri_gdc(xraw, yraw, filt)

with open(output_file, 'w') as f:
    f.write('# xcorr       ycorr\n')
    for i in range(len(xcorr)):
        f.write('{0:10.4f} {1:10.4f}\n'.format(xcorr[i],ycorr[i]))

