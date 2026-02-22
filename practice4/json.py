import json
import os
print(os.getcwd())

with open("sample-data.json") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':7} {'MTU':5}")
print("-" * 80)

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]

    dn = attributes.get("dn", "")
    descr = attributes.get("descr", "")
    speed = attributes.get("speed", "")
    mtu = attributes.get("mtu", "")

    print(f"{dn:50} {descr:20} {speed:7} {mtu:5}")