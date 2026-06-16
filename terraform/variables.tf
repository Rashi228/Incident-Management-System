variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
}

variable "region" {
  description = "The region to deploy resources to"
  type        = string
  default     = "asia-south1"
}

variable "bucket_name" {
  description = "Name of the GCS bucket for uploads"
  type        = string
}

variable "database_url" {
  description = "PostgreSQL connection string"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "Secret key for JWT authentication"
  type        = string
  sensitive   = true
}
