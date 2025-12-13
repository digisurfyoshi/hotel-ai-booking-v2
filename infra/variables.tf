variable "project_id" {
  description = "The Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "The Google Cloud region"
  type        = string
  default     = "asia-northeast1"
}

variable "db_password" {
  description = "The password for the Cloud SQL database user"
  type        = string
  sensitive   = true
}
