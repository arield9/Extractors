import requests
import json

BOT_TOKEN = "8900836460:AAFt5FK2VixHzJIB1WF_83RtmN4O8RKIRao"
CHAT_ID = "7111838470"
START_MESSAGE_ID = 1
MAX_MESSAGE_ID = 100      # Upper bound to scan up to
MAX_CONSECUTIVE_FAILS = 20  # How many misses in a row before stopping


def get_messages():
    all_messages = []
    consecutive_fails = 0

    for message_id in range(START_MESSAGE_ID, MAX_MESSAGE_ID + 1):
        URL = f"https://api.telegram.org/bot{BOT_TOKEN}/forwardMessage"
        payload = {
            "chat_id": CHAT_ID,
            "from_chat_id": CHAT_ID,
            "message_id": message_id
        }

        response = requests.post(URL, json=payload)
        data = response.json()

        if response.status_code == 200 and data.get("ok"):
            print(f"✅ Found message ID {message_id}")
            all_messages.append(data["result"])
            consecutive_fails = 0  # Reset the fail counter on success
        else:
            error_desc = data.get("description", "Unknown error")
            print(f"⏭️  Skipping message ID {message_id}: {error_desc}")
            consecutive_fails += 1

            # Only stop if we've had a long unbroken streak of failures
            if consecutive_fails >= MAX_CONSECUTIVE_FAILS:
                print(f"\n🛑 {MAX_CONSECUTIVE_FAILS} consecutive failures — assuming end of messages.")
                break

    # Save to text file
    output_path = "<txt file path>"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(all_messages, indent=4, ensure_ascii=False))

    print(f"\n✅ Done! Retrieved {len(all_messages)} messages.")
    print(f"📄 Results saved to: {output_path}")
    return all_messages


get_messages()