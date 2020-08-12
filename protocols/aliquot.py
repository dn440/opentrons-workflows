from opentrons import protocol_api
# import pandas as pd

metadata = {'apiLevel': '2.2'}


def run(protocol: protocol_api.ProtocolContext):
	temp_mod = protocol.load_module('Temperature Module', '6')
	tubes = temp_mod.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul',
										label='aliquot tubes')
	protein_tubes = protocol.load_labware("opentrons_24_aluminumblock_nest_2ml_snapcap",'5')
	tiprack1 = protocol.load_labware("opentrons_96_tiprack_300ul",'4')
	#tiprack2 = protocol.load_labware("opentrons_96_tiprack_10ul",'2')
	#tiprack3 = protocol.load_labware("opentrons_96_tiprack_300ul",'4')
	
	p50 = protocol.load_instrument('p50_multi',"left",tip_racks=[tiprack1])
	
	
	# p50.transfer(50, [condition_block.wells_by_name()[well_name].bottom(30) for well_name in source],[cryst_plate.wells_by_name()[well_name] for well_name in res_destination], new_tip ='always')
	# p20.transfer(1, [cryst_plate.wells_by_name()[well_name].bottom(5) for well_name in res_destination],[cryst_plate.wells_by_name()[well_name].bottom(0.5) for well_name in well_one_destination], new_tip ='always')
	p50.pick_up_tip()
	for x in range(0,12):

		p50.transfer(40,protein_tubes.wells_by_name()["A1"],tubes.columns()[x],new_tip='never',mix_before=(5,50))
	p50.drop_tip()
	# p300.transfer(50,condition_block.wells_by_name()["H12"],tubes.columns()[1])
	# p300.transfer(50,condition_block.wells_by_name()["H11"],tubes.columns()[10])
	# p300.transfer(50,condition_block.wells_by_name()["H11"],tubes.columns()[11])

