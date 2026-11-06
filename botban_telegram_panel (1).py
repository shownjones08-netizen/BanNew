RESET = "033[0m"
RESET = "033[0m"
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║   💀 PYTHON SPIRIT — CHANGE NAME & PIC                  ║
║   Creator: SKHHACKER                                    ║
║   FINAL FIX • 100% WORKING                            ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import requests
import json
import base64
from pathlib import Path

# ============================================================
# COLORS
# ============================================================

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
C = '\033[96m'
N = '\033[0m'
BOLD = '\033[1m'

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    clear()
    print(f"""
{R}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   {BOLD}{R}💀 PYTHON SPIRIT — CHANGE NAME & PIC{R}                  ║
║   {BOLD}FINAL FIX • 100% WORKING{R}                                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{N}
""")

# ============================================================
# TELEGRAM API
# ============================================================

def call_api(token, method, data=None, files=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    try:
        if files:
            r = requests.post(url, files=files, timeout=30)
        elif data:
            r = requests.post(url, json=data, timeout=30)
        else:
            r = requests.get(url, timeout=30)
        return r.json()
    except Exception as e:
        return {"ok": False, "description": str(e)}

def get_me(token):
    return call_api(token, "getMe")

def set_name(token, name):
    return call_api(token, "setMyName", {"name": name})

def get_name(token):
    r = call_api(token, "getMyName")
    return r.get("result", {}).get("name", None)

def set_photo(token, photo_path):
    """Set bot profile photo using Telegram Bot API."""
    try:
        if not os.path.exists(photo_path):
            return {"ok": False, "description": "File not found"}

        with open(photo_path, "rb") as f:
            files = {
                "photo": ("photo.jpg", f, "image/jpeg")
            }
            data = {
                "photo": '{"type":"static","photo":"attach://photo"}'
            }

            url = f"https://api.telegram.org/bot{token}/setMyProfilePhoto"
            r = requests.post(url, data=data, files=files, timeout=30)
            return r.json()

    except Exception as e:
        return {"ok": False, "description": str(e)}

# ============================================================
# CHANGE NAME
# ============================================================

def change_name():
    print(f"""
{C}╔═══════════════════════════════════════════════════════════╗
║   {BOLD}✏️  CHANGE BOT NAME{N}{C}                                    ║
╚═══════════════════════════════════════════════════════════╝
{N}
""")
    
    token = input(f"{Y}📤 Enter bot token: {N}").strip()
    if not token:
        print(f"{R}❌ No token!{N}")
        return
    
    print(f"{C}🔍 Checking bot...{N}")
    me = get_me(token)
    if not me.get("ok"):
        print(f"{R}❌ Invalid token!{N}")
        return
    
    bot_username = me["result"].get("username", "Unknown")
    current_name = get_name(token) or me["result"].get("first_name", "Unknown")
    
    print(f"{G}✅ Bot: @{bot_username}{N}")
    print(f"{C}📛 Current Name: {current_name}{N}")
    
    new_name = input(f"{Y}✏️ Enter new name: {N}").strip()
    if not new_name:
        print(f"{R}❌ No name!{N}")
        return
    
    print(f"{C}⏳ Changing name...{N}")
    r = set_name(token, new_name)
    
    if r.get("ok"):
        print(f"{G}✅ Name changed to: {new_name}{N}")
    else:
        print(f"{R}❌ Error: {r.get('description', 'Unknown')}{N}")

# ============================================================
# CHANGE PROFILE PICTURE
# ============================================================

def change_pic():
    print(f"""
{C}╔═══════════════════════════════════════════════════════════╗
║   {BOLD}🖼️  CHANGE PROFILE PICTURE{N}{C}                            ║
║                                                           ║
║   {Y}•{C} Enter bot token                                        ║
║   {Y}•{C} Enter photo file path                                 ║
║   {Y}•{C} 100% WORKING                                         ║
╚═══════════════════════════════════════════════════════════╝
{N}
""")
    
    token = input(f"{Y}📤 Enter bot token: {N}").strip()
    if not token:
        print(f"{R}❌ No token!{N}")
        return
    
    print(f"{C}🔍 Checking bot...{N}")
    me = get_me(token)
    if not me.get("ok"):
        print(f"{R}❌ Invalid token!{N}")
        return
    
    bot_username = me["result"].get("username", "Unknown")
    print(f"{G}✅ Bot: @{bot_username}{N}")
    
    photo_path = input(f"{Y}🖼️ Enter photo file path: {N}").strip()
    if not photo_path:
        print(f"{R}❌ No path!{N}")
        return
    
    if not os.path.exists(photo_path):
        print(f"{R}❌ File not found: {photo_path}{N}")
        return
    
    size = os.path.getsize(photo_path)
    print(f"{C}⏳ Uploading photo... ({size/1024:.1f} KB){N}")
    
    r = set_photo(token, photo_path)
    
    if r.get("ok"):
        print(f"{G}✅ Profile picture updated!{N}")
    else:
        error = r.get('description', 'Unknown')
        print(f"{R}❌ Error: {error}{N}")
        
        if "Not Found" in error or "Bad Request" in error:
            print(f"""
{Y}💡 FIXES:{N}
   1. Use a JPG image (convert PNG to JPG)
   2. Make image smaller (under 500KB)
   3. Use square image (1:1 ratio)
   4. Try this command to convert:
      ffmpeg -i input.png -q:v 2 -vf "scale=500:500" output.jpg
""")

# ============================================================
# MAIN
# ============================================================

def main():
    while True:
        banner()
        
        print(f"""
{BOLD}┌─────────────────────────────────────────────────────────────┐
│  {R}💀 PYTHON SPIRIT — CHANGE NAME & PIC{N}{BOLD}                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  {R}1.{N} {BOLD}CHANGE NAME{N}                                     │
│  {R}2.{N} {BOLD}CHANGE PROFILE PICTURE{N}                         │
│  {R}3.{N} {BOLD}EXIT{N}                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")
        
        choice = input(f"{Y}➜ Enter your choice [1-3]: {N}").strip()
        
        if choice == "3":
            print(f"\n{R}💀 Exiting Python Spirit...{N}")
            sys.exit(0)
        elif choice == "1":
            change_name()
        elif choice == "2":
            change_pic()
        else:
            print(f"{R}❌ Invalid choice!{N}")
        
        input(f"\n{C}Press Enter to continue...{N}")


# =============================================================================
# EXTENDED MANAGEMENT DASHBOARD
# Additive extension: the original call_api(), get_me(), set_name(), get_name(),
# set_photo(), change_name(), change_pic(), banner(), and original main()
# definitions above are retained unchanged. The main() below is a new entry
# point that exposes those existing functions through a local multi-user
# management dashboard.
#
# Dependencies:
#   pip install requests cryptography
#
# Security:
#   - Bot tokens are encrypted at rest with Fernet.
#   - The encryption key is stored separately in botmanager.key.
#   - Local operator passwords are PBKDF2-hashed.
#   - Never share the database and key file together.
# =============================================================================

import sqlite3 as _sqlite3
import hashlib as _hashlib
import secrets as _secrets
import getpass as _getpass
import shutil as _shutil
import zipfile as _zipfile
from datetime import datetime as _datetime
from datetime import timezone as _timezone

DB_FILE = os.getenv("BOTMANAGER_DB", "botmanager.sqlite3")
KEY_FILE = os.getenv("BOTMANAGER_KEY_FILE", "botmanager.key")
BACKUP_DIR = os.getenv("BOTMANAGER_BACKUP_DIR", "botmanager_backups")
PBKDF2_ITERATIONS = 310_000

try:
    from cryptography.fernet import Fernet as _Fernet, InvalidToken as _InvalidToken
except ImportError:
    _Fernet = None
    _InvalidToken = Exception


def _now():
    return _datetime.now(_timezone.utc).isoformat(timespec="seconds")


def _console_clear():
    os.system("cls" if os.name == "nt" else "clear")


def _pause():
    input(f"\n{C}Press Enter to continue...{N}")


def _db():
    connection = _sqlite3.connect(DB_FILE)
    connection.row_factory = _sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def _audit(actor, action, details=""):
    try:
        with _db() as connection:
            connection.execute(
                "INSERT INTO activity_logs(created_at, actor, action, details) VALUES (?, ?, ?, ?)",
                (_now(), str(actor), str(action)[:100], str(details)[:500]),
            )
    except Exception as exc:
        print(f"{Y}Warning: activity log could not be saved: {exc}{N}")


def _init_database():
    with _db() as connection:
        connection.executescript("""
        CREATE TABLE IF NOT EXISTS operators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            password_salt TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('owner','admin','user')),
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS bots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_id TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL,
            first_name TEXT NOT NULL,
            token_ciphertext BLOB NOT NULL,
            added_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS bot_assignments (
            bot_id INTEGER NOT NULL REFERENCES bots(id) ON DELETE CASCADE,
            username TEXT NOT NULL REFERENCES operators(username) ON DELETE CASCADE,
            assigned_by TEXT NOT NULL,
            assigned_at TEXT NOT NULL,
            PRIMARY KEY(bot_id, username)
        );
        CREATE TABLE IF NOT EXISTS access_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_id INTEGER NOT NULL REFERENCES bots(id) ON DELETE CASCADE,
            username TEXT NOT NULL REFERENCES operators(username) ON DELETE CASCADE,
            reason TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            reviewed_by TEXT,
            reviewed_at TEXT
        );
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            actor TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT NOT NULL
        );
        """)
        connection.commit()


def _get_cipher():
    if _Fernet is None:
        raise RuntimeError(
            "Missing dependency 'cryptography'. Install it with: pip install cryptography"
        )
    key_path = Path(KEY_FILE)
    if key_path.exists():
        key = key_path.read_bytes().strip()
    else:
        key = _Fernet.generate_key()
        key_path.write_bytes(key + b"\n")
        try:
            os.chmod(key_path, 0o600)
        except OSError:
            pass
    try:
        return _Fernet(key)
    except Exception as exc:
        raise RuntimeError(
            f"Encryption key file {KEY_FILE!r} is invalid. Restore the matching key backup."
        ) from exc


def _password_record(password, salt=None):
    if salt is None:
        salt = _secrets.token_bytes(16)
    digest = _hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return digest.hex(), salt.hex()


def _verify_password(password, stored_hash, stored_salt):
    calculated, _ = _password_record(password, bytes.fromhex(stored_salt))
    return _secrets.compare_digest(calculated, stored_hash)


def _operator_count():
    with _db() as connection:
        return connection.execute("SELECT COUNT(*) FROM operators").fetchone()[0]


def _create_first_owner():
    print(f"\n{C}First launch: create the local owner account.{N}")
    while True:
        username = input("Owner username: ").strip()
        if username and len(username) <= 40:
            break
        print("Choose a username of 1–40 characters.")
    while True:
        password = _getpass.getpass("Owner password (12+ characters): ")
        if len(password) >= 12:
            confirm = _getpass.getpass("Confirm password: ")
            if password == confirm:
                break
            print("Passwords do not match.")
        else:
            print("Password must contain at least 12 characters.")
    password_hash, salt = _password_record(password)
    with _db() as connection:
        connection.execute(
            "INSERT INTO operators(username,password_hash,password_salt,role,created_at) "
            "VALUES(?,?,?,?,?)",
            (username, password_hash, salt, "owner", _now()),
        )
    _audit(username, "owner_account_created")
    print(f"{G}Owner account created.{N}")


def _login():
    for _ in range(3):
        print(f"\n{BOLD}{C}BOT MANAGER — SIGN IN{N}")
        username = input("Username: ").strip()
        password = _getpass.getpass("Password: ")
        with _db() as connection:
            operator = connection.execute(
                "SELECT * FROM operators WHERE username=? COLLATE NOCASE AND active=1",
                (username,),
            ).fetchone()
        if operator and _verify_password(
            password, operator["password_hash"], operator["password_salt"]
        ):
            _audit(operator["username"], "login_success")
            return dict(operator)
        print(f"{R}Invalid credentials or inactive account.{N}")
        time.sleep(1)
    return None


def _require_role(operator, *roles):
    if operator["role"] not in roles:
        print(f"{R}Permission denied.{N}")
        return False
    return True


def _list_bots(operator, only_accessible=True):
    with _db() as connection:
        if not only_accessible or operator["role"] in ("owner", "admin"):
            rows = connection.execute(
                "SELECT * FROM bots WHERE active=1 ORDER BY id DESC"
            ).fetchall()
        else:
            rows = connection.execute(
                """SELECT b.* FROM bots b
                   JOIN bot_assignments a ON a.bot_id=b.id
                   WHERE b.active=1 AND a.username=?
                   ORDER BY b.id DESC""",
                (operator["username"],),
            ).fetchall()
    return rows


def _bot_token(bot_row):
    cipher = _get_cipher()
    try:
        return cipher.decrypt(bytes(bot_row["token_ciphertext"])).decode("utf-8")
    except _InvalidToken as exc:
        raise RuntimeError(
            "Cannot decrypt this bot token. The matching botmanager.key file is required."
        ) from exc


def _choose_bot(operator, admin_all=False):
    rows = _list_bots(operator, only_accessible=not admin_all)
    if not rows:
        print(f"{Y}No bots are available for this account.{N}")
        return None
    print(f"\n{BOLD}REGISTERED BOTS{N}")
    for index, row in enumerate(rows, 1):
        print(f"{index}. @{row['username']} — {row['first_name']} (ID {row['bot_id']})")
    try:
        selected = int(input("Select bot number (0 to cancel): "))
    except ValueError:
        return None
    if selected == 0 or not 1 <= selected <= len(rows):
        return None
    return rows[selected - 1]


def _add_bot(operator):
    if not _require_role(operator, "owner", "admin"):
        return
    print(f"\n{BOLD}{C}REGISTER A BOT YOU OWN OR ARE AUTHORIZED TO MANAGE{N}")
    token = _getpass.getpass("Bot token (input hidden): ").strip()
    if not token:
        print("No token supplied.")
        return
    print("Validating token with Telegram...")
    result = get_me(token)
    if not result.get("ok"):
        print(f"{R}Token validation failed: {result.get('description', 'Unknown error')}{N}")
        _audit(operator["username"], "bot_token_validation_failed")
        return
    bot = result["result"]
    bot_id = str(bot.get("id"))
    username = bot.get("username") or "unknown"
    first_name = bot.get("first_name") or "Unknown"
    cipher = _get_cipher()
    encrypted = cipher.encrypt(token.encode("utf-8"))
    try:
        with _db() as connection:
            connection.execute(
                """INSERT OR IGNORE INTO bots(bot_id,username,first_name,token_ciphertext,added_by,created_at)
                   VALUES(?,?,?,?,?,?)""",
                (bot_id, username, first_name, encrypted, operator["username"], _now()),
            )
        _audit(operator["username"], "bot_added", f"@{username} id={bot_id}")
        print(f"{G}Added @{username} successfully. Token encrypted in local database.{N}")
    except _sqlite3.IntegrityError:
        print(f"{Y}This bot is already registered.{N}")


def _remove_bot(operator):
    if not _require_role(operator, "owner", "admin"):
        return
    row = _choose_bot(operator, admin_all=True)
    if not row:
        return
    confirm = input(f"Deactivate @{row['username']}? Type YES: ").strip()
    if confirm != "YES":
        print("Cancelled.")
        return
    with _db() as connection:
        connection.execute("UPDATE bots SET active=0 WHERE id=?", (row["id"],))
    _audit(operator["username"], "bot_deactivated", f"@{row['username']}")
    print(f"{G}Bot removed from this manager (the Telegram bot itself is not deleted).{N}")


def _validate_bot(operator):
    row = _choose_bot(operator, admin_all=operator["role"] in ("owner", "admin"))
    if not row:
        return
    try:
        result = get_me(_bot_token(row))
        if result.get("ok"):
            bot = result["result"]
            print(f"{G}Token valid: @{bot.get('username')} (ID {bot.get('id')}){N}")
            _audit(operator["username"], "bot_token_validated", f"@{row['username']}")
        else:
            print(f"{R}Telegram rejected the token: {result.get('description')}{N}")
            _audit(operator["username"], "bot_token_invalid", f"@{row['username']}")
    except Exception as exc:
        print(f"{R}Validation error: {exc}{N}")


def _edit_bot_profile(operator, action):
    row = _choose_bot(operator, admin_all=operator["role"] in ("owner", "admin"))
    if not row:
        return
    try:
        token = _bot_token(row)
        if action == "name":
            current = get_name(token)
            print(f"Current bot name: {current or row['first_name']}")
            value = input("New bot name: ").strip()
            if not value:
                return
            result = set_name(token, value)
        elif action == "photo":
            path = input("Image file path: ").strip().strip('"')
            if not path:
                return
            result = set_photo(token, path)
        elif action == "description":
            value = input("New bot description (up to Telegram's limit): ").strip()
            if not value:
                return
            result = call_api(token, "setMyDescription", {"description": value})
        else:
            return
        if result.get("ok"):
            print(f"{G}Updated @{row['username']} successfully.{N}")
            _audit(operator["username"], f"bot_{action}_updated", f"@{row['username']}")
        else:
            print(f"{R}Telegram API error: {result.get('description', 'Unknown error')}{N}")
            _audit(operator["username"], f"bot_{action}_failed", str(result.get("description", "")))
    except Exception as exc:
        print(f"{R}Operation failed: {exc}{N}")
        _audit(operator["username"], f"bot_{action}_exception", type(exc).__name__)


def _user_management(operator):
    if not _require_role(operator, "owner", "admin"):
        return
    while True:
        print(f"\n{BOLD}{C}USER MANAGEMENT{N}")
        print("1. Create operator")
        print("2. List operators")
        print("3. Activate/deactivate operator")
        print("4. Assign bot to user")
        print("5. Return")
        choice = input("Select: ").strip()
        if choice == "1":
            username = input("New username: ").strip()
            if not username or len(username) > 40:
                print("Invalid username.")
                continue
            if operator["role"] != "owner":
                role = "user"
            else:
                role = input("Role [admin/user]: ").strip().lower()
                if role not in ("admin", "user"):
                    print("Invalid role.")
                    continue
            password = _getpass.getpass("Temporary password (12+ characters): ")
            if len(password) < 12:
                print("Password too short.")
                continue
            password_hash, salt = _password_record(password)
            try:
                with _db() as connection:
                    connection.execute(
                        "INSERT INTO operators(username,password_hash,password_salt,role,created_at) "
                        "VALUES(?,?,?,?,?)",
                        (username, password_hash, salt, role, _now()),
                    )
                _audit(operator["username"], "operator_created", f"{username}:{role}")
                print(f"{G}Created {username} as {role}.{N}")
            except _sqlite3.IntegrityError:
                print("That username already exists.")
        elif choice == "2":
            with _db() as connection:
                rows = connection.execute(
                    "SELECT username,role,active,created_at FROM operators ORDER BY id"
                ).fetchall()
            for row in rows:
                print(f"{row['username']} | {row['role']} | "
                      f"{'active' if row['active'] else 'inactive'} | {row['created_at']}")
        elif choice == "3":
            if operator["role"] != "owner":
                print("Only the owner can change account activation.")
                continue
            username = input("Username: ").strip()
            if username.lower() == operator["username"].lower():
                print("You cannot deactivate your own owner account here.")
                continue
            with _db() as connection:
                target = connection.execute(
                    "SELECT role FROM operators WHERE username=? COLLATE NOCASE",
                    (username,),
                ).fetchone()
                if not target or target["role"] == "owner":
                    print("User not found or protected owner account.")
                    continue
                connection.execute(
                    "UPDATE operators SET active=1-active WHERE username=? COLLATE NOCASE",
                    (username,),
                )
            _audit(operator["username"], "operator_activation_toggled", username)
            print("Operator activation toggled.")
        elif choice == "4":
            if operator["role"] != "owner":
                print("Only the owner can assign bots.")
                continue
            row = _choose_bot(operator, admin_all=True)
            if not row:
                continue
            username = input("Assign to username: ").strip()
            with _db() as connection:
                exists = connection.execute(
                    "SELECT 1 FROM operators WHERE username=? COLLATE NOCASE AND active=1",
                    (username,),
                ).fetchone()
                if not exists:
                    print("Active operator not found.")
                    continue
                connection.execute(
                    "INSERT OR IGNORE INTO bot_assignments(bot_id,username,assigned_by,assigned_at) "
                    "VALUES(?,?,?,?)",
                    (row["id"], username, operator["username"], _now()),
                )
            _audit(operator["username"], "bot_assigned", f"{row['username']}->{username}")
            print("Bot assignment saved.")
        elif choice == "5":
            return
        else:
            print("Invalid selection.")


def _my_bots(operator):
    rows = _list_bots(operator, only_accessible=True)
    if not rows:
        print("No bots assigned. Use Request access or contact an administrator.")
        return
    for row in rows:
        print(f"@{row['username']} | {row['first_name']} | ID {row['bot_id']}")


def _request_access(operator):
    with _db() as connection:
        rows = connection.execute("SELECT id,username,first_name FROM bots WHERE active=1").fetchall()
    if not rows:
        print("No active bots are registered.")
        return
    print("Available bots:")
    for index, row in enumerate(rows, 1):
        print(f"{index}. @{row['username']}")
    try:
        index = int(input("Choose bot number: "))
        if not 1 <= index <= len(rows):
            return
    except ValueError:
        return
    reason = input("Why do you need access? ").strip()[:300]
    with _db() as connection:
        connection.execute(
            "INSERT INTO access_requests(bot_id,username,reason,created_at) VALUES(?,?,?,?)",
            (rows[index - 1]["id"], operator["username"], reason, _now()),
        )
    _audit(operator["username"], "bot_access_requested", rows[index - 1]["username"])
    print(f"{G}Access request sent to the local owner/admin for review.{N}")


def _review_access_requests(operator):
    if not _require_role(operator, "owner", "admin"):
        return
    with _db() as connection:
        rows = connection.execute(
            """SELECT r.*,b.username AS bot_username FROM access_requests r
               JOIN bots b ON b.id=r.bot_id WHERE r.status='pending' ORDER BY r.id"""
        ).fetchall()
    if not rows:
        print("No pending access requests.")
        return
    for row in rows:
        print(f"#{row['id']} | {row['username']} -> @{row['bot_username']} | {row['reason']}")
    try:
        request_id = int(input("Request ID to review (0 to cancel): "))
    except ValueError:
        return
    if request_id == 0:
        return
    decision = input("Approve or reject [a/r]: ").strip().lower()
    with _db() as connection:
        request = connection.execute(
            "SELECT * FROM access_requests WHERE id=? AND status='pending'",
            (request_id,),
        ).fetchone()
        if not request:
            print("Pending request not found.")
            return
        status = "approved" if decision == "a" else "rejected" if decision == "r" else None
        if not status:
            return
        connection.execute(
            "UPDATE access_requests SET status=?,reviewed_by=?,reviewed_at=? WHERE id=?",
            (status, operator["username"], _now(), request_id),
        )
        if status == "approved":
            connection.execute(
                "INSERT OR IGNORE INTO bot_assignments(bot_id,username,assigned_by,assigned_at) "
                "VALUES(?,?,?,?)",
                (request["bot_id"], request["username"], operator["username"], _now()),
            )
    _audit(operator["username"], "access_request_reviewed", f"{request_id}:{status}")
    print(f"{G}Request {status}.{N}")


def _statistics(operator):
    if not _require_role(operator, "owner", "admin"):
        return
    with _db() as connection:
        total_bots = connection.execute("SELECT COUNT(*) FROM bots WHERE active=1").fetchone()[0]
        total_users = connection.execute("SELECT COUNT(*) FROM operators WHERE active=1").fetchone()[0]
        total_assignments = connection.execute("SELECT COUNT(*) FROM bot_assignments").fetchone()[0]
        pending = connection.execute(
            "SELECT COUNT(*) FROM access_requests WHERE status='pending'"
        ).fetchone()[0]
        actions = connection.execute("SELECT COUNT(*) FROM activity_logs").fetchone()[0]
    print(f"\n{BOLD}{C}MANAGER STATISTICS{N}")
    print(f"Active bots:       {total_bots}")
    print(f"Active operators:  {total_users}")
    print(f"Bot assignments:   {total_assignments}")
    print(f"Pending requests:  {pending}")
    print(f"Logged actions:    {actions}")


def _activity_logs(operator):
    if not _require_role(operator, "owner", "admin"):
        return
    with _db() as connection:
        rows = connection.execute(
            "SELECT * FROM activity_logs ORDER BY id DESC LIMIT 50"
        ).fetchall()
    print(f"\n{BOLD}{C}RECENT ACTIVITY (latest 50){N}")
    for row in rows:
        print(f"{row['created_at']} | {row['actor']} | {row['action']} | {row['details']}")


def _broadcast_announcement(operator):
    if not _require_role(operator, "owner", "admin"):
        return
    message = input("Announcement for manager users: ").strip()
    if not message:
        return
    with _db() as connection:
        connection.execute(
            "INSERT INTO announcements(message,created_by,created_at) VALUES(?,?,?)",
            (message[:2000], operator["username"], _now()),
        )
    _audit(operator["username"], "announcement_created")
    print(f"{G}Announcement published to the local dashboard users.{N}")


def _show_announcements(operator):
    with _db() as connection:
        rows = connection.execute(
            "SELECT * FROM announcements ORDER BY id DESC LIMIT 5"
        ).fetchall()
    if rows:
        print(f"\n{BOLD}{Y}ANNOUNCEMENTS{N}")
        for row in rows:
            print(f"- [{row['created_at']}] {row['message']}")


def _backup_database(operator):
    if not _require_role(operator, "owner"):
        return
    os.makedirs(BACKUP_DIR, exist_ok=True)
    filename = os.path.join(
        BACKUP_DIR, f"botmanager-{_datetime.now().strftime('%Y%m%d-%H%M%S')}.sqlite3"
    )
    source = _sqlite3.connect(DB_FILE)
    destination = _sqlite3.connect(filename)
    try:
        source.backup(destination)
    finally:
        destination.close()
        source.close()
    try:
        os.chmod(filename, 0o600)
    except OSError:
        pass
    _audit(operator["username"], "database_backup_created", filename)
    print(f"{G}Database backup created: {filename}{N}")
    print(f"{Y}Keep the separate {KEY_FILE} key file safe. The database backup alone cannot decrypt stored bot tokens.{N}")


def _restore_database(operator):
    if not _require_role(operator, "owner"):
        return
    path = input("Path to SQLite backup: ").strip().strip('"')
    if not os.path.isfile(path):
        print("Backup file not found.")
        return
    confirm = input("This replaces the current manager database. Type RESTORE: ").strip()
    if confirm != "RESTORE":
        print("Cancelled.")
        return
    try:
        # Validate source database before replacing the active DB.
        source = _sqlite3.connect(f"file:{Path(path).resolve()}?mode=ro", uri=True)
        integrity = source.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            source.close()
            print(f"Backup integrity check failed: {integrity}")
            return
        destination = _sqlite3.connect(DB_FILE)
        source.backup(destination)
        destination.close()
        source.close()
        _audit(operator["username"], "database_restored", Path(path).name)
        print(f"{G}Database restored. Restart the manager before further use.{N}")
    except Exception as exc:
        print(f"{R}Restore failed: {exc}{N}")


def _change_password(operator):
    current = _getpass.getpass("Current password: ")
    with _db() as connection:
        row = connection.execute(
            "SELECT * FROM operators WHERE username=?",
            (operator["username"],),
        ).fetchone()
    if not row or not _verify_password(current, row["password_hash"], row["password_salt"]):
        print("Current password is incorrect.")
        return
    new_password = _getpass.getpass("New password (12+ characters): ")
    if len(new_password) < 12:
        print("Password too short.")
        return
    digest, salt = _password_record(new_password)
    with _db() as connection:
        connection.execute(
            "UPDATE operators SET password_hash=?,password_salt=? WHERE username=?",
            (digest, salt, operator["username"]),
        )
    _audit(operator["username"], "password_changed")
    print(f"{G}Password changed.{N}")


def _dashboard(operator):
    while True:
        _console_clear()
        print(f"""{C}{BOLD}
