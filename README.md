# Automated System Monitoring and Reporting

A lightweight, Python-based system monitoring solution that periodically collects system metrics, stores them in a local database, sends real-time alerts, and displays interactive visualizations via a desktop dashboard.

---

## Key Features

### Automated Metric Collection  
Tracks CPU usage, memory (RAM), and battery status using `psutil`.

### Time-Series Logging  
Efficiently stores metrics in an SQLite database with timestamps.

### Real-Time Alerts  
Sends email notifications when thresholds are breached.

### Interactive Desktop Dashboard  
Displays system performance metrics using `PyQt5` and `Matplotlib`.

### Automated Execution via Jenkins  
Runs the monitoring script every 2–5 minutes.

### Charting and Trend Analysis  
Includes line and stacked area charts for visualizing performance trends.

### Testable Architecture  
Designed with unit testing in mind (`pytest` or `unittest`).

---

## Dashboard Visualizations

| Chart                    | Description                                                  |
|--------------------------|--------------------------------------------------------------|
| System Metrics (Hourly)  | Line chart showing CPU and RAM usage over recent hours       |
| System Metrics (Daily)   | Line chart capturing full-day system performance trends      |
| CPU Time (Stacked Area)  | Breakdown of idle, user, and system CPU time                 |
| RAM Usage (Stacked Area) | Memory usage divided into used vs. available over time       |

---

## System Components

### 1. Metric Collection  
**Powered by `psutil`**

Collected data includes:

- `cpu_percent`, `cpu_times_user`, `cpu_times_system`, `cpu_times_idle`  
- `sys_mem_total`, `sys_mem_used`, `sys_mem_avail`, `sys_mem_perc`  
- `bat_per`, `charger_plug`, `time_left`

---

### 2. SQLite Database

- Stores collected metrics with accurate timestamps  
- Optimized for time-series queries  

**Sample schema:**
```bash
id, timestamp, cpu_percent, cpu_times_user, cpu_times_system,
cpu_times_idle, sys_mem_total, sys_mem_used, sys_mem_avail,
sys_mem_perc, bat_per, charger_plug, time_left
```

---

### 3. Email Alert System

Alerts are triggered when:

- CPU usage ≥ 90%  
- RAM usage ≥ 90%  
- Battery ≤ 20%  

Uses `smtplib` and `email.message` for sending notifications.

**Example alert:**  
> ⚠️ CPU usage reached 93.6% at 11:08 AM. RAM usage at 87.3%. Battery at 42%. Charging: No

---

### 4. Real-Time Dashboard

- Built using `PyQt5` with embedded `Matplotlib` charts  
- Automatically refreshes every minute to display latest metrics  
- Supports:
  - Line charts (hourly and daily)
  - Stacked area charts (CPU time, RAM usage)

---

## Jenkins Integration

- Jenkins automates periodic execution of the monitoring script  
- Scheduled to run every 2 or 5 minutes  
- Ensures continuous data collection and timely alerts  
- Scalable to support monitoring across multiple systems

---

## Testing

- Designed with testability in mind using `pytest` or `unittest`  
- Future test coverage includes:
  - Metric collection accuracy  
  - Database insertions  
  - Alert conditions and triggers

---

## System Architecture Diagram

```csharp
[Jenkins Scheduler]
        ↓
[Python Monitoring Script]
        ↓
[psutil - Collect Metrics]
        ↓
[SQLite - Log Data] ←────┐
        ↓                │
[Check Thresholds]       │
        ↓                │
[Send Email Alerts]      │
                         ↓
        [Real-Time Dashboard (PyQt5 + Matplotlib)]
                  ↓
        [Query DB Every Minute → Refresh Charts]

```

<img width="404" height="403" alt="flowcharts_project" src="https://github.com/user-attachments/assets/c09a7530-a0a1-446e-a9b5-5f0cdd58cac4" />

---

## Project Structure

```perl
system-monitor/
│
├── main.py             # Metric collection + alert logic
├── dashboard.py        # PyQt5 real-time dashboard
├── database.py         # SQLite data handling
├── alerts.py           # Email alert logic
├── config.ini          # Configurable thresholds and SMTP settings
├── tests/              # Unit tests (to be developed)
│   └── test_metrics.py
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```
---

## Installation
```bash
git clone https://github.com/yourusername/system-monitor.git
cd system-monitor
pip install -r requirements.txt
```

### Edit config.ini to configure:

- Alert thresholds
- SMTP credentials for email

---
## Usage

Start data collection:
```bash
python get_info_insert_db.py
```

Launch the real-time dashboard:
```bash
python dahsboard.py
```
---

## Roadmap & Future Enhancements

- Multi-system monitoring with remote aggregation  
- Web dashboard using Flask/Django + Chart.js  
- Historical data analysis with trend forecasting (ML integration)  
- Cloud storage and export (e.g., to InfluxDB)  
- Integration with Grafana, Prometheus, or log-shipping tools  

---

## psutil vs. Alternatives

| Feature           | psutil | os/subprocess | shutil/platform | GPUtil | CLI Tools |
|------------------|--------|---------------|------------------|--------|-----------|
| Cross-platform    | ✅     | ❌            | ⚠️               | ❌     | ❌        |
| CPU/RAM Usage     | ✅     | ⚠️            | ❌               | ❌     | ✅        |
| Disk/Network I/O  | ✅     | ⚠️            | ⚠️               | ❌     | ✅        |
| Battery Status    | ✅     | ❌            | ❌               | ⚠️     | ⚠️        |
| Pythonic API      | ✅     | ❌            | ⚠️               | ✅     | ❌        |

---

## License

This project is licensed under the **MIT License**.

---

## Contact

For questions, suggestions, or contributions:  
📧 youremail@example.com






















