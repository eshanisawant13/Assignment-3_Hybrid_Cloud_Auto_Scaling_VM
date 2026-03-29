provider "google" {
  project     = "inbound-bee-475916-p5"
  region      = "us-central1"
  credentials = file("/home/eshani/gcp-key.json")
}

resource "google_compute_instance" "burst_vm" {
  name         = "gcp-burst-node"
  machine_type = "e2-micro"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {
      # This gives the VM a public IP
    }
  }
}
