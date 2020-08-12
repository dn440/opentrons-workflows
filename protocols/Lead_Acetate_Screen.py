from opentrons import protocol_api

metadata = {'apiLevel': '2.5'}

def run(protocol: protocol_api.ProtocolContext):
    #Load Labware
    temp_mod = protocol.load_module('Temperature Module', '9')
    master_plate = temp_mod.load_labware('opentrons_24_aluminumblock_nest_1.5ml_snapcap',
                                        label='Master solutions')
    reaction_plate = protocol.load_labware("biorad_384_wellplate_50ul","10",label="reaction plate")
    mix_plate = protocol.load_labware("gbo_96_wellplate_323ul","11")

    tiprack1 = protocol.load_labware("opentrons_96_tiprack_20ul",'1')
    tiprack2 = protocol.load_labware("opentrons_96_tiprack_20ul",'2')
    tiprack3 = protocol.load_labware("opentrons_96_tiprack_20ul",'3')
#### A1 = liver lysate,  A2 = Water,  A3 = Cell lysate,  A4 = Master Mix
    ##Load pipettes
    p20 = protocol.load_instrument('p20_single_gen2',"right",tip_racks=[tiprack1])
    p10 = protocol.load_instrument("p10_multi","left",tip_racks=[tiprack2,tiprack3])
    p20.flow_rate.aspirate = 8
    p20.flow_rate.dispense = 8
#Transfer 20 uL liver lysate to A1 of mix plate and make serial dilution
    p20.transfer(20,master_plate.wells_by_name()["A1"],reaction_plate.wells_by_name()["B1"])





# p20.transfer(20,master_plate.wells_by_name()["A1"],mix_plate.wells_by_name()["A1"])
# p20.distribute(10,master_plate.wells_by_name()["A2"],[mix_plate.wells_by_name()[well_name] for well_name in ["B1","C1","E1","G1","H1"]])
# p20.pick_up_tip()
# p20.transfer(10,mix_plate.wells_by_name()["A1"],mix_plate.wells_by_name()["B1"],mix_after=(3,10),new_tip="never")
# p20.transfer(10,mix_plate.wells_by_name()["B1"],mix_plate.wells_by_name()["C1"],mix_after=(3,10),new_tip="never")
# p20.transfer(10,mix_plate.wells_by_name()["C1"],mix_plate.wells_by_name()["D1"],mix_after=(3,10),new_tip="never")
# p20.transfer(10,mix_plate.wells_by_name()["D1"],mix_plate.wells_by_name()["E1"],mix_after=(3,10),new_tip="never")
# p20.drop_tip()
# p20.transfer(20,master_plate.wells_by_name()["A3"],mix_plate.wells_by_name()["F1"])
# p20.pick_up_tip()
# p20.transfer(10,mix_plate.wells_by_name()["F1"],mix_plate.wells_by_name()["G1"],mix_after=(3,10),new_tip="never")
# p20.transfer(10,mix_plate.wells_by_name()["G1"],mix_plate.wells_by_name()["H1"],mix_after=(3,10),new_tip="never")
# p20.drop_tip()

# p10.transfer(4,mix_plate.wells_by_name()["A1"],mix_plate.wells_by_name()["A2"])
# p20.transfer(36,master_plate.wells_by_name()["A4"],mix_plate.columns_by_name()["2"],new_tip='always')
# p10.well_bottom_clearance.dispense = 1
# rows=["A","B","C","D","E","F","G","H"]
# reaction_row_dest = "B"
# p10.transfer(10,mix_plate.columns_by_name()["2"],[reaction_plate.wells_by_name()[well_name] for well_name in ["B2","B3","B4"]])
# # for row in rows:
# # 	p20.distribute(10,mix_plate.wells_by_name()[(row+"2")],[reaction_plate.wells_by_name()[well_name] for well_name in [chr(ord(row)+1)+"2",chr(ord(row)+1)+"3",chr(ord(row)+1)+"4"]])
# p20.transfer(10,master_plate.wells_by_name()["A4"],[reaction_plate.wells_by_name()[well_name] for well_name in ["J2","J3","J4"]])

