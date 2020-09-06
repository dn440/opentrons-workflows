# This protocol serves the preparation of a Cystathionine-B-synthase (CBS) activity assay in a microwell plate from Corning (3701).
# The 384-well microplate was customized by CNC machine milling (Leo) to form a tandem of two vertically adjacent wells.
# Objective: screen small library of compounds. Previously, compounds were used at 30uM concentration, this time we use 300uM

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

    # Specify target wells (ONLY NEED TO EDIT WELLS HERE)
    cols_compounds = [1, 2, 3, 4, 5] # library columns to aspirate compounds from
    cols_woSAM = [13, 14, 15, 16, 17] # destination wells in reaction plate (384-tandem)
    cols_wSAM = [18, 19, 20, 21, 22] # destination wells in reaction plate (384-tandem) (30 uM SAM final c)
    wells_reaction_woSAM = ['A' + str(i) for i in cols_woSAM]
    wells_reaction_wSAM = ['A' + str(i) for i in cols_wSAM]
    wells_reaction = ['A' + str(i) for i in (cols_woSAM + cols_wSAM)]
    wells_detection = ['B' + str(i) for i in (cols_woSAM + cols_wSAM)]
    samples = ["10", "11", "12"] # columns on sample plate with protein, substrate wo/SAM, substrate w/SAM
    
    #######################################################################################################################################
    ## PROCEDURE

    # CBS REACTION
    # Transfer 20uL detection reagent from reservoir to reaction plate onto even rows
    p50.distribute(20, reservoir_plate.columns_by_name()["1"], [reaction_plate.wells_by_name()[i] for i in wells_detection])

    # Distribute 2uL compound from 96-well library plate onto odd rows
    for i in range(0, len(cols_compounds)): # iterate through every column on the compound plate
        lib_col = str(cols_compounds[i]) # column of the library plate (single number)
        wells_target = [wells_reaction_woSAM[i], wells_reaction_wSAM[i]] # wells to distribute to (each compound is tested w/ and w/o SAM, so two apart columns)
        p10.distribute(2, library_plate.columns_by_name()[lib_col], [reaction_plate.wells_by_name()[j] for j in wells_target], new_tip = 'once')

    # Distribute 10uL protein onto odd rows
    p50.distribute(10, sample_plate.columns_by_name()[samples[0]], [reaction_plate.wells_by_name()[i] for i in wells_reaction], new_tip = 'once')
    
    # Transfer 8 uL reaction mix to reaction plate
    p50.distribute(8, sample_plate.columns_by_name()[samples[1]], [reaction_plate.wells_by_name()[i] for i in wells_reaction_woSAM], new_tip = 'once') # w/o SAM
    p50.distribute(8, sample_plate.columns_by_name()[samples[2]], [reaction_plate.wells_by_name()[i] for i in wells_reaction_wSAM], new_tip = 'once') # w/ SAM (30uM)


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