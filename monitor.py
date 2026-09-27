import requests

PART_NUMBER = "MJX74VC/A"
LOCATION = "Kitchener, ON"

url = "https://www.apple.com/ca/shop/retail/pickup-message"

params = {
    "parts.0": PART_NUMBER,
    "location": LOCATION,
}

response = requests.get(url, params=params, timeout=15)
response.raise_for_status()

data = response.json()

available_stores = []

for store in data["body"]["stores"]:
    availability = store["partsAvailability"].get(PART_NUMBER, {})

    status = availability.get("pickupDisplay", "unknown")

    print(
        f'{store["storeName"]} '
        f'({store["city"]}, {store["state"]}) '
        f'[{store["storeNumber"]}]: {status}'
    )

    if status == "available":
        available_stores.append(
            f'{store["storeName"]} ({store["city"]}, {store["state"]})'
        )

print()

if available_stores:
    print("🚨 iPhone AVAILABLE!")

    for store in available_stores:
        print(f"  - {store}")
else:
    print("No availability found.")
