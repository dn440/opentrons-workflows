# opentrons robot pipeting protocol
# 2020-12-03
# by Dalibor Nakladal
# objective: screen compound library in CBS activity assay

# Notes: do not use touch tip, this guarantees losing tips

from opentrons import protocol_api

metadata = {'apiLevel': '2.5'}

def run(protocol: protocol_api.ProtocolContext):
    #######################################################################################################################################
    ## SETUP
    
    # Load Labware
    temp_mod = protocol.load_module('Temperature Module', '9')
    reaction_plate = temp_mod.load_labware("biorad_384_wellplate_50ul", label = "reaction plate") # where the magic happens
    library_1 = protocol.load_labware("greiner_96_wellplate_323ul", "4", label = "library 1") # library 'morning'
    reagent_plate = protocol.load_labware("greiner_96_wellplate_323ul", "6", label = "reagents")
    
    # Specify tip racks
    tiprack1 = protocol.load_labware("opentrons_96_tiprack_10ul", '1')

    # Load pipettes and set parameters
    p10 = protocol.load_instrument("p10_multi", "right", tip_racks = [tiprack1])
    p50 = protocol.load_instrument('p50_multi', "left", tip_racks = [tiprack2])

    p10.flow_rate.aspirate = 8
    p10.flow_rate.dispense = 8

    # 384-well depth is 11.56 mm and max volume is 50 uL
    # 20 uL is 2 mm high, tandem (middle) wall is 5.1 mm high
    p10.well_bottom_clearance.dispense = 1

    # Specify target wells
    reagents = ["1", "2"] # columns on reagent plate for substrate and enzyme
    # reaction
    cols_reaction = list(range(1, 13)) # destination wells in reaction plate (Bio-Rad hardshell 384-well)
    wells_reaction = ['A' + str(i) for i in cols_reaction]
    
    # libraries
    lib1_cols = [1, 2, 3, 4, 5, 6, 7, 11, 12] # library columns to aspirate compounds from
    wells_1 = ['A' + str(i) for i in list(range(1, 13))] # target wells for library compounds

    #######################################################################################################################################
    ## PROCEDURE

    # mix substrate and enzyme
    p50.transfer(100, reagent_plate.columns_by_name()[reagents[0]], reagent_plate.columns_by_name()[reagents[1]], mix_after = (3, 40))

    # Distribute substrate mixed with fluorescent dye and enzyme
    p10.distribute(18, reagent_plate.columns_by_name()[reagents[1]], [reaction_plate.wells_by_name()[i] for i in wells_reaction],
    disposal_volume = 1, blow_out = True, new_tip = 'once')

    # Distribute compounds from 96-well library
    # library 1 in wells A1-A12
    for i in range(0, len(cols)):
        p10.transfer(2, library_1.columns_by_name()[str(lib1_cols[i])], reaction_plate.wells_by_name()[wells_1[i]])