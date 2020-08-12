from opentrons import protocol_api

metadata= {'apiLevel': '2.1'}

#Standard layouts of plates used, to make my life easy (You can ignore this)

well_block = [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12'],
              ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12'],
              ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12'],
              ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12'],
              ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12'],
              ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12'],
              ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12'],
              ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12']]

reservoirs = ['A1', 'A3', 'A5', 'A7', 'A9', 'A11', 'A13', 'A15', 'A17', 'A19', 'A21', 'A23',
              'C1', 'C3', 'C5', 'C7', 'C9', 'C11', 'C13', 'C15', 'C17', 'C19', 'C21', 'C23',
              'E1', 'E3', 'E5', 'E7', 'E9', 'E11', 'E13', 'E15', 'E17', 'E19', 'E21', 'E23',
              'G1', 'G3', 'G5', 'G7', 'G9', 'G11', 'G13', 'G15', 'G17', 'G19', 'G21', 'G23',
              'I1', 'I3', 'I5', 'I7', 'I9', 'I11', 'I13', 'I15', 'I17', 'I19', 'I21', 'I23',
              'K1', 'K3', 'K5', 'K7', 'K9', 'K11', 'K13', 'K15', 'K17', 'K19', 'K21', 'K23',
              'M1', 'M3', 'M5', 'M7', 'M9', 'M11', 'M13', 'M15', 'M17', 'M19', 'M21', 'M23',
              'O1', 'O3', 'O5', 'O7', 'O9', 'O11', 'O13', 'O15', 'O17', 'O19', 'O21', 'O23']

well_twos = ['A2', 'A4', 'A6', 'A8', 'A10', 'A12', 'A14', 'A16', 'A18', 'A20', 'A22', 'A24',
             'C2', 'C4', 'C6', 'C8', 'C10', 'C12', 'C14', 'C16', 'C18', 'C20', 'C22', 'C24',
             'E2', 'E4', 'E6', 'E8', 'E10', 'E12', 'E14', 'E16', 'E18', 'E20', 'E22', 'E24',
             'G2', 'G4', 'G6', 'G8', 'G10', 'G12', 'G14', 'G16', 'G18', 'G20', 'G22', 'G24',
             'I2', 'I4', 'I6', 'I8', 'I10', 'I12', 'I14', 'I16', 'I18', 'I20', 'I22', 'I24',
             'K2', 'K4', 'K6', 'K8', 'K10', 'K12', 'K14', 'K16', 'K18', 'K20', 'K22', 'K24',
             'M2', 'M4', 'M6', 'M8', 'M10', 'M12', 'M14', 'M16', 'M18', 'M20', 'M22', 'M24',
             'O2', 'O4', 'O6', 'O8', 'O10', 'O12', 'O14', 'O16', 'O18', 'O20', 'O22', 'O24']

well_ones = ['B2', 'B4', 'B6', 'B8', 'B10', 'B12', 'B14', 'B16', 'B18', 'B20', 'B22', 'B24',
             'D2', 'D4', 'D6', 'D8', 'D10', 'D12', 'D14', 'D16', 'D18', 'D20', 'D22', 'D24',
             'F2', 'F4', 'F6', 'F8', 'F10', 'F12', 'F14', 'F16', 'F18', 'F20', 'F22', 'F24',
             'H2', 'H4', 'H6', 'H8', 'H10', 'H12', 'H14', 'H16', 'H18', 'H20', 'H22', 'H24',
             'J2', 'J4', 'J6', 'J8', 'J10', 'J12', 'J14', 'J16', 'J18', 'J20', 'J22', 'J24',
             'L2', 'L4', 'L6', 'L8', 'L10', 'L12', 'L14', 'L16', 'L18', 'L20', 'L22', 'L24',
             'N2', 'N4', 'N6', 'N8', 'N10', 'N12', 'N14', 'N16', 'N18', 'N20', 'N22', 'N24',
             'P2', 'P4', 'P6', 'P8', 'P10', 'P12', 'P14', 'P16', 'P18', 'P20', 'P22', 'P24']

conditions = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',
              'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12',
              'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12',
              'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12',
              'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',
              'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
              'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12',
              'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12']


