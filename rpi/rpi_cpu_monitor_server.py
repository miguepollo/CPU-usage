import psutil
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/cpu_usage')
def get_cpu_usage():
    # Get the current CPU usage percentage
    cpu_usage = psutil.cpu_percent(interval=1)
    return jsonify({'cpu_usage': cpu_usage})

if __name__ == '__main__':
    # Run the server on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000)
