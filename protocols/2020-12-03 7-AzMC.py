# opentrons robot pipeting protocol
# 2020-12-03
# by Dalibor Nakladal
# objective: screen compound library in CBS activity assay

# Notes
# - do not use touch tip, this guarantees losing tips
# - use blow-out with repeated transfers, otherwise the tip fills up

from opentrons import protocol_api

metadata = {'apiLevel': '2.5'}

def run(protocol: protocol_api.ProtocolContext):
    #######################################################################################################################################
    ## SETUP LABWARE
    
    # Load Labware
    temp_mod = protocol.load_module('Temperature Module', '9')
    reaction_plate = temp_mod.load_labware("biorad_384_wellplate_50ul", label = "reaction plate") # where the magic happens
    reservoir_plate = protocol.load_labware("usascientific_12_reservoir_22ml", "6", label = 'reservoir plate') # reaction mix
    library_1 = protocol.load_labware("greiner_96_wellplate_323ul", "4", label = "library 1") # library 'morning'
    library_2 = protocol.load_labware("greiner_96_wellplate_323ul", "5", label = "library 2") # library 'morning 10x diluted'
    library_3 = protocol.load_labware("greiner_96_wellplate_323ul", "7", label = "library 3") # library 'afternoon'
    library_4 = protocol.load_labware("greiner_96_wellplate_323ul", "8", label = "library 4") # library 'afternoon 10x diluted'
    
    # Specify tip racks
    tiprack1 = protocol.load_labware("opentrons_96_tiprack_10ul", '1')
    tiprack2 = protocol.load_labware("opentrons_96_tiprack_10ul", '2')
    tiprack3 = protocol.load_labware("opentrons_96_tiprack_10ul", '3')

    # Load pipettes and set parameters
    p10 = protocol.load_instrument("p10_multi", "right", tip_racks = [tiprack1, tiprack2, tiprack3])

    p10.flow_rate.aspirate = 8
    p10.flow_rate.dispense = 8

    # 384-well depth is 11.56 mm and max volume is 50 uL
    # 20 uL is 2 mm high, tandem (middle) wall is 5.1 mm high
    p10.well_bottom_clearance.dispense = 1

    #######################################################################################################################################
    ## SETUP LOCATIONS

    # Specify target wells
    reagents = ["1"] # columns on reservoir plate
    # reaction
    cols_reaction = list(range(1, 17)) # destination wells in reaction plate (Bio-Rad hardshell 384-well)
    wells_reaction = ['A' + str(i) for i in cols_reaction] + ['B' + str(i) for i in cols_reaction]
    
    # libraries
    lib1_cols = [1, 2, 3, 4, 5, 6, 7, 11, 12] # library columns to aspirate compounds from
    lib2_cols = [1, 2, 3, 4, 5, 6, 7, 11, 12]
    lib3_cols = [1, 2, 3, 4, 5, 6, 7]
    lib4_cols = [1, 2, 3, 4, 5, 6, 7]
    wells_1 = ['A' + str(i) for i in list(range(1, 10))] # target wells for library compounds
    wells_2 = ['B' + str(i) for i in list(range(1, 10))]
    wells_3 = ['A' + str(i) for i in list(range(10, 17))]
    wells_4 = ['B' + str(i) for i in list(range(10, 17))]

    #######################################################################################################################################
    ## PROCEDURE

    # Distribute substrate mixed with fluorescent dye and enzyme
    vol = 18
    p10.transfer(vol, reservoir_plate.columns_by_name()[reagents[0]], [reaction_plate.wells_by_name()[i] for i in wells_reaction],
    disposal_volume = 0, blow_out = False, new_tip = 'once')

    # Distribute compounds from 96-well libraries
    vol = 2
    # library 1 in wells A1-A12
    cols = lib1_cols
    for i in range(0, len(cols)):
        p10.transfer(vol, library_1.columns_by_name()[str(cols[i])], reaction_plate.wells_by_name()[wells_1[i]])

    # library 2 in wells B1-B12
    cols = lib2_cols
    for i in range(0, len(cols)):
        p10.transfer(vol, library_2.columns_by_name()[str(cols[i])], reaction_plate.wells_by_name()[wells_2[i]])

    # library 3 in wells A13-A24
    cols = lib3_cols
    for i in range(0, len(cols)):
        p10.transfer(vol, library_3.columns_by_name()[str(cols[i])], reaction_plate.wells_by_name()[wells_3[i]])

    # library 4 in wells B13-24 
    cols = lib4_cols
    for i in range(0, len(cols)):
        p10.transfer(vol, library_4.columns_by_name()[str(cols[i])], reaction_plate.wells_by_name()[wells_4[i]])