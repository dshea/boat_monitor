#! /usr/bin/env python3

import asyncio
from bleak import BleakScanner, BleakClient
from bleak.uuids import normalize_uuid_16

programDone = False

deviceName = "L-12100BNN100-A03977"
serviceId = 0xffe0
txCharId = 0xffe1
rxCharId = 0xffe2

voltage0Index = 8
voltageIndex = 12
cellVoltageIndex = 16
currentIndex = 48
cellTempIndex = 52
bmsTempIndex = 54
remainingAhIndex = 62
capacityAhIndex = 64

async def callback_handler(_, data):
    global programDone

    i = 0
    for d in data:
        print(i, d)
        i += 1

    # print("len =", len(data))
    # print(data)
    # print("date[52] =", data[52])
    # print("date[53] =", data[53])

    # print("data =", data[52:54])
    # temp = int.from_bytes(data[52:54],'little')
    # print("temp C =", temp)
    # print("temp F =", temp * 9.0 / 5.0 + 32.0)

    i = voltage0Index
    voltage0 = int.from_bytes(data[i:i+4],'little', signed=False) / 1000.0
    print("voltage0 =", voltage0)

    i = voltageIndex
    voltage = int.from_bytes(data[i:i+4],'little', signed=False) / 1000.0
    print("voltage =", voltage)

    i = cellVoltageIndex
    for j in range(16):
        cellVoltage = int.from_bytes(data[i:i+2],'little', signed=False) / 1000.0
        if cellVoltage != 0:
            print("cell voltage", j, "=", cellVoltage)
        i += 2

    i = currentIndex
    current = int.from_bytes(data[i:i+4],'little', signed=True) / 1000.0
    print("current =", current)

    i = cellTempIndex
    cellTemp = int.from_bytes(data[i:i+2],'little', signed=True)
    print("cellTemp =", cellTemp)

    i = bmsTempIndex
    bmsTemp = int.from_bytes(data[i:i+2],'little', signed=True)
    print("bmsTemp =", bmsTemp)

    i = remainingAhIndex
    remainingAh = int.from_bytes(data[i:i+2],'little', signed=False) / 100.0
    print("remainingAh =", remainingAh)

    i = capacityAhIndex
    capacityAh = int.from_bytes(data[i:i+2],'little', signed=False) / 100.0
    print("capacityAh =", capacityAh)

    print("charge level =", remainingAh / capacityAh * 100.0, "%")

    programDone = True

async def checkDone():
    global programDone

    if not programDone:
       await asyncio.sleep(1.0)

async def main():
    device = await BleakScanner.find_device_by_name(deviceName)
    # print(device)
    # print(dir(device))
    # print()

    async with BleakClient(device) as client:
        # print("connected")
        # print("services")
        # for service in client.services:
        #     print("    ", service)
        #     print("    characteristics")
        #     for characteristic in service.characteristics:
        #         print("        ", characteristic)
        #         print("        descriptors")
        #         for descriptor in characteristic.descriptors:
        #             print("            ", descriptor)
        #         print("        properties")
        #         for property in characteristic.properties:
        #             print("            ", property)




        # print("\n\n")
        service = client.services.get_service(normalize_uuid_16(serviceId))
        # print(service)
        rxCharacteristic = service.get_characteristic(normalize_uuid_16(rxCharId))
        # print("    ", rxCharacteristic)
        # print("    descriptors")
        # for descriptor in rxCharacteristic.descriptors:
        #     print("        ", descriptor)
        # print("    properties")
        # for property in rxCharacteristic.properties:
        #     print("        ", property)

        txCharacteristic = service.get_characteristic(normalize_uuid_16(txCharId))
        # print("    ", txCharacteristic)
        # print("    descriptors")
        # for descriptor in txCharacteristic.descriptors:
        #     print("        ", descriptor)
        # print("    properties")
        # for property in txCharacteristic.properties:
        #     print("        ", property)

        await client.start_notify(txCharacteristic, callback_handler)
        buffer = bytes.fromhex('0000 0401 1355 AA17')
        await client.write_gatt_char(rxCharacteristic, buffer, response=False)
        await checkDone()
        await client.stop_notify(txCharacteristic)

    print("disconnected")

asyncio.run(main())
