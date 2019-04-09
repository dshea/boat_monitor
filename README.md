# boat_monitor
Raspberry pi and website code to monitor Nightshade's bilge pumps and batteries

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
    - humidity - (flaot) precent relative humidity

