import os
import requests

PART_NUMBER = "MJX74VC/A"
LOCATION = "Kitchener, ON"

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

APPLE_URL = "https://www.apple.com/ca/shop/retail/pickup-message"

params = {
    "parts.0": PART_NUMBER,
    "location": LOCATION,
}

response = requests.get(
    APPLE_URL,
    params=params,
    timeout=15,
)
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
            f'{store["storeName"]} — '
            f'{store["city"]}, {store["state"]}'
        )

print()

if not available_stores:
    print("No availability found.")
    exit(0)

#if not available_stores:
#    print("No availability found.")
#
#    # TEMPORARY TELEGRAM TEST
#    available_stores = ["TEST STORE — Waterloo, ON"]

print("🚨 iPhone AVAILABLE!")

message = (
    "🚨 iPhone 18 Pro Max Burgundy 256GB AVAILABLE!\n\n"
    "Pickup locations:\n"
)

for store in available_stores:
    message += f"• {store}\n"

message += "\nCheck Apple Store pickup immediately."

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise RuntimeError("Telegram credentials are not configured.")

telegram_url = (
    f"https://api.telegram.org/bot"
    f"{TELEGRAM_BOT_TOKEN}/sendMessage"
)

telegram_response = requests.post(
    telegram_url,
    data={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    },
    timeout=15,
)

telegram_response.raise_for_status()

print("Telegram notification sent.")
