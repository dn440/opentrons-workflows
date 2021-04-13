# opentrons robot pipeting protocol
# by Dalibor Nakladal
# objective: optimize pipetting volume accuracy for 384-well plates #HSP3841

# Notes:
# when using touch tip, this usually lost the tips, but might be optimized?
# test 8, 10, and 8+10 uL volumes; 2uL added to 8 and then another 10 will be tested another day
# can the p300 be used for these volumes?

from opentrons import protocol_api

metadata = {'apiLevel': '2.5'}

def run(protocol: protocol_api.ProtocolContext):
    #######################################################################################################################################
    ## SETUP
    
    # Load Labware
    temp_mod = protocol.load_module('Temperature Module', '9')
    reaction_plate = temp_mod.load_labware("corning_384_wellplate_112ul_flat", label = "reaction plate") # where the magic happens
    reagent_plate = protocol.load_labware("greiner_96_wellplate_323ul", "6", label = "reagents")
    
    # Specify tip racks
    tiprack1 = protocol.load_labware("opentrons_96_tiprack_10ul", '5')
    tiprack2 = protocol.load_labware("opentrons_96_tiprack_300ul", '8')

    # Load pipettes and set parameters
    p10 = protocol.load_instrument("p10_multi", "right", tip_racks = [tiprack1])
    p50 = protocol.load_instrument('p50_multi', "left", tip_racks = [tiprack2])

    # Aspirate has the default flowrate of 150 ul/s
    # p10.flow_rate.aspirate = 8 # in uL/s
    # Dispense has the default flowrate of 300 ul/s
    # p10.flow_rate.dispense = 8

    # 384-well depth is 11.56 mm and max volume is 50 uL
    # 20 uL is 2 mm high in Biorad #HSP3841,
    # tandem (middle) wall is 5.1 mm high
    p10.well_bottom_clearance.dispense = 1
    p50.well_bottom_clearance.dispense = 3.5

    # Specify source wells
    reagents = ["1", "2"] # columns on reagent plate for substrate and enzyme


    cols_10uL = list(range(5, 8)) # destination wells in reaction plate (Bio-Rad hardshell 384-well)
    wells_reaction = ['A' + str(i) for i in cols_reaction]

    cols_18uL = list(range(9, 14)) # destination wells in reaction plate (Bio-Rad hardshell 384-well)
    wells_reaction = ['A' + str(i) for i in cols_reaction]

    #######################################################################################################################################
    ## PROCEDURE

    cols_8uL = list(range(1, 4)) # destination wells in reaction plate (Bio-Rad hardshell 384-well)
    wells_reaction = ['A' + str(i) for i in cols_reaction]
    # Distribute fluorescent dye
    p50.distribute(8, reagent_plate.columns_by_name()[reagents[1]], [reaction_plate.wells_by_name()[i] for i in wells_reaction],
    disposal_volume = 1, blow_out = True, new_tip = 'once')
