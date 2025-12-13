resource "google_sql_database_instance" "main" {
  name             = "antigravity-db-instance"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro" # Minimal tier for dev/test
  }
  deletion_protection = false # For ease of reconstruction in this phase
}

resource "google_sql_database" "database" {
  name     = "antigravity_db"
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "users" {
  name     = "antigravity_user"
  instance = google_sql_database_instance.main.name
  password = var.db_password
}
