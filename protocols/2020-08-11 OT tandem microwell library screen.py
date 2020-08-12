# This protocol serves the preparation of a Cystathionine-B-synthase (CBS) activity assay in a microwell plate from Corning (3701).
# The 384-well microplate was customized by CNC machine milling (Leo) to form a tandem of two vertically adjacent wells.
# Objective: screen small library of compounds

from opentrons import protocol_api

metadata = {'apiLevel': '2.5'}

def run(protocol: protocol_api.ProtocolContext):
    #######################################################################################################################################
    ## SETUP
    
    # Load Labware
    temp_mod = protocol.load_module('Temperature Module', '9')
    reaction_plate = temp_mod.load_labware("corning_384_wellplate_112ul_flat", label = "reaction plate") # where the magic happens
    # tube_rack = protocol.load_labware("opentrons_96_aluminumblock_generic_pcr_strip_200ul", "6", label = "aluminum block") # CBS and substrate stocks
    sample_plate = protocol.load_labware("greiner_96_wellplate_323ul", "6", label = "sample plate") # CBS and substrate stocks
    reservoir_plate = protocol.load_labware("usascientific_12_reservoir_22ml", "8", label = 'reservoir plate') # DTNB detection reagent
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
    p50.well_bottom_clearance.dispense = 3.5

    # Specify target wells
    cols_compounds = [6, 7, 8, 9, 10]
    cols_noSAM = [9, 10, 11, 12, 13]
    cols_SAM = [14, 15, 16, 17, 18]
    wells_reaction_noSAM = ['A' + str(i) for i in cols_noSAM]
    wells_reaction_SAM = ['A' + str(i) for i in cols_SAM]
    wells_reaction = ['A' + str(i) for i in (cols_noSAM + cols_SAM)]
    wells_detection = ['B' + str(i) for i in (cols_noSAM + cols_SAM)]
    
    #######################################################################################################################################
    ## PROCEDURE

    # Transfer 20uL detection reagent from reservoir to reaction plate
    p50.distribute(20, reservoir_plate.columns_by_name()["1"], [reaction_plate.wells_by_name()[i] for i in wells_detection])

    # Distribute 2uL compound from 96-well library plate onto odd rows
    p10.distribute(2, library_plate.columns_by_name()["6"], [reaction_plate.wells_by_name()[i] for i in ["A9", "A14"]], new_tip = 'once', touch_tip = True) # each compound is tested w/ and w/o SAM (30 uM)
    p10.distribute(2, library_plate.columns_by_name()["7"], [reaction_plate.wells_by_name()[i] for i in ["A10", "A15"]], new_tip = 'once', touch_tip = True)
    p10.distribute(2, library_plate.columns_by_name()["8"], [reaction_plate.wells_by_name()[i] for i in ["A11", "A16"]], new_tip = 'once', touch_tip = True)
    p10.distribute(2, library_plate.columns_by_name()["9"], [reaction_plate.wells_by_name()[i] for i in ["A12", "A17"]], new_tip = 'once', touch_tip = True)
    p10.distribute(2, library_plate.columns_by_name()["10"], [reaction_plate.wells_by_name()[i] for i in ["A13", "A18"]], new_tip = 'once', touch_tip = True)

    # Distribute 10uL protein onto odd rows
    p50.distribute(10, sample_plate.columns_by_name()["4"], [reaction_plate.wells_by_name()[i] for i in wells_reaction], new_tip = 'once', touch_tip = True)
    
    # Transfer 8 uL reaction mix to reaction plate
    p50.distribute(8, sample_plate.columns_by_name()["5"], [reaction_plate.wells_by_name()[i] for i in wells_reaction_noSAM], touch_tip = True) # no SAM
    p50.distribute(8, sample_plate.columns_by_name()["6"], [reaction_plate.wells_by_name()[i] for i in wells_reaction_SAM], touch_tip = True) # SAM (30uM)


# SAMPLE CODE
# p20.transfer(20,reservoir_plate.wells_by_name()["A1"],mix_plate.wells_by_name()["A1"])
# p20.distribute(10,reservoir_plate.wells_by_name()["A2"],[mix_plate.wells_by_name()[well_name] for well_name in ["B1","C1","E1","G1","H1"]])
# p20.pick_up_tip()
# p20.transfer(10,mix_plate.wells_by_name()["A1"],mix_plate.wells_by_name()["B1"],mix_after=(3,10),new_tip="never")
# p20.transfer(10,mix_plate.wells_by_name()["B1"],mix_plate.wells_by_name()["C1"],mix_after=(3,10),new_tip="never")
# p20.transfer(10,mix_plate.wells_by_name()["C1"],mix_plate.wells_by_name()["D1"],mix_after=(3,10),new_tip="never")
# p20.transfer(10,mix_plate.wells_by_name()["D1"],mix_plate.wells_by_name()["E1"],mix_after=(3,10),new_tip="never")
# p20.drop_tip()
# p20.transfer(20,reservoir_plate.wells_by_name()["A3"],mix_plate.wells_by_name()["F1"])
# p20.pick_up_tip()
# p20.transfer(10,mix_plate.wells_by_name()["F1"],mix_plate.wells_by_name()["G1"],mix_after=(3,10),new_tip="never")
# p20.transfer(10,mix_plate.wells_by_name()["G1"],mix_plate.wells_by_name()["H1"],mix_after=(3,10),new_tip="never")
# p20.drop_tip()

# p10.transfer(4,mix_plate.wells_by_name()["A1"],mix_plate.wells_by_name()["A2"])
# p20.transfer(36,reservoir_plate.wells_by_name()["A4"],mix_plate.columns_by_name()["2"],new_tip='always')
# p10.well_bottom_clearance.dispense = 1
# rows=["A","B","C","D","E","F","G","H"]
# reaction_row_dest = "B"
# p10.transfer(10,mix_plate.columns_by_name()["2"],[reaction_plate.wells_by_name()[well_name] for well_name in ["B2","B3","B4"]])
# # for row in rows:
# # 	p20.distribute(10,mix_plate.wells_by_name()[(row+"2")],[reaction_plate.wells_by_name()[well_name] for well_name in [chr(ord(row)+1)+"2",chr(ord(row)+1)+"3",chr(ord(row)+1)+"4"]])
# p20.transfer(10,reservoir_plate.wells_by_name()["A4"],[reaction_plate.wells_by_name()[well_name] for well_name in ["J2","J3","J4"]])