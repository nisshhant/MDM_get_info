import time
import requests
import subprocess

API_URL = "http://localhost:7188/Command"  # Change to your server address if needed

while True:
    try:
        # Step 1: Get the latest command from server
        response = requests.get(f"{API_URL}/get")
        command = response.json().get("command", "")
        
        if command:
            print(f"Running command: {command}")
            
            # Step 2: Run the command
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                output = e.output

            # Step 3: Send result back to server
            requests.post(f"{API_URL}/result", json={"command": output})
        
        time.sleep(3)
    except Exception as e:
        print("Error:", e)
        time.sleep(5)
