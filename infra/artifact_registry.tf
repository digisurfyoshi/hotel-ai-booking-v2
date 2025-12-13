resource "google_artifact_registry_repository" "app_repo" {
  location      = var.region
  repository_id = "antigravity-repo"
  description   = "Docker repository for Antigravity application"
  format        = "DOCKER"
}
