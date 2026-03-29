from flask import Flask, request, render_template_string
import subprocess
import threading

app = Flask(__name__)

# A Professional-looking Server Management Dashboard
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Cloud Management Console</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; }
        .navbar { background: #1a237e; color: white; padding: 15px 30px; margin-bottom: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .container { max-width: 900px; margin: auto; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        h2 { color: #1a237e; margin-top: 0; }
        .status-up { color: #2ecc71; font-weight: bold; }
        .btn-action { background: #d32f2f; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; transition: 0.3s; }
        .btn-action:hover { background: #b71c1c; }
        .logs { background: #263238; color: #cfd8dc; padding: 15px; border-radius: 6px; font-family: monospace; height: 100px; overflow-y: auto; font-size: 13px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="navbar">
            <h1 style="margin:0;">Infrastructure Manager v2.0</h1>
        </div>

        <div class="grid">
            <div class="card">
                <h2>Local Node Status</h2>
                <p>Hostname: <strong>eshani-server</strong></p>
                <p>Status: <span class="status-up">● ACTIVE</span></p>
                <p>Location: VMware Workstation (NAT)</p>
                <hr>
                <p><strong>System Maintenance:</strong></p>
                <form action="/stress" method="post">
                    <button class="btn-action" type="submit">Execute Stress Simulation</button>
                </form>
            </div>

            <div class="card">
                <h2>Cloud Burst Status</h2>
                <p>Provider: Google Cloud Platform</p>
                <p>Region: us-central1</p>
                <div class="logs" id="log-box">
                    > System monitoring active...<br>
                    > Waiting for Prometheus trigger...
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/stress', methods=['POST'])
def run_stress():
    # This triggers the actual 'stress' tool on your system
    print("🔥 Manual Stress Test Initiated via Dashboard...")
    threading.Thread(target=lambda: subprocess.run(["stress", "--cpu", "4", "--timeout", "40"])).start()
    return "<h1>Stress Test Running</h1><p>The 'stress' tool is now consuming 100% CPU. Watch Prometheus and the Python terminal.</p><a href='/'>Return to Dashboard</a>"

@app.route('/webhook', methods=['POST'])
def scale():
    data = request.json
    if data['status'] == 'firing':
        print("🚨 WEBHOOK RECEIVED: CPU Critical Load detected by Prometheus!")
        print("🚀 Executing Terraform Cloud Provisioning...")
        # Runs your Terraform code to spin up the GCP VM
        subprocess.run(["terraform", "apply", "-auto-approve"], cwd="/home/eshani/terraform")
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)