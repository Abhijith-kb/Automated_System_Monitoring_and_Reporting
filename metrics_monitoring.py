import sqlite3
from config import db_path, THRESHOLDS
from alert_mailer import send_alert
from datetime import datetime

# This file monitors metrics (via data fetching + alerts).

def alert_check():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = """SELECT cpu_percent, sys_mem_perc, bat_per, timestamp 
            FROM system_metrics 
            ORDER BY timestamp DESC LIMIT 1"""
    cur.execute(query)
    row = cur.fetchone()
    conn.close()

    if row is None:
        print("No metrics found in database!")
        return
    
    cpu_per, sys_mem_perc, bat_per, timestamp = row
    subject_parts = []
    body_parts = [f"Timestamp: {timestamp}\n"]

    # CPU Check
    if cpu_per >= THRESHOLDS["max_cpu_percent"]:
        subject_parts.append("High CPU")
        body_parts.append(f"⚠️ CPU usage is above {THRESHOLDS['max_cpu_percent']}%: {cpu_per}%")
        body_parts.append("\nPossible Issues:")
        body_parts.append("- Too many running processes or background apps")
        body_parts.append("- A program may be stuck or consuming excess resources")
        body_parts.append("- Outdated drivers or heavy workloads")
        body_parts.append("\nSuggestions:")
        body_parts.append("- Close unnecessary programs or browser tabs")
        body_parts.append("- Check Task Manager to identify high-usage processes")
        body_parts.append("- Restart stuck apps or the system if needed")
        body_parts.append("- Keep drivers updated")
        body_parts.append("- Consider hardware upgrade or better cooling if this happens often\n")

    # RAM Check
    if sys_mem_perc >= THRESHOLDS["max_ram_percent"]:
        subject_parts.append("High RAM")
        body_parts.append(f"⚠️ RAM usage is above {THRESHOLDS['max_ram_percent']}%: {sys_mem_perc}%")
        body_parts.append("\nPossible Issues:")
        body_parts.append("- Too many applications or browser tabs open")
        body_parts.append("- Memory leaks from long-running apps")
        body_parts.append("- Insufficient RAM for workload")
        body_parts.append("\nSuggestions:")
        body_parts.append("- Close unused applications")
        body_parts.append("- Restart the system to clear memory leaks")
        body_parts.append("- Disable unnecessary startup programs")
        body_parts.append("- Increase virtual memory (page file) if needed")
        body_parts.append("- Upgrade RAM if this issue is frequent\n")

    # Battery Check
    if bat_per <= THRESHOLDS["min_battery_percent"]:
        subject_parts.append("Low Battery")
        body_parts.append(f"⚠️ Battery is below {THRESHOLDS['min_battery_percent']}%: {bat_per}%")
        body_parts.append("\nPossible Issues:")
        body_parts.append("- Battery draining quickly without charger")
        body_parts.append("- Risk of sudden shutdown and data loss")
        body_parts.append("- Battery wear over time")
        body_parts.append("\nSuggestions:")
        body_parts.append("- Plug in the charger immediately")
        body_parts.append("- Reduce screen brightness and close background apps")
        body_parts.append("- Enable battery saver mode")
        body_parts.append("- Avoid letting battery fully discharge often")
        body_parts.append("- For long-term health, avoid keeping battery at 100% all the time when plugged in\n")

    if subject_parts:
        subject = "System Alert: " + ", ".join(subject_parts)
        # Add general health tips at the end of every mail
        body_parts.append("\n💡 General PC Health Tips:")
        body_parts.append("- Keep your OS and drivers updated")
        body_parts.append("- Run disk cleanup and antivirus scans periodically")
        body_parts.append("- Ensure good ventilation to avoid overheating")
        body_parts.append("- Backup important data regularly\n")
        
        body = "\n".join(body_parts)
        send_alert(subject, body)

# Reusable DB query helper
def execute_query(query, params=None, convert_timestamps=False):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
    
    if convert_timestamps:
        return [(datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"), *row[1:]) for row in rows]
    
    return rows

# 1. Get CPU, Battery, and RAM % (Latest 50 entries, ordered ASC)
def get_percent_data_from_db():
    query = """
        SELECT timestamp, cpu_percent, bat_per, sys_mem_perc
        FROM (
            SELECT timestamp, cpu_percent, bat_per, sys_mem_perc
            FROM system_metrics
            ORDER BY timestamp DESC
            LIMIT 50
        ) AS latest_50
        ORDER BY timestamp;
    """
    return execute_query(query, convert_timestamps=False)

# 2. Get latest CPU time breakdown
def get_cpu_time_distribution():
    query = """
        SELECT cpu_times_system, cpu_times_user, cpu_times_idle
        FROM system_metrics
        ORDER BY timestamp DESC
        LIMIT 1
    """
    row = execute_query(query)
    if row:
        system, user, idle = row[0]
        return {
            "System Mode(Kernel & Drivers)": system,
            "User Mode": user,
            "Idle Mode": idle
        }
    else:
        return {
            "System Mode(Kernel & Drivers)": 0,
            "User Mode": 0,
            "Idle Mode": 0
        }

# 3. Get RAM stats (Latest 50 entries)
def get_ram_data_from_db():
    query = """
        SELECT timestamp, sys_mem_total, sys_mem_used, sys_mem_avail
        FROM (
            SELECT timestamp, sys_mem_total, sys_mem_used, sys_mem_avail
            FROM system_metrics
            ORDER BY timestamp DESC
            LIMIT 50
        ) AS latest_50
        ORDER BY timestamp;
    """
    return execute_query(query, convert_timestamps=True)

# 4. Get CPU time trend (full timeline, with converted timestamps)
def get_cpu_time_trend():
    query = """
        SELECT timestamp, cpu_times_user, cpu_times_system, cpu_times_idle
        FROM system_metrics
        ORDER BY timestamp
    """
    return execute_query(query, convert_timestamps=True)