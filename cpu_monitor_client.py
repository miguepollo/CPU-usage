import requests
import tkinter as tk
from tkinter import ttk
import threading
import time

class CPUMonitorApp:
    def __init__(self, raspberry_pi_ip):
        self.raspberry_pi_ip = raspberry_pi_ip
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Raspberry Pi System Monitor")
        self.root.geometry("400x300")
        self.root.configure(bg='#2c3e50')
        
        # Create a frame for system info
        self.frame = ttk.Frame(self.root, style='TFrame')
        self.frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#2c3e50')
        style.configure('TLabel', 
                        foreground='white', 
                        background='#2c3e50', 
                        font=('Arial', 12))
        style.configure('Title.TLabel', 
                        font=('Arial', 16, 'bold'))
        
        # Title
        title = ttk.Label(self.frame, text="Raspberry Pi Monitor", style='Title.TLabel')
        title.pack(pady=(0, 20))
        
        # CPU Usage
        self.cpu_label = ttk.Label(self.frame, text="CPU Usage: ---%", style='TLabel')
        self.cpu_label.pack(pady=5)
        
        # Memory Usage
        self.memory_label = ttk.Label(self.frame, text="Memory Usage: ---%", style='TLabel')
        self.memory_label.pack(pady=5)
        
        # CPU Temperature
        self.temp_label = ttk.Label(self.frame, text="CPU Temperature: ---°C", style='TLabel')
        self.temp_label.pack(pady=5)
        
        # Progress Bars
        self.cpu_progress = ttk.Progressbar(self.frame, length=300, mode='determinate')
        self.cpu_progress.pack(pady=5)
        
        self.memory_progress = ttk.Progressbar(self.frame, length=300, mode='determinate')
        self.memory_progress.pack(pady=5)
        
        # Start monitoring thread
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.update_system_info)
        self.monitor_thread.start()
        
        # Setup close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def update_system_info(self):
        while self.monitoring:
            try:
                # Fetch system info from Raspberry Pi
                response = requests.get(f'http://{self.raspberry_pi_ip}:5000/system_info', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Update labels in main thread
                    self.root.after(0, self.update_labels, 
                                    data['cpu_usage'], 
                                    data['memory_usage'], 
                                    data.get('cpu_temp'))
            except Exception as e:
                print(f"Error fetching system info: {e}")
            
            # Wait for 2 seconds before next update
            time.sleep(2)
    
    def update_labels(self, cpu_usage, memory_usage, cpu_temp):
        # Update CPU Usage
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        self.cpu_progress['value'] = cpu_usage
        
        # Update Memory Usage
        self.memory_label.config(text=f"Memory Usage: {memory_usage}%")
        self.memory_progress['value'] = memory_usage
        
        # Update CPU Temperature
        temp_text = f"CPU Temperature: {cpu_temp}°C" if cpu_temp is not None else "CPU Temperature: N/A"
        self.temp_label.config(text=temp_text)
    
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
