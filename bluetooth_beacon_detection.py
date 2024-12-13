import asyncio
from bleak import BleakScanner

async def discover_devices_with_rssi():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    if devices:
        print(f"Found {len(devices)} device(s):")
        for device in devices:
            print(f"  Name: {device.name or 'Unknown'}")
            print(f"  Address: {device.address}")
            print(f"  RSSI: {device.rssi} dBm\n")
    else:
        print("No BLE devices found.")

if __name__ == "__main__":
    asyncio.run(discover_devices_with_rssi())
