import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv('db_path')
app_password = os.getenv("app_password")
from_address = os.getenv("from_address")
to_address = os.getenv("to_address")
server = os.getenv("server")

THRESHOLDS = {
    "max_cpu_percent": 90.0,        # cpu_percent
    "min_battery_percent": 20.0,    # bat_per
    "max_ram_percent": 90.0         # sys_mem_per
}

EMAIL_SETTINGS = {
    "server": server,
    "port": 587,
    # "username": "your_email@example.com",
    "password": app_password,          
    "from": from_address,
    "to": to_address       
}