# Specify the range of the block of conditions you want to use
# For example rows A through E and Columns 1-10 would be: starting_row =1 Max_row = 5  starting_column = 1 Max_column = 10
starting_row = 1
max_row = 5
starting_column = 1
max_column = 8
sources = []
# sources = [well for row in well_block[(starting_row-1):max_row] for well in row[(starting_col-1):max_column]]
for row in well_block[(starting_row-1):max_row]:
    for well in row[(starting_column-1):max_column]:
        sources.append(well)
print (sources)

## Specify reservoir volume to be dispensed (ul)
res_vol = 50

## Specify aspiration and dispense heights (mm above bottom of well to aspirate or dispense) (default: 1mm)
## This matters when your well is very full and you don't want the pipette to displace all the liquid
condition_asp_height = 10
reservoir_asp_height = 1
protein_asp_height = 0.5
drop_disp_height = 0.3

## Specify drop volumes to be dispensed (ul) (minimum = 1 uL)
prot_drop1 = 1
res_drop1 = 1
prot_drop2 = 1
res_drop2 = 1

###!!!!##### IMPORTANT! Currently Multichannel does not support 2 drops. This is a BUG that has not been updated yet in the Official Opentrons Code

## Specify whether you want to set two drops (True or False (watch spelling, they need to start with capital))

two_drops = True

## Specify whether you are using single channel p20 pipette for drops or Multichannel p10 ('single' or 'multi')
pipette_type = 'multi'

#specify protein location on the deck:  [Slot, tube_well1,tube_well2, etc]
#Tube(s) will be placed on 96-well Aluminium block. Have same number of tubes as rows of conditions when using the multichannel
### E.G. When you have conditions from A1 through D7 then place tubes of protein with relevant volume in A1, B1, C1 and D1
### When setting 2 drops with different protein sources (e.g. 2 different compounds) put the different protein in a separate column
### And add the location of the second column to the list below
protein_location = ["8","A1","A2"]

##If you set 2 drops to True this will create a crystallisation plate with 2 'different' proteins. ONLY WORKS WITH SINGLE CHANNEL!!


##########################################################################################################
## Everything before this line should be set to what you want


# This translates the condition locations to reservoir and drop locations
res_destination = []
well_one_destination = []
well_two_destination = []
for well in sources:
    res_destination.append(reservoirs[conditions.index(well)])
    well_one_destination.append(well_ones[conditions.index(well)])
    well_two_destination.append(well_twos[conditions.index(well)])