╔══════════════════════════════════════════════════════════════╗
║                 PYTHON SPIRIT • BOT MANAGER                 ║
╠══════════════════════════════════════════════════════════════╣
║  Signed in: {operator['username']:<18} Role: {operator['role']:<12}║
╚══════════════════════════════════════════════════════════════╝{N}""")
        _show_announcements(operator)
        print(f"""
{BOLD}BOT OPERATIONS{N}
  1. My / assigned bots
  2. Add bot (owner/admin)
  3. Remove bot (owner/admin)
  4. Validate bot token
  5. Change bot name
  6. Change bot profile picture
  7. Change bot description

{BOLD}TEAM OPERATIONS{N}
  8. User management (owner/admin)
  9. Request bot access
 10. Review access requests (owner/admin)
 11. Statistics (owner/admin)
 12. Activity logs (owner/admin)
 13. Broadcast announcement (owner/admin)

{BOLD}SYSTEM{N}
 14. Backup database (owner)
 15. Restore database (owner)
 16. Change my password
 17. Logout
""")
        choice = input(f"{Y}Select an option: {N}").strip()
        if choice == "1":
            _my_bots(operator)
        elif choice == "2":
            _add_bot(operator)
        elif choice == "3":
            _remove_bot(operator)
        elif choice == "4":
            _validate_bot(operator)
        elif choice == "5":
            _edit_bot_profile(operator, "name")
        elif choice == "6":
            _edit_bot_profile(operator, "photo")
        elif choice == "7":
            _edit_bot_profile(operator, "description")
        elif choice == "8":
            _user_management(operator)
        elif choice == "9":
            _request_access(operator)
        elif choice == "10":
            _review_access_requests(operator)
        elif choice == "11":
            _statistics(operator)
        elif choice == "12":
            _activity_logs(operator)
        elif choice == "13":
            _broadcast_announcement(operator)
        elif choice == "14":
            _backup_database(operator)
        elif choice == "15":
            _restore_database(operator)
        elif choice == "16":
            _change_password(operator)
        elif choice == "17":
            _audit(operator["username"], "logout")
            break
        else:
            print(f"{R}Invalid selection.{N}")
        _pause()


def main():
    if _Fernet is None:
        print("Install required packages first: pip install requests cryptography")
        return
    try:
        _init_database()
        _get_cipher()  # Create/load encryption key before accepting bot tokens.
        if _operator_count() == 0:
            _create_first_owner()
        while True:
            operator = _login()
            if not operator:
                print(f"{R}Too many failed login attempts. Exiting.{N}")
                return
            _dashboard(operator)
            if input("Exit manager? [y/N]: ").strip().lower() == "y":
                return
    except KeyboardInterrupt:
        print(f"\n{Y}Manager stopped safely.{N}")
    except Exception as exc:
        print(f"{R}Manager error: {exc}{N}")
        raise





# =============================================================================
# TELEGRAM REPLY-KEYBOARD PANEL — ADDITIVE EXTENSION
# Original functions above are retained. This extension adds a Telegram-facing
# user/admin panel. It uses a separate manager bot token and the same encrypted
# bot-token storage/database. It never displays or forwards submitted bot tokens.
#
# Environment:
#   MANAGER_BOT_TOKEN="token of the panel bot"
#   PANEL_OWNER_IDS="123456789,987654321"  (Telegram numeric user IDs)
#   FORCE_JOIN_CHAT="@your_channel"         (optional)
#
# Install:
#   pip install requests cryptography
# =============================================================================

import html as _html
import threading as _threading

_PANEL_STATES = {}
_PANEL_STOP = False
_PANEL_POLL_TIMEOUT = 25
_PANEL_BUTTONS = {
    "user": [
        ["🤖 Add Bot Token", "🗂️ My Bots"],
        ["✏️ Change Name", "📝 Change Description"],
        ["🖼️ Change Picture", "👤 User Hub"],
        ["📊 Token Usage", "🔗 Referrals"],
        ["💎 Premium", "✅ Successful"],
        ["❌ Rejected", "🆘 Support"],
        ["ℹ️ Help", "🏠 Main Menu"],
    ],
    "admin": [
        ["📡 Live Connect", "📢 Broadcast"],
        ["⚙️ System Manager", "🖼️ Media Manager"],
        ["➕ Add Admin", "⭐ Add Points"],
        ["📣 Force Join", "💎 Premium Access"],
        ["📥 Pending Tokens", "📈 Statistics"],
        ["⬅️ User Panel", "🏠 Main Menu"],
    ],
}
_PANEL_BACK = [["⬅️ Back to Panel"]]


def _panel_owner_ids():
    raw = os.getenv("PANEL_OWNER_IDS", "")
    return {int(x.strip()) for x in raw.split(",") if x.strip().isdigit()}


def _panel_init():
    _init_database()
    _get_cipher()
    with _db() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS panel_users(
            tg_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT,
            points INTEGER NOT NULL DEFAULT 0, referred_by INTEGER,
            created_at TEXT NOT NULL, last_seen TEXT NOT NULL,
            is_premium INTEGER NOT NULL DEFAULT 0, premium_until TEXT
        );
        CREATE TABLE IF NOT EXISTS panel_admins(
            tg_id INTEGER PRIMARY KEY, added_by INTEGER NOT NULL, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS panel_token_requests(
            id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id INTEGER NOT NULL,
            bot_id TEXT NOT NULL, username TEXT NOT NULL, first_name TEXT NOT NULL,
            token_ciphertext BLOB NOT NULL, status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL, reviewed_at TEXT, reviewed_by INTEGER
        );
        CREATE TABLE IF NOT EXISTS panel_usage(
            tg_id INTEGER PRIMARY KEY, tokens_submitted INTEGER NOT NULL DEFAULT 0,
            approved INTEGER NOT NULL DEFAULT 0, rejected INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS panel_settings(
            key TEXT PRIMARY KEY, value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS panel_support(
            id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id INTEGER NOT NULL,
            message TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'open',
            created_at TEXT NOT NULL
        );
        """)
        for owner_id in _panel_owner_ids():
            con.execute(
                "INSERT OR IGNORE INTO panel_admins(tg_id,added_by,created_at) VALUES(?,?,?)",
                (owner_id, owner_id, _now()),
            )


