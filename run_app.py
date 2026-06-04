import subprocess
import time
import sys
import os

def launch_application():
    print("==================================================")
    print("Step 1: Launching Weather FastAPI Backend Server...")
    print("==================================================")
    
    server_process = subprocess.Popen([sys.executable, "server.py"])
    
    print("\nWaiting for local server spin-up...")
    time.sleep(3) 
    
    print("\n==================================================")
    print("Step 2: Launching Tkinter Meteorological Dashboard...")
    print("==================================================")
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\nManually interrupting the launcher...")
    finally:
        print("\nClosing background weather server process...")
        server_process.terminate()
        server_process.wait() # İşlemin tamamen sonlandığından emin olur
        print("Application shut down successfully.")

if __name__ == "__main__":
    if os.path.dirname(os.path.abspath(__file__)):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
    launch_application()