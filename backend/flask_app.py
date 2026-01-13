from flask import Flask, request, jsonify, render_template_string
import datetime

app = Flask(__name__)

# --- BAGIAN 1: TAMPILAN DASHBOARD (HTML & JAVASCRIPT) ---
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>IoT Dashboard Final</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: sans-serif; padding: 20px; background: #f0f2f5; }
        .card { background: white; padding: 20px; margin: 10px auto; max-width: 800px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .status { padding: 10px; color: white; font-weight: bold; text-align: center; border-radius: 4px; }
        .normal { background: #28a745; } .warning { background: #ffc107; color: black; } .critical { background: #dc3545; }
    </style>
</head>
<body>
    <div class="card">
        <h2 style="text-align:center;">Smart Lab Monitor</h2>
        <div id="statusBox" class="status normal">MENUNGGU DATA...</div>
        <canvas id="myChart"></canvas>
    </div>

    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: { 
                labels: [], 
                datasets: [{ label: 'Suhu (°C)', data: [], borderColor: '#007bff', fill: false }] 
            }
        });

        async function updateData() {
            try {
                const response = await fetch('/api/data_list');
                const data = await response.json();
                
                if (data.length > 0) {
                    const latest = data[data.length - 1]; // Data terbaru
                    const history = data.slice(-20);      // 20 Data terakhir

                    // Update Status
                    const box = document.getElementById('statusBox');
                    box.innerText = "STATUS: " + latest.prediction + " (" + latest.temperature + "°C)";
                    box.className = 'status ' + (latest.prediction === 'NORMAL' ? 'normal' : latest.prediction.includes('CRITICAL') ? 'critical' : 'warning');

                    // Update Grafik
                    chart.data.labels = history.map(d => new Date(d.timestamp).toLocaleTimeString());
                    chart.data.datasets[0].data = history.map(d => d.temperature);
                    chart.update();
                }
            } catch(e) { console.log(e); }
        }
        setInterval(updateData, 3000); // Update tiap 3 detik
    </script>
</body>
</html>
"""

# --- BAGIAN 2: LOGIKA SERVER & AI ---
data_store = [] # Penyimpanan sementara

def ai_check(temp):
    try: t = float(temp)
    except: return "ERROR"
    
    if t >= 35.0: return "CRITICAL OVERHEAT"
    elif t >= 30.0: return "WARNING HIGH"
    elif t < 20.0: return "WARNING LOW"
    else: return "NORMAL"

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/data', methods=['POST'])
def receive():
    json_data = request.json
    temp = json_data.get('temperature', 0)
    status = ai_check(temp)
    
    data_store.append({
        'timestamp': datetime.datetime.now().isoformat(),
        'temperature': temp,
        'prediction': status
    })
    
    # Simpan max 50 data agar server tidak berat
    if len(data_store) > 50: data_store.pop(0)
    
    return jsonify({"status": "saved", "ai": status}), 200

@app.route('/api/data_list', methods=['GET'])
def get_list():
    return jsonify(data_store)
"""
PENTING: JANGAN jalankan app.run() di sini jika di PythonAnywhere.
Kode di bawah hanya untuk testing di laptop lokal.
"""
if __name__ == '__main__':
    app.run(debug=True)