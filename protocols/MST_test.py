from opentrons import protocol_api

metadata = {'apiLevel': '2.1'}

locations =  ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',
              'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12',
              'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12',
              'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12',
              'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',
              'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
              'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12',
              'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12']

### Change location and settings here
final_vol = 20
dilution_factor = 2
num_dilutions = 16
compound_stock_location = "H12"
buffer_location = "H11"
protein_location = "H10"
liquid_trash_tube = "H9"
starting_location = "A1"

## Calculation of appropriate volumes
trans_vol = final_vol / dilution_factor
buffer_vol = final_vol - trans_vol

## Determination with tubes/wells will be used for dilution
buffer_wells = []
current_row = starting_location[0]
current_column = int(starting_location[1])
for x in range(current_column,num_dilutions):
    current_column += 1
    if current_column > 12:
        current_row = chr(ord(current_row)+1)
        current_column = 1
    buffer_wells.append(current_row + str(current_column))
protein_wells = buffer_wells
protein_wells.insert(0,starting_location)


### Protocol 
        
def run(protocol: protocol_api.ProtocolContext):
    #labware
    temp_mod = protocol.load_module('Temperature Module', '9')
    plate = temp_mod.load_labware("opentrons_96_aluminumblock_generic_pcr_strip_200ul",
                                  label='Temp-controlled pcr tubes')
    #tiprack
    tiprack1 = protocol.load_labware("opentrons_96_tiprack_20ul","1")
    #pipettes
    p20 = protocol.load_instrument("p20_single_gen2","right",tip_racks=[tiprack1])
    
    # Move compound stock to start of series
    p20.transfer(final_vol,plate.wells_by_name()[compound_stock_location],plate.wells_by_name()[starting_location])
    # Put buffer in each tube
    p20.transfer(buffer_vol, plate.wells_by_name()[buffer_location],[plate.wells_by_name()[well_name] for well_name in buffer_wells[1:]])
    # Perform serial dilution
    p20.pick_up_tip()
    p20.transfer(trans_vol,plate.wells_by_name()[starting_location],plate.wells_by_name()[buffer_wells[0]],mix_after=(3,final_vol/2),new_tip='never')
    for num,well in enumerate(buffer_wells[:-1]):
        source = well
        destination = buffer_wells[num+1]
        p20.transfer(trans_vol,plate.wells_by_name()[source],plate.wells_by_name()[destination], mix_after=(3,final_vol/2),new_tip='never')
    # Discard excess from last tube
    p20.transfer(buffer_vol, plate.wells_by_name()[buffer_wells[-1]],plate.wells_by_name()[liquid_trash_tube],new_tip='never')
    p20.drop_tip()
    #add protein to all tubes
    p20.transfer(buffer_vol, plate.wells_by_name()[protein_location],[plate.wells_by_name()[well_name] for well_name in protein_wells],mix_after=(3,final_vol/2),new_tip='always')
    
    
