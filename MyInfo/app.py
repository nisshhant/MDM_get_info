import importlib.util
import subprocess
import sys
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SystemInfoCollector:
    REQUIRED_LIBS = ['psutil', 'requests']

    def __init__(self):
        self.install_missing_packages()
        self.import_modules()

    def install_missing_packages(self):
        for package in self.REQUIRED_LIBS:
            if not self.is_installed(package):
                print(f"[INFO] Installing missing package: {package}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    def is_installed(self, package_name):
        spec = importlib.util.find_spec(package_name)
        return spec is not None

    def import_modules(self):
        global platform, psutil, socket, uuid, os, sys, json, requests
        import platform
        import psutil
        import socket
        import uuid
        import os
        import sys
        import json
        import requests

    def get_system_info(self):
        info = {}

        info['OS'] = platform.system()
        info['OS Version'] = platform.version()
        info['Platform'] = platform.platform()
        info['Machine'] = platform.machine()
        info['Processor'] = platform.processor()
        info['Architecture'] = platform.architecture()[0]

        info['Hostname'] = socket.gethostname()
        info['IP Address'] = socket.gethostbyname(socket.gethostname())

        info['MAC Address'] = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                                        for elements in range(0, 8 * 6, 8)][::-1])

        info['Physical Cores'] = psutil.cpu_count(logical=False)
        info['Total Cores'] = psutil.cpu_count(logical=True)
        info['CPU Usage (%)'] = psutil.cpu_percent(interval=1)

        svmem = psutil.virtual_memory()
        info['Total RAM (GB)'] = round(svmem.total / (1024 ** 3), 2)
        info['Available RAM (GB)'] = round(svmem.available / (1024 ** 3), 2)
        info['RAM Usage (%)'] = svmem.percent

        disk_info = []
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    'Device': partition.device,
                    'Mountpoint': partition.mountpoint,
                    'File System': partition.fstype,
                    'Total Size (GB)': round(usage.total / (1024 ** 3), 2),
                    'Used (GB)': round(usage.used / (1024 ** 3), 2),
                    'Free (GB)': round(usage.free / (1024 ** 3), 2),
                    'Usage (%)': usage.percent
                })
            except PermissionError:
                continue
        info['Disks'] = disk_info

        net_io = psutil.net_io_counters()
        info['Total Bytes Sent'] = net_io.bytes_sent
        info['Total Bytes Received'] = net_io.bytes_recv

        info['Python Version'] = sys.version

        return info

    def run(self):
        print("[INFO] Python client is polling for 'start' command...")
        while True:
            try:
                # Get current command from the server
                response = requests.get("http://192.168.1.133:5555/api/Command", verify=False)
                command = response.json().get("command", "").lower()
                if command == "start":
                    print("[INFO] 'start' command received. Collecting system info...")	
                    
                    info = self.get_system_info()

                    # Send system info to server
                    res = requests.post("http://192.168.1.133:5555/api/SystemInfo",
                                        json=info,
                                        headers={'Content-Type': 'application/json'},
                                        verify=False)
                    
                    print(f"[INFO] System info sent. Server responded with: {res.status_code}")

                    # Reset command to idle
                    reset_response = requests.post("http://192.168.1.133:5555/api/Command",
                                                   json={"cmd": "idle"},
                                                   headers={'Content-Type': 'application/json'},
                                                   verify=False)
                    print(f"[INFO] Command reset. Server response: {reset_response.status_code}")
                    print("[INFO] Returning to polling mode...")

                time.sleep(5)
            except Exception as e:
                print(f"[ERROR] {e}")
                time.sleep(5)

if __name__ == "__main__":
    SystemInfoCollector().run()