def _panel_is_admin(tg_id):
    with _db() as con:
        return bool(con.execute(
            "SELECT 1 FROM panel_admins WHERE tg_id=?", (tg_id,)
        ).fetchone())


def _panel_setting(key, default=""):
    with _db() as con:
        row = con.execute("SELECT value FROM panel_settings WHERE key=?", (key,)).fetchone()
    return row["value"] if row else default


def _panel_set_setting(key, value):
    with _db() as con:
        con.execute(
            "INSERT INTO panel_settings(key,value) VALUES(?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, str(value)),
        )


def _panel_api(token, method, data=None, files=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    try:
        if files:
            response = requests.post(url, data=data or {}, files=files, timeout=45)
        else:
            response = requests.post(url, json=data or {}, timeout=45)
        return response.json()
    except Exception as exc:
        return {"ok": False, "description": str(exc)}


def _panel_send(chat_id, text, keyboard=None, parse_mode="HTML"):
    token = os.getenv("MANAGER_BOT_TOKEN", "").strip()
    if not token:
        return {"ok": False, "description": "MANAGER_BOT_TOKEN is not configured"}
    markup = {"keyboard": keyboard or _PANEL_BUTTONS["user"],
              "resize_keyboard": True, "is_persistent": True}
    return _panel_api(token, "sendMessage", {
        "chat_id": chat_id, "text": text, "parse_mode": parse_mode,
        "reply_markup": markup, "disable_web_page_preview": True,
    })


def _panel_quote(chat_id, heading, body, keyboard=None):
    safe_heading = _html.escape(str(heading))
    safe_body = _html.escape(str(body))
    return _panel_send(
        chat_id, f"<blockquote><b>{safe_heading}</b>\n{safe_body}</blockquote>",
        keyboard or _PANEL_BACK,
    )


def _panel_register_user(user, start_arg=""):
    tg_id = int(user["id"])
    referrer = int(start_arg[4:]) if start_arg.startswith("ref_") and start_arg[4:].isdigit() else None
    if referrer == tg_id:
        referrer = None
    with _db() as con:
        exists = con.execute("SELECT 1 FROM panel_users WHERE tg_id=?", (tg_id,)).fetchone()
        if not exists:
            con.execute(
                """INSERT INTO panel_users(tg_id,username,first_name,referred_by,created_at,last_seen)
                   VALUES(?,?,?,?,?,?)""",
                (tg_id, user.get("username", ""), user.get("first_name", ""),
                 referrer, _now(), _now()),
            )
            con.execute("INSERT OR IGNORE INTO panel_usage(tg_id) VALUES(?)", (tg_id,))
            if referrer:
                con.execute("UPDATE panel_users SET points=points+1 WHERE tg_id=?", (referrer,))
        else:
            con.execute(
                "UPDATE panel_users SET username=?,first_name=?,last_seen=? WHERE tg_id=?",
                (user.get("username", ""), user.get("first_name", ""), _now(), tg_id),
            )


def _panel_join_ok(tg_id):
    channel = os.getenv("FORCE_JOIN_CHAT", "").strip()
    if not channel:
        channel = _panel_setting("force_join")
    if not channel or channel.lower() == "off":
        return True
    token = os.getenv("MANAGER_BOT_TOKEN", "").strip()
    result = _panel_api(token, "getChatMember", {"chat_id": channel, "user_id": tg_id})
    if not result.get("ok"):
        return False
    status = result.get("result", {}).get("status")
    return status in ("creator", "administrator", "member")


def _panel_user_menu(chat_id):
    _panel_send(chat_id, "👤 <b>USER PANEL</b>\nChoose an option below.", _PANEL_BUTTONS["user"])


def _panel_admin_menu(chat_id):
    _panel_send(chat_id, "💗 <b>ADMIN PANEL — PAGE 1/1</b>\nChoose an admin feature from the keyboard below.",
                _PANEL_BUTTONS["admin"])


def _panel_stats(tg_id):
    with _db() as con:
        user = con.execute("SELECT * FROM panel_users WHERE tg_id=?", (tg_id,)).fetchone()
        usage = con.execute("SELECT * FROM panel_usage WHERE tg_id=?", (tg_id,)).fetchone()
        bots = con.execute(
            "SELECT COUNT(*) FROM panel_token_requests WHERE tg_id=? AND status='approved'",
            (tg_id,),
        ).fetchone()[0]
    return user, usage, bots


def _panel_begin_token(chat_id, tg_id):
    _PANEL_STATES[tg_id] = {"step": "token"}
    _panel_quote(chat_id, "ADD BOT TOKEN",
        "Send the token for a bot you own or are explicitly authorized to manage. "
        "The token is encrypted and hidden from chat responses. Admin approval is required.")


def _panel_handle_text(message):
    user = message.get("from", {})
    chat_id = message.get("chat", {}).get("id")
    tg_id = int(user.get("id", 0))
    text_in = (message.get("text") or "").strip()
    if not chat_id or not tg_id:
        return
    _panel_register_user(user)
    is_admin = _panel_is_admin(tg_id)
    state = _PANEL_STATES.get(tg_id, {})

    if text_in.startswith("/start"):
        arg = text_in.split(maxsplit=1)[1] if len(text_in.split()) > 1 else ""
        _panel_register_user(user, arg)
        if not _panel_join_ok(tg_id):
            channel = os.getenv("FORCE_JOIN_CHAT", "") or _panel_setting("force_join")
            _panel_quote(chat_id, "FORCE JOIN", f"Please join {channel}, then press /start.")
            return
        _panel_user_menu(chat_id)
        return
    if text_in == "/admin" and is_admin:
        _panel_admin_menu(chat_id)
        return
    if text_in in ("🏠 Main Menu", "⬅️ Back to Panel"):
        _PANEL_STATES.pop(tg_id, None)
        _panel_admin_menu(chat_id) if is_admin and text_in == "🏠 Main Menu" else _panel_user_menu(chat_id)
        return
    if text_in == "⬅️ User Panel":
        _PANEL_STATES.pop(tg_id, None)
        _panel_user_menu(chat_id)
        return

    # Stateful user/admin workflows
    step = state.get("step")
    if step == "choose_edit_bot":
        ids = state.get("ids", [])
        if not text_in.isdigit() or not 1 <= int(text_in) <= len(ids):
            _panel_quote(chat_id, "INVALID SELECTION", "Send a valid bot number.")
            return
        selected_id = ids[int(text_in) - 1]
        mode = state.get("mode")
        _PANEL_STATES[tg_id] = {"step": mode, "bot_id": selected_id}
        prompt = "Send the new bot name." if mode == "edit_name" else (
            "Send the new bot description." if mode == "edit_description"
            else "Send the bot number again to confirm picture workflow."
        )
        if mode == "photo_bot":
            _PANEL_STATES[tg_id] = {"step": "photo_upload", "bot_id": selected_id}
            _panel_quote(chat_id, "CHANGE PICTURE", "Now send the new profile photo as an image.")
        else:
            _panel_quote(chat_id, "BOT PROFILE UPDATE", prompt)
        return
    if step == "token":
        token_value = text_in
        # Reduce exposure in chat history; only accept tokens for bots the user owns.
        _panel_api(os.getenv("MANAGER_BOT_TOKEN", ""), "deleteMessage",
                   {"chat_id": chat_id, "message_id": message.get("message_id")})
        if len(token_value) < 20 or ":" not in token_value:
            _panel_quote(chat_id, "REJECTED", "That does not look like a Telegram bot token. Send a valid token or /cancel.")
            return
        result = get_me(token_value)
        if not result.get("ok"):
            _panel_quote(chat_id, "REJECTED", "Telegram token validation failed. Check it and try again.")
            with _db() as con:
                con.execute("UPDATE panel_usage SET rejected=rejected+1 WHERE tg_id=?", (tg_id,))
            _PANEL_STATES.pop(tg_id, None)
            return
        bot = result["result"]
        cipher = _get_cipher()
        with _db() as con:
            con.execute(
                """INSERT INTO panel_token_requests(tg_id,bot_id,username,first_name,token_ciphertext,created_at)
                   VALUES(?,?,?,?,?,?)""",
                (tg_id, str(bot["id"]), bot.get("username", "unknown"),
                 bot.get("first_name", "Unknown"), cipher.encrypt(token_value.encode()), _now()),
            )
            con.execute(
                "UPDATE panel_usage SET tokens_submitted=tokens_submitted+1 WHERE tg_id=?", (tg_id,)
            )
        _PANEL_STATES.pop(tg_id, None)
        _panel_quote(chat_id, "SUBMITTED SUCCESSFULLY",
                     f"@{bot.get('username','unknown')} is queued for admin review. You will receive the decision.")
        return
    if step in ("edit_name", "edit_description"):
        bot_id = state.get("bot_id")
        with _db() as con:
            row = con.execute(
                "SELECT * FROM panel_token_requests WHERE id=? AND tg_id=? AND status='approved'",
                (bot_id, tg_id),
            ).fetchone()
        if not row:
            _PANEL_STATES.pop(tg_id, None)
            _panel_quote(chat_id, "BOT NOT FOUND", "No approved bot selected.")
            return
        cipher = _get_cipher()
        bot_token = cipher.decrypt(row["token_ciphertext"]).decode()
        method = "setMyName" if step == "edit_name" else "setMyDescription"
        field = "name" if step == "edit_name" else "description"
        result = _panel_api(bot_token, method, {field: text_in[:64 if field == "name" else 512]})
        _PANEL_STATES.pop(tg_id, None)
        _panel_quote(chat_id, "UPDATE SUCCESSFUL" if result.get("ok") else "UPDATE REJECTED",
                     f"@{row['username']}: {result.get('description', 'Updated successfully' if result.get('ok') else 'Telegram API rejected the change')}")
        return
    if step == "photo_bot":
        if not text_in.isdigit():
            _panel_quote(chat_id, "INVALID SELECTION", "Send the bot number shown in My Bots.")
            return
        _PANEL_STATES[tg_id] = {"step": "photo_upload", "bot_id": int(text_in)}
        _panel_quote(chat_id, "CHANGE PICTURE", "Now send the new profile photo as an image.")
        return
    if step == "support":
        with _db() as con:
            cur = con.execute(
                "INSERT INTO panel_support(tg_id,message,created_at) VALUES(?,?,?)",
                (tg_id, text_in[:2000], _now()),
            )
            ticket_id = cur.lastrowid
        _PANEL_STATES.pop(tg_id, None)
        _panel_quote(chat_id, "SUPPORT TICKET CREATED", f"Ticket #{ticket_id} has been sent to the support queue.")
        return
    if step == "broadcast" and is_admin:
        _PANEL_STATES.pop(tg_id, None)
        with _db() as con:
            recipients = [r["tg_id"] for r in con.execute("SELECT tg_id FROM panel_users").fetchall()]
        sent = failed = 0
        for recipient in recipients:
            result = _panel_send(recipient, _html.escape(text_in))
            if result.get("ok"): sent += 1
            else: failed += 1
        _panel_quote(chat_id, "BROADCAST FINISHED", f"Successful: {sent}\nRejected: {failed}")
        return
    if step == "new_admin" and is_admin:
        _PANEL_STATES.pop(tg_id, None)
        if not text_in.isdigit():
            _panel_quote(chat_id, "REJECTED", "Send a numeric Telegram user ID.")
            return
        new_id = int(text_in)
        with _db() as con:
            con.execute("INSERT OR IGNORE INTO panel_admins(tg_id,added_by,created_at) VALUES(?,?,?)",
                        (new_id, tg_id, _now()))
        _panel_quote(chat_id, "ADMIN ADDED", f"Telegram user ID {new_id} can now access the admin panel.")
        return
    if step in ("points", "premium", "force_join") and is_admin:
        _PANEL_STATES.pop(tg_id, None)
        parts = text_in.split()
        if step == "force_join":
            _panel_set_setting("force_join", text_in)
            _panel_quote(chat_id, "FORCE JOIN UPDATED", f"Required channel set to {text_in}")
            return
        if len(parts) < 2 or not parts[0].isdigit():
            _panel_quote(chat_id, "INVALID INPUT", "Format: USER_ID VALUE")
            return
        target, value = int(parts[0]), parts[1]
        if step == "points" and value.lstrip("-").isdigit():
            with _db() as con:
                con.execute("UPDATE panel_users SET points=points+? WHERE tg_id=?", (int(value), target))
            _panel_quote(chat_id, "POINTS UPDATED", f"User {target}: {value} points adjustment.")
        elif step == "premium":
            days = int(value) if value.isdigit() else 0
            if days <= 0:
                _panel_quote(chat_id, "REJECTED", "Format: USER_ID DAYS")
                return
            until = (_datetime.now(_timezone.utc) + __import__("datetime").timedelta(days=days)).isoformat()
            with _db() as con:
                con.execute("UPDATE panel_users SET is_premium=1,premium_until=? WHERE tg_id=?", (until, target))
            _panel_quote(chat_id, "PREMIUM ACTIVATED", f"User {target} premium for {days} days.")
        return

    # Main menu buttons
    if text_in == "🤖 Add Bot Token":
        _panel_begin_token(chat_id, tg_id)
    elif text_in == "🗂️ My Bots":
        with _db() as con:
            rows = con.execute(
                "SELECT id,username,first_name FROM panel_token_requests WHERE tg_id=? AND status='approved' ORDER BY id DESC",
                (tg_id,),
            ).fetchall()
        body = "\\n".join(
            [f"{i+1}. @{r['username']} — {r['first_name']} (request #{r['id']})" for i, r in enumerate(rows)]
        ) or "No approved bots yet."
        _panel_quote(chat_id, "MY BOTS", body)
    elif text_in in ("✏️ Change Name", "📝 Change Description", "🖼️ Change Picture"):
        with _db() as con:
            rows = con.execute(
                "SELECT id,username FROM panel_token_requests WHERE tg_id=? AND status='approved' ORDER BY id DESC",
                (tg_id,),
            ).fetchall()
        if not rows:
            _panel_quote(chat_id, "NO APPROVED BOTS", "Submit a bot token and wait for admin approval.")
            return
        body = "\\n".join([f"{i+1}. @{r['username']}" for i, r in enumerate(rows)])
        _panel_quote(chat_id, "SELECT YOUR BOT", body + "\\nSend its number.")
        mode = {"✏️ Change Name": "edit_name", "📝 Change Description": "edit_description",
                "🖼️ Change Picture": "photo_bot"}[text_in]
        _PANEL_STATES[tg_id] = {"step": "choose_edit_bot", "mode": mode,
                                "ids": [r["id"] for r in rows]}
    elif text_in == "👤 User Hub":
        user_row, usage, approved = _panel_stats(tg_id)
        _panel_quote(chat_id, "USER HUB",
            f"ID: {tg_id}\nPoints: {user_row['points']}\nPremium: {'Active' if user_row['is_premium'] else 'Inactive'}\nApproved bots: {approved}")
    elif text_in == "📊 Token Usage":
        _, usage, _ = _panel_stats(tg_id)
        _panel_quote(chat_id, "TOKEN USAGE",
            f"Submitted: {usage['tokens_submitted']}\nApproved: {usage['approved']}\nRejected: {usage['rejected']}\nPending: {usage['tokens_submitted']-usage['approved']-usage['rejected']}")
    elif text_in == "🔗 Referrals":
        me = _panel_api(os.getenv("MANAGER_BOT_TOKEN", ""), "getMe")
        username = me.get("result", {}).get("username", "your_bot")
        with _db() as con:
            count = con.execute("SELECT COUNT(*) FROM panel_users WHERE referred_by=?", (tg_id,)).fetchone()[0]
        _panel_quote(chat_id, "REFERRALS", f"Your link:\nhttps://t.me/{username}?start=ref_{tg_id}\nInvited: {count}\nEarned points: {count}")
    elif text_in == "💎 Premium":
        user_row, _, _ = _panel_stats(tg_id)
        _panel_quote(chat_id, "PREMIUM ACCESS",
            f"Status: {'Active' if user_row['is_premium'] else 'Not active'}\nContact support to request premium access.")
    elif text_in in ("✅ Successful", "❌ Rejected"):
        status = "approved" if text_in == "✅ Successful" else "rejected"
        with _db() as con:
            rows = con.execute(
                "SELECT username,created_at FROM panel_token_requests WHERE tg_id=? AND status=? ORDER BY id DESC LIMIT 10",
                (tg_id, status),
            ).fetchall()
        lines = [f"@{r['username']} — {r['created_at']}" for r in rows] or ["No records yet."]
        _panel_quote(chat_id, "SUCCESSFUL" if status == "approved" else "REJECTED", "\n".join(lines))
    elif text_in == "🆘 Support":
        _PANEL_STATES[tg_id] = {"step": "support"}
        _panel_quote(chat_id, "SUPPORT", "Send your issue in one message.")
    elif text_in == "ℹ️ Help":
        _panel_quote(chat_id, "HELP",
            "Add Bot Token: submit a bot you own; admin approval is required.\n"
            "User Hub: view points and premium status.\nToken Usage: see submitted/approved/rejected counts.\n"
            "Referrals: share your personal invite link.\nSupport: create a ticket.")
    elif text_in == "📡 Live Connect" and is_admin:
        _panel_quote(chat_id, "LIVE CONNECT",
            f"Panel bot: online\nPolling: active\nRegistered users: {_panel_count('panel_users')}\nPending token requests: {_panel_count('panel_token_requests', 'status=\'pending\'')}")
    elif text_in == "📢 Broadcast" and is_admin:
        _PANEL_STATES[tg_id] = {"step": "broadcast"}
        _panel_quote(chat_id, "BROADCAST", "Send the announcement text to broadcast to registered panel users.")
    elif text_in == "⚙️ System Manager" and is_admin:
        _panel_quote(chat_id, "SYSTEM MANAGER",
            f"Database: connected\nEncryption: {'ready' if _Fernet else 'missing'}\nPython: {sys.version.split()[0]}\nForce join: {_panel_setting('force_join', os.getenv('FORCE_JOIN_CHAT','') or 'off')}")
    elif text_in == "🖼️ Media Manager" and is_admin:
        _panel_quote(chat_id, "MEDIA MANAGER", "Send a photo or video with caption to save it as the welcome media, or send /clearmedia.")
    elif text_in == "➕ Add Admin" and is_admin:
        _PANEL_STATES[tg_id] = {"step": "new_admin"}
        _panel_quote(chat_id, "ADD ADMIN", "Send the new admin's numeric Telegram user ID.")
    elif text_in == "⭐ Add Points" and is_admin:
        _PANEL_STATES[tg_id] = {"step": "points"}
        _panel_quote(chat_id, "ADD POINTS", "Send: USER_ID POINTS (negative values subtract points).")
    elif text_in == "📣 Force Join" and is_admin:
        _PANEL_STATES[tg_id] = {"step": "force_join"}
        _panel_quote(chat_id, "FORCE JOIN", "Send a channel username such as @yourchannel, or 'off' to disable.")
    elif text_in == "💎 Premium Access" and is_admin:
        _PANEL_STATES[tg_id] = {"step": "premium"}
        _panel_quote(chat_id, "PREMIUM ACCESS", "Send: USER_ID DAYS")
    elif text_in == "📥 Pending Tokens" and is_admin:
        with _db() as con:
            rows = con.execute(
                "SELECT id,tg_id,username,created_at FROM panel_token_requests WHERE status='pending' ORDER BY id LIMIT 20"
            ).fetchall()
        body = "\n".join([f"#{r['id']} @{r['username']} — user {r['tg_id']} — {r['created_at']}" for r in rows]) or "No pending requests."
        body += "\n\nTo approve/reject, send /approve ID or /reject ID."
        _panel_quote(chat_id, "PENDING TOKENS", body)
    elif text_in == "📈 Statistics" and is_admin:
        _panel_quote(chat_id, "STATISTICS",
            f"Users: {_panel_count('panel_users')}\nToken submissions: {_panel_count('panel_token_requests')}\nApproved: {_panel_count('panel_token_requests', 'status=\'approved\'')}\nRejected: {_panel_count('panel_token_requests', 'status=\'rejected\'')}\nSupport tickets: {_panel_count('panel_support')}")
    else:
        if text_in.startswith("/approve ") or text_in.startswith("/reject "):
            if not is_admin:
                _panel_quote(chat_id, "ACCESS DENIED", "Admin permission required.")
                return
            action, request_id = text_in.split(maxsplit=1)
            _panel_review_token(chat_id, tg_id, request_id, action[1:])
        elif text_in == "/cancel":
            _PANEL_STATES.pop(tg_id, None)
            _panel_user_menu(chat_id)
        elif text_in == "/clearmedia" and is_admin:
            _panel_set_setting("welcome_media", "")
            _panel_quote(chat_id, "MEDIA CLEARED", "Welcome media removed.")
        else:
            _panel_quote(chat_id, "NOT RECOGNIZED", "Choose a feature from the keyboard.")


def _panel_count(table, where="1=1"):
    allowed = {"panel_users", "panel_token_requests", "panel_support"}
    if table not in allowed:
        return 0
    with _db() as con:
        return con.execute(f"SELECT COUNT(*) FROM {table} WHERE {where}").fetchone()[0]


def _panel_review_token(chat_id, reviewer, request_id, action):
    if not request_id.isdigit() or action not in ("approve", "reject"):
        _panel_quote(chat_id, "INVALID REQUEST", "Use /approve ID or /reject ID.")
        return
    with _db() as con:
        row = con.execute(
            "SELECT * FROM panel_token_requests WHERE id=? AND status='pending'",
            (int(request_id),),
        ).fetchone()
        if not row:
            _panel_quote(chat_id, "NOT FOUND", "No pending request with that ID.")
            return
        status = "approved" if action == "approve" else "rejected"
        con.execute(
            "UPDATE panel_token_requests SET status=?,reviewed_at=?,reviewed_by=? WHERE id=?",
            (status, _now(), reviewer, int(request_id)),
        )
        if status == "approved":
            con.execute(
                """INSERT OR IGNORE INTO bots(bot_id,username,first_name,token_ciphertext,added_by,created_at)
                   VALUES(?,?,?,?,?,?)""",
                (row["bot_id"], row["username"], row["first_name"], row["token_ciphertext"],
                 f"telegram:{row['tg_id']}", _now()),
            )
            # Ownership is tracked in panel_token_requests.tg_id; the console
            # operator assignment table is intentionally not used for Telegram IDs.
        con.execute(
            f"UPDATE panel_usage SET {status}= {status}+1 WHERE tg_id=?", (row["tg_id"],)
        )
    _panel_quote(chat_id, status.upper(), f"Request #{request_id} for @{row['username']} marked {status}.")
    _panel_send(row["tg_id"], f"<blockquote><b>TOKEN REQUEST {status.upper()}</b>\n@{_html.escape(row['username'])}</blockquote>",
                _PANEL_BUTTONS["user"])


def _panel_handle_update(update):
    if update.get("message"):
        message = update["message"]
        user = message.get("from", {})
        tg_id = int(user.get("id", 0))
        current_state = _PANEL_STATES.get(tg_id, {})
        if message.get("photo") and current_state.get("step") == "photo_upload":
            request_id = current_state.get("bot_id")
            with _db() as con:
                row = con.execute(
                    "SELECT * FROM panel_token_requests WHERE id=? AND tg_id=? AND status='approved'",
                    (request_id, tg_id),
                ).fetchone()
            if not row:
                _PANEL_STATES.pop(tg_id, None)
                _panel_quote(message["chat"]["id"], "BOT NOT FOUND", "No approved bot selected.")
                return
            cipher = _get_cipher()
            bot_token = cipher.decrypt(row["token_ciphertext"]).decode()
            manager_token = os.getenv("MANAGER_BOT_TOKEN", "")
            file_id = message["photo"][-1]["file_id"]
            meta = _panel_api(manager_token, "getFile", {"file_id": file_id})
            if not meta.get("ok"):
                _panel_quote(message["chat"]["id"], "UPLOAD REJECTED", "Could not retrieve that photo.")
                return
            file_path = meta["result"]["file_path"]
            download = requests.get(
                f"https://api.telegram.org/file/bot{manager_token}/{file_path}", timeout=45
            )
            temp_path = Path(f"panel_photo_{tg_id}.jpg")
            temp_path.write_bytes(download.content)
            result = set_photo(bot_token, str(temp_path))
            try:
                temp_path.unlink(missing_ok=True)
            except Exception:
                pass
            _PANEL_STATES.pop(tg_id, None)
            _panel_quote(message["chat"]["id"],
                         "UPDATE SUCCESSFUL" if result.get("ok") else "UPDATE REJECTED",
                         f"@{row['username']}: {result.get('description', 'Profile photo updated' if result.get('ok') else 'Telegram rejected the photo')}")
            return
        if message.get("photo") or message.get("video"):
            if _panel_is_admin(tg_id):
                file_obj = message.get("photo", [{}])[-1] if message.get("photo") else message.get("video")
                file_id = file_obj.get("file_id", "")
                kind = "photo" if message.get("photo") else "video"
                _panel_set_setting("welcome_media", f"{kind}:{file_id}")
                _panel_quote(message["chat"]["id"], "MEDIA SAVED", "Welcome media stored as Telegram file_id.")
            return
        _panel_handle_text(message)


def _panel_run():
    token = os.getenv("MANAGER_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Set MANAGER_BOT_TOKEN to the token of your panel bot.")
    me = _panel_api(token, "getMe")
    if not me.get("ok"):
        raise RuntimeError(f"Panel bot token rejected: {me.get('description')}")
    _panel_init()
    print(f"Telegram panel online: @{me['result'].get('username')}")
    offset = 0
    while True:
        try:
            response = _panel_api(token, "getUpdates", {
                "offset": offset, "timeout": _PANEL_POLL_TIMEOUT,
                "allowed_updates": ["message"],
            })
            if not response.get("ok"):
                time.sleep(3)
                continue
            for update in response.get("result", []):
                offset = max(offset, update["update_id"] + 1)
                try:
                    _panel_handle_update(update)
                except Exception as exc:
                    print(f"Panel update error: {type(exc).__name__}: {exc}")
        except KeyboardInterrupt:
            print("\nTelegram panel stopped.")
            break
        except Exception as exc:
            print(f"Polling error: {type(exc).__name__}: {exc}")
            time.sleep(3)


# Keep the old local dashboard available as a fallback when no panel token is set.
_legacy_console_main = main

def main():
    if os.getenv("MANAGER_BOT_TOKEN", "").strip():
        _panel_run()
    else:
        print("MANAGER_BOT_TOKEN not set; opening the original local dashboard.")
        _legacy_console_main()



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}💀 Interrupted!{N}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{R}❌ Error: {e}{N}")
        sys.exit(0)