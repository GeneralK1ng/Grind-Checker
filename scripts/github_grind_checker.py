import os
import requests
from datetime import datetime, timedelta, timezone
from collections import defaultdict

usernames = ['GeneralK1ng']
work_start_hour = 10
work_end_hour = 18
lookback_days = 7
github_token = os.getenv("GITHUB_TOKEN")

local_tz = datetime.now().astimezone().tzinfo


def fetch_user_events(username, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    for page in range(1, 8):
        url = f"https://api.github.com/users/{username}/events/public?page={page}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        yield from response.json()


def analyze_user(username):
    hourly_activity = defaultdict(int)
    daily_hour_activity = defaultdict(lambda: defaultdict(int))
    event_type_count = defaultdict(int)
    off_hour_count = 0
    midnight_activity = 0
    weekend_activity = 0
    total_activity = 0
    active_days = set()

    now = datetime.now(local_tz)

    for event in fetch_user_events(username, token=github_token):
        created_at = event.get("created_at")
        if not created_at:
            continue

        utc_time = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        local_time = utc_time.astimezone(local_tz)

        if (now - local_time).days > lookback_days:
            break

        date_str = local_time.strftime("%Y-%m-%d")
        hour = local_time.hour

        active_days.add(date_str)
        hourly_activity[hour] += 1
        daily_hour_activity[date_str][hour] += 1
        event_type_count[event.get("type", "Unknown")] += 1
        total_activity += 1

        if hour < work_start_hour or hour >= work_end_hour:
            off_hour_count += 1
        if hour < 6:
            midnight_activity += 1
        if local_time.weekday() >= 5:
            weekend_activity += 1

    if total_activity == 0:
        return None

    grind_score = off_hour_count / total_activity + 0.1 * weekend_activity + 0.2 * midnight_activity

    return {
        "username": username,
        "off_hour_count": off_hour_count,
        "total_activity": total_activity,
        "hourly_activity": hourly_activity,
        "daily_hour_activity": daily_hour_activity,
        "event_type_count": event_type_count,
        "midnight_activity": midnight_activity,
        "weekend_activity": weekend_activity,
        "grind_score": grind_score,
        "active_days_count": len(active_days),
    }


def write_analysis_to_file(result):
    today = datetime.now(local_tz).strftime("%Y-%m-%d")
    os.makedirs("reports", exist_ok=True)
    with open(f"reports/{today}.md", "w", encoding="utf-8") as f:
        f.write(f"# GitHub Activity Report - {today}\n\n")
        f.write(f"👤 User: {result['username']}\n")
        f.write(f"📊 Total Events: {result['total_activity']} | Off-Hour Events: {result['off_hour_count']}\n")
        f.write(
            f"📅 Active Days: {result['active_days_count']} | Midnight Events: {result['midnight_activity']} | Weekend Events: {result['weekend_activity']}\n")
        f.write(f"🔥 Grind Score: {result['grind_score']:.2f}\n\n")

        f.write("🔧 Event Type Breakdown:\n")
        for k, v in result['event_type_count'].items():
            f.write(f"- {k}: {v}\n")

        f.write("\n⏰ Hourly Activity (Local Time):\n")
        max_count = max(result["hourly_activity"].values()) or 1
        for hour in range(24):
            count = result["hourly_activity"].get(hour, 0)
            bar = '▇' * int(count * 20 / max_count)
            f.write(f"{hour:02d}:00 | {bar} ({count})\n")

        f.write("\n📆 Daily Activity Breakdown:\n")
        for day in sorted(result["daily_hour_activity"]):
            f.write(f"- {day}: ")
            for hour in sorted(result["daily_hour_activity"][day]):
                count = result["daily_hour_activity"][day][hour]
                f.write(f"{hour:02d}h({count}) ")
            f.write("\n")


if __name__ == "__main__":
    for user in usernames:
        try:
            result = analyze_user(user)
            if result:
                write_analysis_to_file(result)
            else:
                print(f"⚠️ No recent activity from {user} in last {lookback_days} days.")
        except Exception as e:
            print(f"❌ Failed to analyze {user}: {e}")