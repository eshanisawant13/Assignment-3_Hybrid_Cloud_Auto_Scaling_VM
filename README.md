
# **Hybrid Cloud: Auto Scaling to GCP**

## **1. Project Description**
This project implements a **Hybrid Cloud Auto Scaling** architecture. The system monitors a local virtualized environment (Ubuntu VM) for high resource consumption. When the system detects a CPU/Load threshold exceeding **75%**, it automatically triggers an Infrastructure-as-Code (IaC) pipeline to provision a new Virtual Machine in **Google Cloud Platform (GCP)** to handle the overflow workload.
<img width="1177" height="537" alt="c" src="https://github.com/user-attachments/assets/b094cbcb-ed6f-437a-b507-db5b19ce3e0d" />

## **2. Technology Stack**

### **The Monitoring Layer**
* **Ubuntu 24.04 LTS:** The base Operating System for the local environment.
* **Node Exporter:** A Prometheus exporter that sits on the OS and collects hardware/kernel metrics (CPU, RAM, Disk).
* **Prometheus:** A time-series database and monitoring server that "scrapes" metrics from the Node Exporter and evaluates alerting rules.
* **Alertmanager:** Handles alerts sent by Prometheus. It deduplicates, groups, and routes them to the correct receiver via webhooks.

### **The Integration Layer (Backend)**
* **Python (Flask):** A lightweight web server that acts as the "Scaling Brain." It listens for signals from the monitoring stack.
 

 **Terraform:** An Infrastructure-as-Code tool used to provision and manage the GCP Compute Engine instances.
* **GCP SDK (gcloud):** Used for authentication between the local VM and Google Cloud.
  <img width="1670" height="848" alt="image" src="https://github.com/user-attachments/assets/1d358abb-7bc1-4731-8bd2-bbc755a0e1db" />



## **3. Backend Scripts & Why They Are Used**

### **`scaler.py` (The Webhook Listener)**
* **Purpose:** Prometheus cannot run shell commands directly. This script acts as the "bridge." It listens on port `5001` for a POST request from Alertmanager. 
* **Logic:** When it receives a "firing" alert, it triggers a system call to execute Terraform. It also provides a web-based dashboard for manual stress testing.

### **`main.tf` (The Infrastructure Definition)**
* **Purpose:** To ensure the cloud VM is created exactly the same way every time.
* **Role:** Defines the machine type (`e2-micro`), the OS image (`debian-11`), and the network settings for the Google Cloud instance.

### **`alert_rules.yml` (The Threshold Logic)**
* **Purpose:** To define exactly what "75% usage" means.
* **Logic:** It uses the expression `node_load1 > 0.75` for a duration of 30 seconds to ensure the system doesn't scale up for tiny, temporary spikes.


## **4. Configuration & Setup**

### **Step 1: Local VM Prep**
```bash
sudo apt update && sudo apt install prometheus prometheus-node-exporter terraform stress -y
```

### **Step 2: Monitoring Setup**
1.  **Prometheus:** Edit `/etc/prometheus/prometheus.yml` to include the `node` job and point to your `alert_rules.yml`.
2.  **Alertmanager:** Edit `/etc/prometheus/alertmanager.yml` to route alerts to `http://localhost:5001/webhook`.

### **Step 3: GCP Authentication**
Place your Google Cloud Service Account JSON key in the `terraform/` directory and initialize:
```bash
cd terraform
terraform init
```


## **5. Execution Flow**

1.  **Start the Scaler:**
    ```bash
    source myenv/bin/activate
    python3 scaler.py
    ```
2.  **Access the Dashboard:** Open `http://<VM_IP>:5001` in your browser.
3.  **Trigger Stress Test:** Click **"Execute Stress Simulation"**.
4.  **Automatic Scaling:**
    * **Prometheus** detects load > 0.75.
    * **Alertmanager** sends a signal to the Python script.
    * **Python** executes `terraform apply -auto-approve`.
    * **GCP** spins up a new instance within 30-60 seconds.

---
So hence we saw the entire procedure how in hybrid cloud auto scaling is done , when the resource utilization exceeds above 75 % usage , new auto scaled VM's are created in Google Cloud Storage.
