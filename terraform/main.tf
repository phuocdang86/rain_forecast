# Defining the provider and version constraints
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.80.0"  # Provider version
    }
  }
  required_version = ">=1.9.6"  # Minimum Terraform version
}

# Google Cloud provider block
provider "google" {
  project = var.project_id
  region  = var.region
}

# Google Kubernetes Engine (GKE) cluster definition
resource "google_container_cluster" "primary" {
  name     = "${var.project_id}-gke"
  location = var.region

  # Enabling Autopilot mode
  enable_autopilot = true
}
