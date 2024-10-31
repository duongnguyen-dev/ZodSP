terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.80.0"
    }
  }
}

// The library with methods for creating and
// managing the infrastructure in GCP, this will
// apply to all the resources in the project
provider "google" {
  project     = var.project_id
  region      = var.region
}

// Google Kubernetes Engine
resource "google_container_cluster" "sgd-cluster" {
  name = "${var.project_id}-sgd-gke"
  location = var.region

  enable_autopilot = true
}

# resource "google_compute_instance" "sgd" {
#   name = var.instance_name
#   machine_type = var.machine_type
#   zone = var.zone

#   boot_disk {
#     initialize_params {
#       image = var.boot_disk_image
#       size = var.boot_disk_size
#     }
#   }
  
#   network_interface {
#     network = "default"

#     access_config {
#       // If you don't set anything here, the instance only have internal IP
#     }
#   }
# }

resource "google_compute_firewall" "sgd-firewall" {
  name = var.firewall_name
  network = "default"

  allow {
    protocol = "tcp"
    ports = ["3002"]
  }

  source_ranges = ["0.0.0.0/0"] // Allow all traffic
}