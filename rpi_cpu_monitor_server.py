import psutil
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/system_info')
def get_system_info():
    # Get CPU usage percentage
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Get memory usage
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    
    # Get CPU temperature (works on Raspberry Pi)
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as temp_file:
            cpu_temp = int(temp_file.read()) / 1000.0  # Convert to Celsius
    except Exception:
        cpu_temp = None
    
    return jsonify({
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'cpu_temp': cpu_temp
    })

if __name__ == '__main__':
    # Run the server on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000)
