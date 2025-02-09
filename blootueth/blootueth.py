#!/usr/bin/python3
# blootueth.py - jk4ln
# v1.0

import asyncio
import argparse
from bleak import BleakScanner, BleakClient

async def list_characteristics_and_write(device_address, write_enabled):
    timeout = 15 #  adjust timeout as needed
    async with BleakClient(device_address, timeout=timeout) as client:
        services = client.services

        characteristics_list = []

        for service in services:
            print(f"Service UUID: {service.uuid}")
            for idx, characteristic in enumerate(service.characteristics, start=1):
                print(f"  {idx}. Characteristic UUID: {characteristic.uuid}")
                print(f"    Properties: {characteristic.properties}")
                print(f"    Handle: {characteristic.handle}")
                
                try:
                    value = await asyncio.wait_for(client.read_gatt_char(characteristic), timeout)
                    print(f"    Value: {value}")
                except asyncio.TimeoutError:
                    print("    Timeout error: Failed to read characteristic value within the specified time.")
                except Exception as e:
                    print(f"    Failed to read value: {e}")

                characteristics_list.append(characteristic)

        if write_enabled and characteristics_list:
            print("---")
            char_idx = int(input("\nEnter the number of the characteristic you want to write to: ")) - 1
            if 0 <= char_idx < len(characteristics_list):
                characteristic = characteristics_list[char_idx]
                value_to_write = input(f"Enter the value to write to {characteristic.uuid}: ")

                # convert the input value to bytes
                try:
                    value_bytes = value_to_write.encode('utf-8')  # adjust encoding as needed
                    await client.write_gatt_char(characteristic, value_bytes)
                    print(f"Successfully wrote value: {value_to_write} to {characteristic.uuid}")
                except Exception as e:
                    print(f"Failed to write value: {e}")
            else:
                print("Invalid choice.")

async def discover_devices():
    devices = await BleakScanner.discover()
    
    if not devices:
        print("No devices found.")
        return None
    
    print("Available devices:")
    for idx, device in enumerate(devices, start=1):
        print(f"{idx}. Device: {device.name}, Address: {device.address}")

    print("---")
    device_choice = input("Enter the number of the device you want to connect to: ")
    print("---") 
    try:
        device_idx = int(device_choice) - 1
        selected_device = devices[device_idx]
        print(f"Selected device: {selected_device.name} ({selected_device.address})")
        return selected_device.address
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid number.")
        return None

async def main():
    parser = argparse.ArgumentParser(description="Interact with Bluetooth devices using Bleak.")
    parser.add_argument('-w', '--write', action='store_true', help="Enable writing to characteristics")
    args = parser.parse_args()

    device_address = await discover_devices()
    if device_address:
        try:
            await list_characteristics_and_write(device_address, args.write)
        except:
            print("Connection Error.")

asyncio.run(main())
