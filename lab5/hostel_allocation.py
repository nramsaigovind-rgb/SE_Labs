
"""Hostel room allocation and room lookup application."""

import os
import secrets

import yaml
from flask import Flask, request
from markupsafe import escape

# Global hostel state
rooms = {}
allocations = {}
waitlist = []
app = Flask(__name__)

CONFIG = """
blocks:
  A: {gender: M, rooms: 3, capacity: 2, fee: 4000}
  B: {gender: F, rooms: 2, capacity: 3, fee: 3500}
"""


def load_config(text=CONFIG):
    """Load the hostel configuration and initialize rooms."""
    config = yaml.safe_load(text)

    for block, info in config["blocks"].items():
        for number in range(1, info["rooms"] + 1):
            room_no = block + str(number)
            rooms[room_no] = {
                "gender": info["gender"],
                "capacity": info["capacity"],
                "fee": info["fee"],
                "occupants": [],
            }

    return config


def allocate_room(student_id, name, gender, year, preferred=None):
    """Allocate a suitable room to a student."""
    if not isinstance(year, int) or isinstance(year, bool):
        return None

    if student_id in allocations:
        return allocations[student_id]["room"]

    preferred = [] if preferred is None else preferred
    candidates = list(dict.fromkeys(preferred + list(rooms.keys())))

    for room_no in candidates:
        room = rooms.get(room_no)

        if room is None or room["gender"] != gender:
            continue

        if len(room["occupants"]) >= room["capacity"]:
            continue

        room["occupants"].append(student_id)
        allocations[student_id] = {
            "name": name,
            "room": room_no,
            "year": year,
        }
        return room_no

    if student_id not in waitlist:
        waitlist.append(student_id)

    return None


def vacate_room(student_id):
    """Remove a student from their room and allocation records."""
    allocation = allocations.pop(student_id, None)

    if allocation is None:
        return

    room = rooms.get(allocation["room"])

    if room is not None and student_id in room["occupants"]:
        room["occupants"].remove(student_id)

    if student_id in waitlist:
        waitlist.remove(student_id)


def monthly_fee(student_id, days_stayed):
    """Calculate the fee for complete 30-day periods."""
    room_no = allocations[student_id]["room"]
    room = rooms[room_no]
    months = days_stayed // 30

    return months * room["fee"]


def priority_order(students):
    """Sort students by seniority, with the highest year first."""
    return sorted(
        students,
        key=lambda student: student["year"],
        reverse=True,
    )


def room_lottery(student_ids):
    """Return student IDs in a cryptographically secure random order."""
    return secrets.SystemRandom().sample(
        student_ids, len(student_ids)
    )


def vacant_beds():
    """Count available beds across all rooms."""
    return sum(
        room["capacity"] - len(room["occupants"])
        for room in rooms.values()
    )


def connect_warden_db():
    """Create the lab's simulated warden database connection."""
    return sqlite_connect(
        host="localhost",
        user="warden",
        password=os.environ.get("WARDEN_DB_PASSWORD", ""),
    )


def sqlite_connect(host, user, password):
    """Simulate a database connection without exposing its password."""
    return {
        "host": host,
        "user": user,
        "connected": bool(password),
    }


def start_remote_log_config():
    """Prevent use of an unauthenticated remote logging listener."""
    raise RuntimeError(
        "Remote logging configuration is disabled for security."
    )


@app.route("/room")
def room_lookup():
    """Return the room allocation for the requested student ID."""
    student_id = request.args.get("id", "")
    allocation = allocations.get(student_id)

    if allocation is None:
        return "<h1>No room allocation found</h1>", 404

    return (
        f"<h1>Room for {escape(student_id)}: "
        f"{escape(allocation['room'])}</h1>"
    )


def run_portal():
    """Run the Flask portal without the interactive debugger."""
    app.run(debug=False)


def main():
    """Demonstrate hostel room allocation operations."""
    load_config()

    print("Rooms:", list(rooms.keys()))
    print("S1 ->", allocate_room("S1", "Arjun", "M", 1))
    print("S2 ->", allocate_room("S2", "Kabir", "M", 2))
    print("S3 ->", allocate_room("S3", "Rohan", "M", 3))
    print("S4 (female) ->", allocate_room("S4", "Diya", "F", 1))
    print("S1 again ->", allocate_room("S1", "Arjun", "M", 1))
    print("S5 year '2' ->", allocate_room("S5", "Vikram", "M", "2"))
    print("Occupants of A1:", rooms["A1"]["occupants"])

    vacate_room("S2")
    print("Occupants of A1 after S2 left:", rooms["A1"]["occupants"])
    print("Fee for S1, 45 days:", monthly_fee("S1", 45))
    print(
        "Priority (seniors first?):",
        [
            student["year"]
            for student in priority_order(
                [{"year": 1}, {"year": 4}, {"year": 2}]
            )
        ],
    )
    print("Lottery:", room_lottery(["S6", "S7", "S8"]))
    print("Vacant beds:", vacant_beds())
    print("Warden DB:", connect_warden_db())
    print("Waitlist:", waitlist)


if __name__ == "__main__":
    main()
