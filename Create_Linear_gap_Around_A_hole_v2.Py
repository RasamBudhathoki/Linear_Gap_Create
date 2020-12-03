import os, sys

# written by R.Budhathoki
# Input

myfiles = os.listdir(os.getcwd())
start_IDs_file_name = 'Spigot_pin_Gap_Create_Input.csv'


# Opening starts IDs file
fopen =open (start_IDs_file_name, 'rb')
for line in fopen:
    line = line.strip('\r\n')
    if line !='':
        if 'Start_Node_ID' in line:
            Start_Node_ID = line.split(',')[1].strip()
        elif 'Start_CBUSH_ID' in line:
            Start_CBUSH_ID = line.split(',')[1].strip()        
        elif 'Start_Spoint_ID' in line:
            Start_Spoint_ID = line.split(',')[1].strip()
#

found = False
fout=open('FTB4_spigot_pins_Bearing_Linear_Gap_v7.gap','w')
fout1=open('FTB4_spigot_pins_Bearing_Linear_Gap_nodes_v7.dat','w')

Grid_cards_line =[]
mpc_Cards_line=[]
cbush_pbush_cards_line= []

for f in myfiles:
    if 'RBE2' in f and '.bdf' in f:
        found = True

        print '-'*30
        print 'Working on.....' + f


        data = []
        fopen =open (f, 'rb')
        for line in fopen:
            line = line.strip('\r\n')
            if line.startswith('GRID'):
                if '*' in line:
                    print 'Warning, This Tool works only with Nastran smalle field, GO Back and change the node card to Small field'
                    quit()
                else:
                   data.append(line)
            elif line.startswith('RBE2'):
                Start_RBE_ID =line[8:16].strip()
                RBE3_Center_Node_ID = line[16:24].strip()

                print 'RBE3 = ' + Start_RBE_ID
                print 'center_node iD = ' + RBE3_Center_Node_ID

                
