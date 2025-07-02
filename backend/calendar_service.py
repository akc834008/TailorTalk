import os
import datetime
import dateparser
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Constants
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/credential.json"))
calendar_id = "akc834008@gmail.com"

# ✅ Load credentials only when needed
def get_credentials():
    return service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

# ✅ Get calendar API service
def get_calendar_service():
    return build("calendar", "v3", credentials=get_credentials())

def is_slot_free(start_dt, end_dt):
    try:
        service = get_calendar_service()
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_dt.isoformat(),
            timeMax=end_dt.isoformat(),
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])
        return len(events) == 0
    except Exception as e:
        print("❌ Error checking availability:", str(e))
        return False

def find_next_available_slot(start_dt, duration_minutes=60, search_hours=6):
    try:
        service = get_calendar_service()
        end_search = start_dt + datetime.timedelta(hours=search_hours)

        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_dt.isoformat(),
            timeMax=end_search.isoformat(),
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])
        events.sort(key=lambda e: e["start"]["dateTime"])

        current = start_dt
        for event in events:
            busy_start = dateparser.parse(event["start"]["dateTime"])
            busy_end = dateparser.parse(event["end"]["dateTime"])

            if (busy_start - current).total_seconds() >= duration_minutes * 60:
                return current
            if busy_end > current:
                current = busy_end

        if (end_search - current).total_seconds() >= duration_minutes * 60:
            return current

        return None
    except Exception as e:
        print("❌ Error finding next free slot:", str(e))
        return None

def suggest_free_slot(date_str: str, duration_minutes: int = 60):
    try:
        start_dt = dateparser.parse(date_str + " 9:00 AM")
        if not start_dt:
            raise ValueError("Could not parse date for suggestion")

        suggestion = find_next_available_slot(start_dt, duration_minutes)
        if suggestion:
            return f"✅ You're free at {suggestion.strftime('%I:%M %p')} on {suggestion.strftime('%A, %d %B %Y')}."
        else:
            return "❌ No available slots found tomorrow within working hours."
    except Exception as e:
        return f"❌ Error suggesting time: {str(e)}"

def create_event(summary: str, date_time_str: str, duration_minutes: int = 60):
    try:
        start_dt = dateparser.parse(date_time_str)
        if not start_dt:
            raise ValueError(f"Could not parse datetime: {date_time_str}")
        end_dt = start_dt + datetime.timedelta(minutes=duration_minutes)

        if not is_slot_free(start_dt, end_dt):
            suggested = find_next_available_slot(start_dt + datetime.timedelta(minutes=1), duration_minutes)
            if suggested:
                return {
                    "success": False,
                    "event_link": f"❌ That time is already booked.\n\n✅ You're free at {suggested.strftime('%I:%M %p')} — want me to book that instead?"
                }
            else:
                return {
                    "success": False,
                    "event_link": f"❌ That time is booked, and no free slots found in the next few hours."
                }

        service = get_calendar_service()
        event = {
            "summary": summary,
            "start": {"dateTime": start_dt.isoformat(), "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end_dt.isoformat(), "timeZone": "Asia/Kolkata"},
        }

        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

        print("✅ Event created:", created_event)
        return {
            "success": True,
            "event_link": created_event.get("htmlLink", "No link returned")
        }

    except Exception as e:
        print("❌ Calendar booking error:", str(e))
        return {
            "success": False,
            "event_link": f"Google Calendar Error: {str(e)}"
        }
