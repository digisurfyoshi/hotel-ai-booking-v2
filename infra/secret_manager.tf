resource "google_secret_manager_secret" "db_url" {
  secret_id = "antigravity-db-url"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_url_version" {
  secret = google_secret_manager_secret.db_url.id
  secret_data = "postgresql://antigravity_user:${var.db_password}@/${google_sql_database.database.name}?host=/cloudsql/${google_sql_database_instance.main.connection_name}"
}
