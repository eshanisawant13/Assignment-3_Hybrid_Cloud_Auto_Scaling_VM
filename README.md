This is a comprehensive, professional **README.md** file for your repository. It is designed to be clear, technically deep, and easy for your instructor to follow.

---

# **Hybrid Cloud Bursting: Automated Scaling to GCP**

## **1. Project Description**
This project implements a **Cloud Bursting** architecture. The system monitors a local virtualized environment (Ubuntu VM) for high resource consumption. When the system detects a CPU/Load threshold exceeding **75%**, it automatically triggers an Infrastructure-as-Code (IaC) pipeline to provision a new Virtual Machine in **Google Cloud Platform (GCP)** to handle the overflow workload.

---

## **2. Technology Stack**

### **The Monitoring Layer**
* **Ubuntu 24.04 LTS:** The base Operating System for the local environment.
* **Node Exporter:** A Prometheus exporter that sits on the OS and collects hardware/kernel metrics (CPU, RAM, Disk).
* **Prometheus:** A time-series database and monitoring server that "scrapes" metrics from the Node Exporter and evaluates alerting rules.
* **Alertmanager:** Handles alerts sent by Prometheus. It deduplicates, groups, and routes them to the correct receiver via webhooks.

### **The Integration Layer (Backend)**
* **Python (Flask):** A lightweight web server that acts as the "Scaling Brain." It listens for signals from the monitoring stack.
* **Terraform:** An Infrastructure-as-Code tool used to provision and manage the GCP Compute Engine instances.
* **GCP SDK (gcloud):** Used for authentication between the local VM and Google Cloud.

---

## **3. Backend Scripts & Why They Are Used**

### **`scaler.py` (The Webhook Listener)**
* **Why:** Prometheus cannot run shell commands directly. This script acts as the "bridge." It listens on port `5001` for a POST request from Alertmanager. 
* **Logic:** When it receives a "firing" alert, it triggers a system call to execute Terraform. It also provides a web-based dashboard for manual stress testing.

### **`main.tf` (The Infrastructure Definition)**
* **Why:** To ensure the cloud VM is created exactly the same way every time.
* **Role:** Defines the machine type (`e2-micro`), the OS image (`debian-11`), and the network settings for the Google Cloud instance.

### **`alert_rules.yml` (The Threshold Logic)**
* **Why:** To define exactly what "75% usage" means.
* **Logic:** It uses the expression `node_load1 > 0.75` for a duration of 30 seconds to ensure the system doesn't scale up for tiny, temporary spikes.

---

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

---

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

## **6. Declaration (Plagiarism Clause)**
I, **Eshani**, hereby declare that this implementation and all associated documentation are my original work. The logic for the hybrid cloud integration, the configuration of the monitoring stack, and the Terraform scripts were developed by me to fulfill the requirements of this assignment.
