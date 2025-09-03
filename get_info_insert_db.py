import psutil
import sqlite3
from config import db_path
from metrics_monitoring import alert_check

def setup_db():
    #print("db path",db_path)
    conn = sqlite3.connect(db_path) 
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS system_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT (datetime('now', 'localtime')),
        cpu_percent REAL,
        cpu_times_user REAL,
        cpu_times_system REAL,
        cpu_times_idle REAL,
        sys_mem_total REAL,
        sys_mem_avail REAL,
        sys_mem_perc REAL,
        sys_mem_used REAL,
        bat_per REAL,
        charger_plug INTEGER,
        time_left INTEGER
    );''')
    conn.commit()
    conn.close()

def cpu_data():
    #cpu_cores = psutil.cpu_count() # number of logical CPUs (including hyperthreaded cores) (number of cores)
    #cpu_phy_cores = psutil.cpu_count(logical=False) # number of physical cores
    cpu_percent = psutil.cpu_percent(interval=1) # returns CPU utilization as a percentage averaged over interval of 1 second.
    cpu_percent_pre = psutil.cpu_percent(interval=1, percpu=True)   # Pre-core Usage
    
    cpu_times = psutil.cpu_times()              # Returns a named tuple with fields that represent the amount of time the CPU has spent in each state(in secs).
    cpu_times_user = cpu_times.user             # Time spent in user mode.
    cpu_times_system = cpu_times.system         # Time spent in system mode (kernel processes and drivers).
    cpu_times_idle = cpu_times.idle             # Time CPU was idle
    cpu_times_interrupt = cpu_times.interrupt   # Time spent handling hardware interrupts.
    cpu_times_dpc = cpu_times.dpc               # Time spent handling Deferred Procedure Calls (DPCs).(DPCs are low-priority tasks queued by hardware interrupts.)

    cpu_freq = psutil.cpu_freq()                # Current CPU frequency: current, min, max in MHz.
    cpu_freq_cur = cpu_freq.current
    cpu_freq_max = cpu_freq.max
    cpu_freq_min = cpu_freq.min
    
    return cpu_percent, cpu_times_user, cpu_times_system, cpu_times_idle

def virtual_memory_data ():
    sys_mem = psutil.virtual_memory()   # system memory usage in bytes
    # print(sys_mem)
    sys_mem_total = sys_mem.total       # total physical memory excluding swap in bytes. divide by (1024*1024) to get in mbs
    sys_mem_avail = sys_mem.available   # memory that can be given instantly to processes without the system going into swap. This includes free memory and memory used for disk caching that can be repurposed.
    sys_mem_perc = sys_mem.percent      # Calculated as: percent = (total - available) / total * 100. Represents the percentage of memory in use.
    sys_mem_used = sys_mem.used         # Memory that is currently being used. On Windows, this is calculated as: used = total - available. ⚠️ It's not total - free because of how Windows caches memory.
    sys_mem_free = sys_mem.free         # Memory that is completely unallocated. This is often low on Windows due to aggressive caching in "standby" memory.
    return sys_mem_total, sys_mem_avail, sys_mem_perc, sys_mem_used

def battery_data():
    battery = psutil.sensors_battery()
    bat_per = battery.percent               # Battery charge percentage (0–100).
    charger_plug = battery.power_plugged    # True if the device is plugged in (charging or full), False if running on battery.
    time_left = abs(battery.secsleft)       # Estimated seconds left before full discharge or full charge, depending on whether the laptop is plugged in. May be psutil.POWER_TIME_UNLIMITED, psutil.POWER_TIME_UNKNOWN, or an integer (in seconds).
    return bat_per, charger_plug, time_left

def insert_metrics(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute('''
        INSERT INTO system_metrics (
            cpu_percent,
            cpu_times_user,
            cpu_times_system,
            cpu_times_idle,
            sys_mem_total,
            sys_mem_avail,
            sys_mem_perc,
            sys_mem_used,
            bat_per,
            charger_plug,
            time_left
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    
    conn.commit()
    conn.close()



if __name__ == '__main__':
    setup_db()
    data = []
    # cpu_percent, cpu_times_user, cpu_times_system, cpu_times_idle, cpu_freq_cur, cpu_freq_max, cpu_freq_min = cpu_data() # 7
    data.extend(cpu_data())
    # sys_mem_total, sys_mem_avail, sys_mem_perc, sys_mem_used, sys_mem_free = virtual_memory_data()  # 5
    data.extend(virtual_memory_data())
    # bat_per, charger_plug, time_left = battery_data() # 3
    data.extend(battery_data())
    insert_metrics(data)
    alert_check()
    # print("Data inserted into DB")