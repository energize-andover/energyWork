# Copyright 2018 BACnet Gateway.  All rights reserved.

try:
    import argparse
    import pandas as pd
    import datetime
    from energyWork.py.bacnet_gateway_requests import get_value_and_units

    # Get hostname and port of BACnet Gateway
    parser = argparse.ArgumentParser( description='Test BACnet Gateway', add_help=False )
    parser.add_argument( '-h', dest='hostname' )
    parser.add_argument( '-p', dest='port' )
    args = parser.parse_args()

    temp_file = open("../csv/temp.csv", "w")
    co2_file = open("../csv/co2.csv", "w")

    # Read spreadsheet into a dataframe.
    # Each row contains the following:
    #   - Location
    #   - Instance ID of CO2 sensor
    #   - Instance ID of temperature sensor
    df = pd.read_csv( '../csv/ahs_air.csv', na_filter=False, comment='#')

    # Output column headings
    print('{0},{1},{2},{3},{4},'.format('"Date / Time"', '"Units"', '"Facility"', '"UID"', '"Value"'))

    co2_file.write('{0},{1},{2},{3},{4},'.format('"Date / Time"', '"Units"',
                                             '"Facility"', '"UID"', '"Value"'))
    temp_file.write('{0},{1},{2},{3},{4},'.format('"Date / Time"', '"Units"',
                                              '"Facility"', '"UID"', '"Value"'))

    # Iterate over the rows of the dataframe, getting temperature and CO2 values for each location
    for index, row in df.iterrows():

        # Retrieve data
        temp_value, temp_units = get_value_and_units( row['Facility'], row['Temperature'], args.hostname, args.port )
        co2_value, co2_units = get_value_and_units( row['Facility'], row['CO2'], args.hostname, args.port )

        # Prepare to print
        temp_value = int( temp_value ) if temp_value else ''
        temp_units = temp_units if temp_units else ''
        co2_value = int( co2_value ) if co2_value else ''
        co2_units = co2_units if co2_units else ''

        # Output CSV format
        # Output CO2 CSV file
        co2_file.write("\n")
        print('CO2 Levels - {0},{1},{2},{3},{4}'.format(datetime.datetime.utcnow(), co2_units, row['Facility'],
                                                    row['Label'], co2_value))
        co2_file.write('{0},{1},{2},{3},{4}'.format(datetime.datetime.utcnow(), co2_units, row['Facility'],
                                                row['Label'], co2_value))

        # Output Temp CSV file
        temp_file.write("\n")
        print('Temperature - {0},{1},{2},{3},{4},'.format(datetime.datetime.utcnow(), temp_units,
                                       row['Facility'], row['Label'], temp_value))
        temp_file.write('{0},{1},{2},{3},{4},'.format(datetime.datetime.utcnow(), temp_units,
                                                row['Facility'], row['Label'], temp_value))

except KeyboardInterrupt:
    co2_file.close()
    temp_file.close()
    print( 'Bye' )
    import sys
    sys.exit()
