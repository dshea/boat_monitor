# boat_monitor
Raspberry pi and website code to monitor Nightshade's bilge pumps and batteries


raspberry pi
    - upload jason file 4x? a day
        - read database and create json file
        - each upload requires turning on the network
	- use ftp to transfer file
    - file name = 2019-03-28T15:53:00.json

web php
    - find json files, load them into database, move them to a sub-dir
    - create graph from database
    - display graph in browser



database fields

pump
    - time - (int) unixtime pump turned on
    - name - (str) pump name
    - duration - (int) # seconds pump was on

battery
    - time - (int) unixtime reading was taken
    - battery1 - (float) battery bank 1, house bank
    - battery2 - (float) battery bank 2, starting battery
    - temp - (float) temp in fahrenheit
    - humidity - (float) precent relative humidity

