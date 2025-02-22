import requests
import tkinter as tk
import threading
import time

class CPUMonitorApp:
    def __init__(self, raspberry_pi_ip):
        self.raspberry_pi_ip = raspberry_pi_ip
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Raspberry Pi CPU Monitor")
        self.root.geometry("300x200")
        
        # CPU Usage Label
        self.cpu_label = tk.Label(self.root, text="CPU Usage: ---%", font=("Arial", 16))
        self.cpu_label.pack(expand=True)
        
        # Start monitoring thread
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.update_cpu_usage)
        self.monitor_thread.start()
        
        # Setup close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def update_cpu_usage(self):
        while self.monitoring:
            try:
                # Fetch CPU usage from Raspberry Pi
                response = requests.get(f'http://{self.raspberry_pi_ip}:5000/cpu_usage', timeout=5)
                if response.status_code == 200:
                    cpu_usage = response.json()['cpu_usage']
                    # Update label in main thread
                    self.root.after(0, self.update_label, cpu_usage)
            except Exception as e:
                print(f"Error fetching CPU usage: {e}")
            
            # Wait for 2 seconds before next update
            time.sleep(2)
    
    def update_label(self, cpu_usage):
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
    
    def on_closing(self):
        # Stop monitoring thread
        self.monitoring = False
        self.monitor_thread.join()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

# Replace with your Raspberry Pi's IP address
if __name__ == '__main__':
    app = CPUMonitorApp('192.168.1.100')  # Change this to your Raspberry Pi's IP
    app.run()
