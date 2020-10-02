# The problem:
# long 300uL tips are hardly suitable for small-necked 384-wells. We were using them because they were convenient to distribute 5uL volumes
# into several columns after a single aspiration using the p50 pipette. However we ran into problems with dimensional accuracy, often the tip
# would hit the edge of the well neck and bend or completely miss. We solved part of the problem by moving the target 384-well plate from the
# temperature module onto the metal base plate of the robot, which has metal clips that fix it in place.
# Still, the volumes were inconsistently dispensed into the wells due the necessary high dispense height and due to adhesion forces, i.e.
# the liquid would sometimes stay inside the well but sometimes stay attached to the tip or the neck of the well. This also introduced potential
# carryover of compounds into the next wells. The solution will be to only use the p10 pipette and reduce volumes. Perhaps a reaction volume of
# 15uL instead of 25uL will still work well and be more economical.

# Therefore this protocol serves the optimization of pipetting accuracy and liquid adhesion of small volumes into a 384-well plate.
# Methylene blue can be used to make visual examination easier.

# Notes: do not use touch tip, this guarantees losing tips

from opentrons import protocol_api

metadata = {'apiLevel': '2.5'}

def run(protocol: protocol_api.ProtocolContext):
    #######################################################################################################################################
    ## SETUP
    
    # Load Labware
    temp_mod = protocol.load_module('Temperature Module', '9')
    reaction_plate = protocol.load_labware("biorad_384_wellplate_50ul", "8", label = "reaction plate") # where the magic happens
    # tube_rack = protocol.load_labware("opentrons_96_aluminumblock_generic_pcr_strip_200ul", "6", label = "aluminum block") # CBS and substrate stocks
    sample_plate = protocol.load_labware("greiner_96_wellplate_323ul", "6", label = "sample plate") # CBS and dye stocks (!!! protect dye from light !!!)
    library_plate = protocol.load_labware("greiner_96_wellplate_323ul", "5", label = "library plate") # compound library
    
    # Specify tip racks
    tiprack1 = protocol.load_labware("opentrons_96_tiprack_10ul", '2')
    tiprack2 = protocol.load_labware("opentrons_96_tiprack_300ul", '3')

    # Load pipettes and set parameters
    p10 = protocol.load_instrument("p10_multi", "right", tip_racks = [tiprack1])
    p50 = protocol.load_instrument('p50_multi', "left", tip_racks = [tiprack2])

    p10.flow_rate.aspirate = 8
    p10.flow_rate.dispense = 8
    # 384-well depth is 11.56 mm and max volume is 112 uL
    # 20 uL is 2 mm high, tandem (middle) wall is 5.1 mm high
    p10.well_bottom_clearance.dispense = 1
    p50.well_bottom_clearance.dispense = 7

    # Specify target wells (ONLY NEED TO EDIT WELLS HERE)
    samples = ["5", "6"] # columns on sample plate with protein and dye
    cols_compounds = [6, 7, 8, 9, 10] # library columns to aspirate compounds from
    cols_woSAM = [1, 2, 3, 4, 5] # destination wells in reaction plate (384-tandem)
    cols_wSAM = [6, 7, 8, 9, 10] # destination wells in reaction plate (384-tandem) (30 uM SAM final c)
    wells_reaction_woSAM = ['A' + str(i) for i in cols_woSAM]
    wells_reaction_wSAM = ['A' + str(i) for i in cols_wSAM]
    wells_reaction = ['A' + str(i) for i in (cols_woSAM + cols_wSAM)]
    
    #######################################################################################################################################
    ## PROCEDURE

    # Distribute fluorescent dye from sample plate to reaction plate
    # p10.distribute(5, sample_plate.columns_by_name()[samples[2]], [reaction_plate.wells_by_name()[i] for i in wells_reaction],
    # disposal_volume = 0, blow_out = False, touch_tip = True)

    # Distribute protein mixed with fluorescent dye
    p10.distribute(13.5, sample_plate.columns_by_name()[samples[0]], [reaction_plate.wells_by_name()[i] for i in wells_reaction_woSAM],
    disposal_volume = 0, blow_out = False, new_tip = 'once')
    p10.distribute(13.5, sample_plate.columns_by_name()[samples[1]], [reaction_plate.wells_by_name()[i] for i in wells_reaction_wSAM],
    disposal_volume = 0, blow_out = False, new_tip = 'once')
    #p10.distribute(13.5, sample_plate.columns_by_name()[samples[1]], [reaction_plate.wells_by_name()[i] for i in wells_reaction_wSAM],
    #disposal_volume = 0, blow_out = False, new_tip = 'once', touch_tip = True)
    
    # Distribute compounds from 96-well library plate and mix
    vol = 1.5
    for i in range(0, len(cols_compounds)):
        p10.transfer(vol, library_plate.columns_by_name()[str(cols_compounds[i])], reaction_plate.wells_by_name()[wells_reaction_woSAM[i]], mix_after = (3, vol))
        p10.transfer(vol, library_plate.columns_by_name()[str(cols_compounds[i])], reaction_plate.wells_by_name()[wells_reaction_wSAM[i]], mix_after = (3, vol))

    # for i in range(0, len(cols_compounds)): # iterate through every column on the compound plate
    #     lib_col = str(cols_compounds[i]) # column of the library plate (single number)
    #     wells_target = [wells_reaction_woSAM[i], wells_reaction_wSAM[i]] # wells to distribute to (each compound is tested w/ and w/o SAM, so two apart columns)
    #     p10.distribute(1.5, library_plate.columns_by_name()[lib_col], [reaction_plate.wells_by_name()[j] for j in wells_target],
    #     new_tip = 'always', mix_after = (3, 1.5))