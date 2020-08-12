from opentrons import protocol_api

metadata = {'apiLevel': '2.1'}
def run(protocol: protocol_api.ProtocolContext):
	tiprack1 = protocol.load_labware("opentrons_96_tiprack_20ul",'1')
	p20 = protocol.load_instrument('p20_single_gen2',"right",tip_racks=[tiprack1])
	p20.pick_up_tip()
	p20.drop_tip()