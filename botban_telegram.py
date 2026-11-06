#!/usr/bin/env python3
# Telegram interface for the original botban.py.
# Keeps botban.py unchanged and reuses its get_me, set_name and set_photo functions.
# Main interface token: BOTBAN_MANAGER_TOKEN (must be different from panel token).
# User target bot tokens are held in memory only and are never written to disk.

import os
import time
import tempfile
import requests
import botban

API = "https://api.telegram.org/bot{}"
FILE_API = "https://api.telegram.org/file/bot{}"
MANAGER_TOKEN = os.getenv("BOTBAN_MANAGER_TOKEN", "").strip()
POLL_TIMEOUT = 25

MENU = [
    ["🤖 Add Bot Token"],
    ["✏️ Change Name", "🖼️ Change Picture"],
    ["👤 My Session", "❌ Remove Token"],
    ["ℹ️ Help"],
]
BACK = [["⬅️ Back to Panel"]]

# Volatile state only: a restart clears submitted tokens.
USER_TOKENS = {}
USER_STATES = {}


def api(method, data=None, files=None):
    url = API.format(MANAGER_TOKEN) + "/" + method
    try:
        if files:
            r = requests.post(url, data=data or {}, files=files, timeout=45)
        else:
            r = requests.post(url, json=data or {}, timeout=45)
        return r.json()
    except Exception as exc:
        return {"ok": False, "description": str(exc)}


def send(chat_id, text, keyboard=MENU):
    return api("sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {
            "keyboard": keyboard,
            "resize_keyboard": True,
            "is_persistent": True,
        },
        "disable_web_page_preview": True,
    })


def delete_message(chat_id, message_id):
    api("deleteMessage", {"chat_id": chat_id, "message_id": message_id})


def start(chat_id):
    send(chat_id,
         "🤖 BOT MANAGER\n\nAdd a bot you own, then choose whether to change its name or profile picture.",
         MENU)


def target_token(user_id):
    return USER_TOKENS.get(user_id)