#
        input_nodes_dict ={}
        for item in data:
            nodeid = item[8:16].strip()

            mydict={}
            mydict['GRID'] = item[0:8].strip()
            mydict['ID'] = item[8:16].strip()
            mydict['CP'] = item[16:24].strip()
            mydict['X1'] = item[24:32].strip()
            mydict['X2'] = item[32:40].strip()
            mydict['X3'] = item[40:48].strip()
            mydict['CD'] = item[48:56].strip()
            mydict['PS'] = item[56:64].strip()
            mydict['SEID'] = item[64:72].strip()

    
            input_nodes_dict[nodeid] = mydict

            if nodeid !=RBE3_Center_Node_ID:
                cbush_coord_id = mydict['CD'].strip()
                if mydict['CD'].strip()=='':
                    print 'Nodes around the circular must contain analysis coord sys !!'
                    quit()
        ################
        RBE3_independant_nodes =[]
        gap_nodes_list=[]
        Cbush_nodes_list=[]
        
        i=int(float(Start_Node_ID))

        for nodeid in  input_nodes_dict.keys():
            #
            if nodeid==RBE3_Center_Node_ID:
                continue
            else:
                cbush_first_node = str(i)
                cbush_second_node = str(i+1)
                RBE3_independant_nodes.append(cbush_second_node)
                #
                mydict={}
                mydict['Gap_Opening_Node']=nodeid
                mydict['Gap_closing_Node']=cbush_first_node
                gap_nodes_list.append(mydict)
                #
                mydict={}
                mydict['cbush_Node_A']=cbush_first_node
                mydict['cbush_Node_B']=cbush_second_node
                Cbush_nodes_list.append(mydict)
                #
                grid_ref_data_dict=input_nodes_dict[nodeid]

                node_card1= '%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s'%('GRID',cbush_first_node,grid_ref_data_dict['CP'] ,grid_ref_data_dict['X1'],grid_ref_data_dict['X2'],
                                                            grid_ref_data_dict['X3'],grid_ref_data_dict['CD'],grid_ref_data_dict['PS'],grid_ref_data_dict['SEID']  )
                node_card2= '%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s'%('GRID',cbush_second_node,grid_ref_data_dict['CP'] ,grid_ref_data_dict['X1'],grid_ref_data_dict['X2'],
                                                            grid_ref_data_dict['X3'],grid_ref_data_dict['CD'],grid_ref_data_dict['PS'],grid_ref_data_dict['SEID']  )
                Grid_cards_line.append(node_card1)
                Grid_cards_line.append(node_card2)
                i= i +2
            #print nodeid, input_nodes_dict[nodeid]
        Start_Node_ID =str(i)
        Grid_cards_line.append('$$')

        ################################################################
        #Creating pbush Cards...
        pbush_card ='%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s'% ('PBUSH',Start_CBUSH_ID,'K','1.+9','1.+9','1.+9','1.+9','1.+9','1.+9')
        #fout.write('%s\n'%pbush_card)
        #fout.write('$\n')
        cbush_pbush_cards_line.append(pbush_card)
        cbush_pbush_cards_line.append('$')
        #print 'Creating Pbush Property.....Done!!!!'
        ################################################################

        # Creating Cbush Cards.....
        i=int(float(Start_CBUSH_ID))
        for item in Cbush_nodes_list:
            Node_A =item['cbush_Node_A']
            Node_B = item['cbush_Node_B']
            cbush_card ='%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s'% ('CBUSH',str(i),Start_CBUSH_ID, Node_A, Node_B,'','','',cbush_coord_id)
            #fout.write('%s\n'%cbush_card)
            cbush_pbush_cards_line.append(cbush_card)
            cbush_card ='%-8s%-8s'% ('','.5')
            #fout.write('%s\n'%cbush_card)
            cbush_pbush_cards_line.append(cbush_card)
            i = i+1
        Start_CBUSH_ID = str(i) 
        #print 'Creating Cbush Elements.....Done!!!!'

        # Creating RBE2 Elements
        RBE_Card_line = '%-8s%-8s%-8s%-8s'%('RBE2',Start_RBE_ID,RBE3_Center_Node_ID,'123456')

        j = len(RBE3_independant_nodes)
        if j<6:
            for mpc_node in RBE3_independant_nodes:
                RBE_Card_line=RBE_Card_line+('%-8s'%mpc_node)
            #fout.write('%s\n'%RBE_Card_line)
            mpc_Cards_line.append(RBE_Card_line)
        else:
            for mpc_node in RBE3_independant_nodes:
                if len(RBE_Card_line)==72:
                    #fout.write('%s\n'%RBE_Card_line)
                    mpc_Cards_line.append(RBE_Card_line)
                    RBE_Card_line='        '

                RBE_Card_line=RBE_Card_line+('%-8s'%mpc_node)
            
                j = j-1

            #fout.write('%s\n'%RBE_Card_line)
            mpc_Cards_line.append(RBE_Card_line)
        #print 'Creating RBE2.....Done!!!!'
        ####

        #print 'Creating Linear Gap SPOINT, SUPPORT, MPC, SPC Cards.....'
        fout.write('$$ Linear Gap Elements\n')

        i=int(float(Start_Spoint_ID))
        for item in gap_nodes_list:
            Gap_Opening_Node=item['Gap_Opening_Node']
            Gap_closing_Node=item['Gap_closing_Node']

            comment_line ='$gap between grid '+Gap_Opening_Node+' dof 1 and grid '+Gap_closing_Node+' dof 1 init opening = 0.0   '
            fout.write('%s\n'%comment_line)

            spoint_line= '%-8s%-8s%-8s'%('SPOINT',str(i),str(i+1))
            fout.write('%s\n'%spoint_line)
            #
            support_line= '%-8s%-8s%-8s'%('SUPORT',str(i),'0')
            fout.write('%s\n'%support_line)
            #
            spc_line= '%-8s%-8s%-8s%-8s%-8s'%('SPC','101106',str(i+1),'0','0.0')
            fout.write('%s\n'%spc_line)
            mpc_line= '%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s'%('MPC','101106',Gap_Opening_Node,'1','1.',Gap_closing_Node,'1','-1.')
            fout.write('%s\n'%mpc_line)
            mpc_line= '%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s'%('','',str(i),'0','1.',str(i+1),'0','-1.')
            fout.write('%s\n'%mpc_line)
            i=i+2
        Start_Spoint_ID= str(i)   
        
################################################################
###############################################################################
fout1.write('$$High Stiff Cbush\n')
for item in cbush_pbush_cards_line:
    fout1.write('%s\n'%item)
fout1.write('$$\n')
fout1.write('$$RBE2\n')
for item in mpc_Cards_line:
    fout1.write('%s\n'%item)
fout1.write('$$\n')
#
fout1.write('$$Nodes\n')
for item in Grid_cards_line:
    fout1.write('%s\n'%item)
fout1.write('$$\n')
#
if not found:
    print 'Warning !!!!!! No MPC input bdf file is found'
fout.close()
fout1.close()
print '\n'
print 'Job Complete!!!!'








