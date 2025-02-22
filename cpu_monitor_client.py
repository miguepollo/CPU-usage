import requests
import tkinter as tk
from tkinter import ttk
import threading
import time
import sv_ttk  # Modern tkinter theme library

class CPUMonitorApp:
    def __init__(self, raspberry_pi_ip):
        self.raspberry_pi_ip = raspberry_pi_ip
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Raspberry Pi Monitor")
        self.root.geometry("500x600")
        
        # Use modern theme
        sv_ttk.set_theme("dark")
        
        # Main container with padding
        self.main_container = ttk.Frame(self.root, padding="20 20 20 20")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = ttk.Label(
            self.main_container, 
            text="Raspberry Pi System Monitor", 
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(pady=(0, 30))
        
        # System Info Frames
        self.create_system_info_frames()
        
        # Connection Status
        self.connection_label = ttk.Label(
            self.main_container, 
            text="Conectando...", 
            foreground="yellow"
        )
        self.connection_label.pack(pady=(20, 0))
        
        # Start monitoring thread
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.update_system_info)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        # Setup close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_system_info_frames(self):
        # CPU Frame
        cpu_frame = ttk.LabelFrame(self.main_container, text="CPU", padding="10 10 10 10")
        cpu_frame.pack(fill=tk.X, pady=10)
        
        self.cpu_usage_label = ttk.Label(cpu_frame, text="Uso: 0%", font=("Arial", 12))
        self.cpu_usage_label.pack(pady=(0, 5))
        
        self.cpu_progress = ttk.Progressbar(cpu_frame, length=400, mode='determinate')
        self.cpu_progress.pack(fill=tk.X)
        
        # Memory Frame
        memory_frame = ttk.LabelFrame(self.main_container, text="Memoria", padding="10 10 10 10")
        memory_frame.pack(fill=tk.X, pady=10)
        
        self.memory_usage_label = ttk.Label(memory_frame, text="Uso: 0%", font=("Arial", 12))
        self.memory_usage_label.pack(pady=(0, 5))
        
        self.memory_progress = ttk.Progressbar(memory_frame, length=400, mode='determinate')
        self.memory_progress.pack(fill=tk.X)
        
        # Temperature Frame
        temp_frame = ttk.LabelFrame(self.main_container, text="Temperatura", padding="10 10 10 10")
        temp_frame.pack(fill=tk.X, pady=10)
        
        self.temp_label = ttk.Label(temp_frame, text="Temperatura: N/A", font=("Arial", 12))
        self.temp_label.pack()
        
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
                    
                    # Update connection status
                    self.root.after(0, self.update_connection_status, True)
            except Exception as e:
                # Update connection status on error
                self.root.after(0, self.update_connection_status, False)
                print(f"Error fetching system info: {e}")
            
            # Wait for 2 seconds before next update
            time.sleep(2)
    
    def update_labels(self, cpu_usage, memory_usage, cpu_temp):
        # Update CPU Usage
        self.cpu_usage_label.config(text=f"Uso: {cpu_usage}%")
        self.cpu_progress['value'] = cpu_usage
        
        # Update Memory Usage
        self.memory_usage_label.config(text=f"Uso: {memory_usage}%")
        self.memory_progress['value'] = memory_usage
        
        # Update CPU Temperature
        temp_text = f"Temperatura: {cpu_temp}°C" if cpu_temp is not None else "Temperatura: N/A"
        self.temp_label.config(text=temp_text)
    
    def update_connection_status(self, connected):
        if connected:
            self.connection_label.config(text="Conectado", foreground="green")
        else:
            self.connection_label.config(text="Sin conexión", foreground="red")
    
    def on_closing(self):
        # Stop monitoring thread
        self.monitoring = False
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

# Replace with your Raspberry Pi's IP address
if __name__ == '__main__':
    app = CPUMonitorApp('192.168.1.121')  # Change this to your Raspberry Pi's IP
    app.run()