def handle_message(message):
    chat_id = message.get("chat", {}).get("id")
    user = message.get("from", {})
    user_id = user.get("id")
    if not chat_id or not user_id:
        return

    text = (message.get("text") or "").strip()
    state = USER_STATES.get(user_id)

    if text.startswith("/start") or text == "🏠 Main Menu" or text == "⬅️ Back to Panel":
        USER_STATES.pop(user_id, None)
        start(chat_id)
        return

    if text == "/cancel":
        USER_STATES.pop(user_id, None)
        send(chat_id, "Cancelled.", MENU)
        return

    if text == "ℹ️ Help":
        send(chat_id,
             "HELP\n1. Add Bot Token: submit a token for a bot you own.\n"
             "2. Change Name: set that bot's display name.\n"
             "3. Change Picture: send a new profile photo.\n\n"
             "Tokens are kept in memory only and cleared when this process restarts.",
             MENU)
        return

    if text == "🤖 Add Bot Token":
        USER_STATES[user_id] = "waiting_token"
        send(chat_id, "Send the token of a Telegram bot you own or are authorised to manage. "
                      "The message will be deleted after receipt. Send /cancel to stop.", BACK)
        return

    if state == "waiting_token":
        token = text
        delete_message(chat_id, message.get("message_id"))
        if ":" not in token or len(token) < 20:
            send(chat_id, "❌ That does not look like a valid bot token. Try again with Add Bot Token.", MENU)
            USER_STATES.pop(user_id, None)
            return
        result = botban.get_me(token)
        USER_STATES.pop(user_id, None)
        if not result.get("ok"):
            send(chat_id, "❌ Telegram rejected that token. Check it and try again.", MENU)
            return
        USER_TOKENS[user_id] = token
        bot_info = result.get("result", {})
        send(chat_id,
             f"✅ Bot connected: @{bot_info.get('username', 'unknown')}\n"
             "Choose Change Name or Change Picture.",
             MENU)
        return

    if text == "👤 My Session":
        token = target_token(user_id)
        if not token:
            send(chat_id, "No bot token is active. Choose Add Bot Token.", MENU)
            return
        result = botban.get_me(token)
        if result.get("ok"):
            info = result["result"]
            send(chat_id, f"Connected bot: @{info.get('username', 'unknown')}\n"
                          f"Name: {info.get('first_name', 'unknown')}", MENU)
        else:
            USER_TOKENS.pop(user_id, None)
            send(chat_id, "The token is no longer valid. Please add it again.", MENU)
        return

    if text == "❌ Remove Token":
        USER_TOKENS.pop(user_id, None)
        USER_STATES.pop(user_id, None)
        send(chat_id, "✅ The active token was cleared from memory.", MENU)
        return

    if text == "✏️ Change Name":
        if not target_token(user_id):
            send(chat_id, "First choose Add Bot Token.", MENU)
            return
        USER_STATES[user_id] = "waiting_name"
        send(chat_id, "Send the new bot display name (up to 64 characters).", BACK)
        return

    if state == "waiting_name":
        name = text
        if not name or len(name) > 64:
            send(chat_id, "❌ Name must contain 1–64 characters. Try again.", BACK)
            return
        result = botban.set_name(target_token(user_id), name)
        USER_STATES.pop(user_id, None)
        if result.get("ok"):
            send(chat_id, f"✅ Bot name changed to: {name}", MENU)
        else:
            send(chat_id, f"❌ Telegram rejected the change: {result.get('description', 'Unknown error')}", MENU)
        return

    if text == "🖼️ Change Picture":
        if not target_token(user_id):
            send(chat_id, "First choose Add Bot Token.", MENU)
            return
        USER_STATES[user_id] = "waiting_photo"
        send(chat_id, "Now send the new profile picture as a photo (not as a document).", BACK)
        return

    if state == "waiting_photo" and message.get("photo"):
        photo_id = message["photo"][-1]["file_id"]
        meta = api("getFile", {"file_id": photo_id})
        if not meta.get("ok"):
            USER_STATES.pop(user_id, None)
            send(chat_id, "❌ Could not retrieve that photo.", MENU)
            return
        file_path = meta["result"]["file_path"]
        try:
            download = requests.get(
                FILE_API.format(MANAGER_TOKEN) + "/" + file_path, timeout=45
            )
            download.raise_for_status()
            suffix = os.path.splitext(file_path)[1] or ".jpg"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp:
                temp.write(download.content)
                temp_path = temp.name
            try:
                result = botban.set_photo(target_token(user_id), temp_path)
            finally:
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass
            USER_STATES.pop(user_id, None)
            if result.get("ok"):
                send(chat_id, "✅ Bot profile picture updated.", MENU)
            else:
                send(chat_id, f"❌ Telegram rejected the picture: {result.get('description', 'Unknown error')}", MENU)
        except Exception as exc:
            USER_STATES.pop(user_id, None)
            send(chat_id, f"❌ Photo processing failed: {type(exc).__name__}", MENU)
        return

    if state == "waiting_photo":
        send(chat_id, "Please send the image as a Telegram photo, or /cancel.", BACK)
        return

    send(chat_id, "Choose an option from the keyboard.", MENU)


def main():
    if not MANAGER_TOKEN:
        raise SystemExit("Set BOTBAN_MANAGER_TOKEN before starting this interface.")
    check = api("getMe")
    if not check.get("ok"):
        raise SystemExit("Manager bot token was rejected by Telegram.")
    print("Bot manager online: @" + check["result"].get("username", "unknown"))
    offset = 0
    while True:
        try:
            response = api("getUpdates", {
                "offset": offset,
                "timeout": POLL_TIMEOUT,
                "allowed_updates": ["message"],
            })
            if not response.get("ok"):
                print("Telegram polling error:", response.get("description", "unknown"))
                time.sleep(3)
                continue
            for update in response.get("result", []):
                offset = update["update_id"] + 1
                try:
                    if update.get("message"):
                        handle_message(update["message"])
                except Exception as exc:
                    print("Update error:", type(exc).__name__, str(exc))
        except KeyboardInterrupt:
            print("\nBot manager stopped.")
            break
        except Exception as exc:
            print("Polling error:", type(exc).__name__, str(exc))
            time.sleep(3)


if __name__ == "__main__":
    main()
