# opentrons robot pipeting protocol
# 2020-12-03
# by Dalibor Nakladal
# objective: screen compound library in CBS activity assay

# Notes: do not use touch tip, this guarantees losing tips

###############################
# DON'T FORGET TO DO A DRY RUN
###############################

from opentrons import protocol_api

metadata = {'apiLevel': '2.5'}

def run(protocol: protocol_api.ProtocolContext):
    #######################################################################################################################################
    ## SETUP
    #######################################################################################################################################
    
    # Load Labware
    temp_mod = protocol.load_module('Temperature Module', '9')
    reaction_plate = temp_mod.load_labware("biorad_384_wellplate_50ul", label = "reaction plate") # where the magic happens
    reagent_plate = protocol.load_labware("greiner_96_wellplate_323ul", "6", label = "reagents")
    
    # Specify tip racks
    tiprack1 = protocol.load_labware("opentrons_96_tiprack_10ul", '8')
    tiprack2 = protocol.load_labware("opentrons_96_tiprack_300ul", '5')

    # Load pipettes and set parameters
    p10 = protocol.load_instrument("p10_multi", "right", tip_racks = [tiprack1])
    p50 = protocol.load_instrument('p50_multi', "left", tip_racks = [tiprack2])

    p10.flow_rate.aspirate = 8
    p10.flow_rate.dispense = 8

    # 384-well depth is 11.56 mm and max volume is 50 uL
    # 20 uL is 2 mm high, tandem (middle) wall is 5.1 mm high
    p10.well_bottom_clearance.dispense = 1.5

    # Specify target wells
    # 1 = substrate CON
    # 2 = substrate CON
    # 3 = substrate SAM
    # 4 = substrate SAM
    # 5 = enzyme
    # 6 = enzyme
    reagents = ["1", "2", "3", "4", "5", "6"] # columns on reagent plate for substrate and enzyme

    # reaction
    cols_reaction = list(range(1, 24)) # destination wells in reaction plate (Bio-Rad hardshell 384-well)
    wells_reaction_CON = ['A' + str(i) for i in cols_reaction]
    wells_reaction_SAM = ['B' + str(i) for i in cols_reaction]
    
    #######################################################################################################################################
    ## PROCEDURE
    #######################################################################################################################################

    ####### FIRST PLATE HALF #######
    t_vol = 84
    t_mix = 40

    ### reactions CON
    p50.pick_up_tip()
    # mix substrate and enzyme
    p50.transfer(t_vol, reagent_plate.columns_by_name()[reagents[4]], reagent_plate.columns_by_name()[reagents[0]],
    mix_after = (3, t_mix), new_tip = 'never')

    # Distribute substrate mixed with fluorescent dye and enzyme
    p50.distribute(20, reagent_plate.columns_by_name()[reagents[0]], [reaction_plate.wells_by_name()[i] for i in wells_reaction_CON[0:12]],
    disposal_volume = 1, blow_out = True, new_tip = 'never')
    p50.drop_tip()

    ### reactions SAM 
    p50.pick_up_tip()
    # mix substrate and enzyme
    p50.transfer(t_vol, reagent_plate.columns_by_name()[reagents[4]], reagent_plate.columns_by_name()[reagents[2]],
    mix_after = (3, t_mix), new_tip = 'never')

    # Distribute substrate mixed with fluorescent dye and enzyme
    p50.distribute(20, reagent_plate.columns_by_name()[reagents[2]], [reaction_plate.wells_by_name()[i] for i in wells_reaction_SAM[0:12]],
    disposal_volume = 1, blow_out = True, new_tip = 'never')
    p50.drop_tip()

    ####### SECOND PLATE HALF #######

    ### reactions CON
    p50.pick_up_tip()
    # mix substrate and enzyme
    p50.transfer(t_vol, reagent_plate.columns_by_name()[reagents[5]], reagent_plate.columns_by_name()[reagents[1]],
    mix_after = (3, t_mix), new_tip = 'never')

    # Distribute substrate mixed with fluorescent dye and enzyme
    p50.distribute(20, reagent_plate.columns_by_name()[reagents[1]], [reaction_plate.wells_by_name()[i] for i in wells_reaction_CON[12:25]],
    disposal_volume = 1, blow_out = True, new_tip = 'never')
    p50.drop_tip()

    ### reactions SAM
    p50.pick_up_tip()
    # mix substrate and enzyme
    p50.transfer(t_vol, reagent_plate.columns_by_name()[reagents[5]], reagent_plate.columns_by_name()[reagents[3]],
    mix_after = (3, t_mix), new_tip = 'never')

    # Distribute substrate mixed with fluorescent dye and enzyme
    p50.distribute(20, reagent_plate.columns_by_name()[reagents[3]], [reaction_plate.wells_by_name()[i] for i in wells_reaction_SAM[12:25]],
    disposal_volume = 1, blow_out = True, new_tip = 'never')
    p50.drop_tip()