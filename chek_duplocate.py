import os, sys
####################
inputfile1 = 'FTB4_spigot_pins_Bearing_Linear_Gap_nodes_v7.dat'
inputfile2 = 'FTB4_spigot_pins_Bearing_Linear_Gap_v7.gap'
##############
data =[]

fopen =open (inputfile1, 'rb')
for line in fopen:
    line = line.strip('\r\n')
    data.append(line)

fopen.close()

fopen =open (inputfile2, 'rb')
for line in fopen:
    line = line.strip('\r\n')
    data.append(line)

fopen.close()



grids = []
spoints = []
cbushids = []

duplicate_grids =[]
duplicate_spoint =[]
duplicate_cbush =[]

for item in data:
    if item.startswith('GRID '):
        nodeid = item[8:16].strip()
        if nodeid not in grids:
            grids.append(nodeid)
        else:
            duplicate_grids.append(nodeid)
    elif item.startswith('SPOINT '):
        spoint1 = item[8:16].strip()
        spoint2 = item[16:24].strip()
        
        if spoint1 not in spoints:
            spoints.append(spoint1)
        else:
            duplicate_spoint.append(spoint1)
        if spoint2 not in spoints:
            spoints.append(spoint2)
        else:
            duplicate_spoint.append(spoint2)
    elif item.startswith('CBUSH '):
        cbush = item[8:16].strip()
        if cbush not in cbushids:
            cbushids.append(cbush)
        else:
            duplicate_cbush.append(cbush)

if len(duplicate_grids) ==0:
    print 'NO duplicate nodes found'

if len(duplicate_spoint) ==0:
    print 'NO duplicate Spoints found'    

if len(duplicate_cbush) ==0:
    print 'NO duplicate Cbush found'    
