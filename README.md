# 🖥️ Automated System Monitoring and Reporting

A lightweight, Python-based system monitoring solution that periodically collects system metrics, stores them in a local database, sends real-time alerts, and displays interactive visualizations via a desktop dashboard.

---

## 🚀 Key Features

### ✅ Automated Metric Collection  
Tracks CPU usage, memory (RAM), and battery status using `psutil`.

### 🕒 Time-Series Logging  
Efficiently stores metrics in an SQLite database with timestamps.

### ⚠️ Real-Time Alerts  
Sends email notifications when thresholds are breached.

### 📉 Interactive Desktop Dashboard  
Displays system performance metrics using `PyQt5` and `Matplotlib`.

### 🔁 Automated Execution via Jenkins  
Runs the monitoring script every 2–5 minutes.

### 📈 Charting and Trend Analysis  
Includes line and stacked area charts for visualizing performance trends.

### 🧪 Testable Architecture  
Designed with unit testing in mind (`pytest` or `unittest`).

---

## 📊 Dashboard Visualizations

| **Chart**                  | **Description**                                             |
|---------------------------|-------------------------------------------------------------|
| System Metrics (Hourly)   | Line chart showing CPU and RAM usage over recent hours      |
| System Metrics (Daily)    | Line chart capturing full-day system performance trends     |
| CPU Time (Stacked Area)   | Breakdown of idle, user, and system CPU time                |
| RAM Usage (Stacked Area)  | Memory usage divided into used vs. available over time      |

---

## 🧩 System Components

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