def run(protocol: protocol_api.ProtocolContext):
    #Load Labware
    temp_mod = protocol.load_module('Temperature Module', '9')
    cryst_plate = temp_mod.load_labware('swissci_2_well_crystallisation_plate',
                                        label='Temp-controlled crystallisation plate')
    prot_block = protocol.load_labware("opentrons_96_aluminumblock_generic_pcr_strip_200ul",
                                       protein_location[0],label="Protein container")
    condition_block = protocol.load_labware("usascientific_96_wellplate_2.4ml_deep",'11')
    tiprack1 = protocol.load_labware("opentrons_96_tiprack_20ul",'4')
    tiprack2 = protocol.load_labware("opentrons_96_tiprack_20ul",'5')
    tiprack3 = protocol.load_labware("opentrons_96_tiprack_20ul",'6')
    tiprack4 = protocol.load_labware("opentrons_96_tiprack_300ul",'10')
    
    ##Transfer conditions to crystallisation plate
    
    if max_row == 8:
        p50 = protocol.load_instrument('p50_multi',"left",tip_racks=[tiprack4])
        p50.well_bottom_clearance.aspirate = condition_asp_height
        p50.flow_rate.aspirate = 10
        p50.flow_rate.dispense = 20
        p50.transfer(res_vol, [condition_block.wells_by_name()[well_name] for well_name in sources],
                 [cryst_plate.wells_by_name()[well_name] for well_name in res_destination], new_tip ='always',mix_before=(3,50))
    elif max_row < 8:
        p50 = protocol.load_instrument('p50_multi',"left")
        p50.well_bottom_clearance.aspirate = condition_asp_height
        p50.flow_rate.aspirate = 10
        p50.flow_rate.dispense = 20
        tiprow = chr(ord("H") - (max_row-starting_row))
        for tipcolumn in range(starting_column,(max_column+1)):
            tipwell = tiprow + str(tipcolumn)
            p50.pick_up_tip(tiprack4.wells_by_name()[tipwell])
            p50.transfer(res_vol, condition_block.columns_by_name()[str(tipcolumn)],
                         cryst_plate.columns_by_name()[str(tipcolumn + (tipcolumn-1))],mix_before=(3,50), new_tip ='never')   
            p50.drop_tip()
    
    if pipette_type == 'single':
        p20 = protocol.load_instrument('p20_single_gen2',"right",tip_racks=[tiprack1,tiprack2,tiprack3])
        p20.well_bottom_clearance.aspirate = protein_asp_height
        p20.well_bottom_clearance.dispense = drop_disp_height
        ## Transfer protein from tube to crystallisation plate drop wells 1
        p20.distribute(prot_drop1,prot_block.wells_by_name()[protein_location[1]],
                       [cryst_plate.wells_by_name()[well_name] for well_name in well_one_destination],touch_tip=True)

        ## Transfer protein to second drop well if desired (see above to set variable)
        if two_drops == True:
            p20.distribute(prot_drop2,prot_block.wells_by_name()[protein_location[2]],
                           [cryst_plate.wells_by_name()[well_name] for well_name in well_two_destination],touch_tip=True)

        # add Reservoir solution to drops
        p20.flow_rate.aspirate = 1
        p20.flow_rate.dispense = 1
        p20.well_bottom_clearance.aspirate = reservoir_asp_height
        p20.well_bottom_clearance.dispense = drop_disp_height

        if two_drops == True:
            for loc, well_name in enumerate(res_destination):
                p20.pick_up_tip()
                p20.transfer(res_drop1,cryst_plate.wells_by_name()[well_name],
                             cryst_plate.wells_by_name()[well_one_destination[loc]],new_tip='never')
                p20.transfer(res_drop2,cryst_plate.wells_by_name()[well_name],
                             cryst_plate.wells_by_name()[well_two_destination[loc]],new_tip='never')
                p20.drop_tip()
        else:
            p20.transfer(res_drop1,[cryst_plate.wells_by_name()[well_name] for well_name in res_destination],
                     [cryst_plate.wells_by_name()[well_name] for well_name in well_one_destination],new_tip='always')

    elif pipette_type == 'multi':
        ##Grab reservoir source and drop-well destinations
        pipette_row = chr(64+starting_row)
        dest = [cryst_plate.wells_by_name()[well_name] for well_name in well_two_destination if pipette_row in well_name]
        sourc = [cryst_plate.wells_by_name()[well_name] for well_name in res_destination if pipette_row in well_name]
        
        if max_row == 8:
            p10 = protocol.load_instrument('p10_multi',"right",tip_racks=[tiprack1,tiprack2,tiprack3])
            p10.well_bottom_clearance.aspirate = protein_asp_height
            p10.well_bottom_clearance.dispene = drop_disp_height
            p10.flow_rate.aspirate = 1
            p10.flow_rate.dispense = 1
            
            ##Dispense protein drops
            p10.distribute(prot_drop1,prot_block.wells_by_name()[protein_location[1]],dest,touch_tip=True)
            ##Dispense Reservoir drops
            p10.well_bottom_clearance.aspirate = reservoir_asp_height
            p10.transfer(res_drop1,sourc,dest,new_tip='always')

        elif max_row < 8:
            p10 = protocol.load_instrument('p10_multi',"right")
            p10.well_bottom_clearance.aspirate = protein_asp_height
            p10.well_bottom_clearance.dispene = drop_disp_height
            p10.flow_rate.aspirate = 1
            p10.flow_rate.dispense = 1
            
            ## Dispense Protein Drops
            tiprow = chr(ord("H") - (max_row-starting_row))
            p10.pick_up_tip(tiprack1.wells_by_name()[tiprow+"1"])
            p10.distribute(prot_drop1,prot_block.wells_by_name()[protein_location[1]],dest,touch_tip=True,new_tip='never')
            p10.drop_tip()
            ##Dispense Reservoir Drops
            p10.well_bottom_clearance.aspirate = reservoir_asp_height
            tipcol = 1
            for s,d in zip(sourc,dest):
                p10.pick_up_tip(tiprack2.wells_by_name()[(pipette_row+str(tipcol))])
                p10.transfer(res_drop1,s,d,new_tip='never')
                p10.drop_tip()
                tipcol +=1
      
           
    else:
        print("Error! Cannot determine which pipette you want to use!")
