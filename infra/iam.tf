resource "google_service_account" "cloud_run_sa" {
  account_id   = "antigravity-cloud-run-sa"
  display_name = "Cloud Run Service Account"
}

# Grant operations on Cloud SQL to the service account
resource "google_project_iam_member" "sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}
