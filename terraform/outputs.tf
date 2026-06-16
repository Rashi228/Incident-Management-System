output "backend_url" {
  description = "The URL of the Backend Cloud Run service"
  value       = google_cloud_run_v2_service.backend.uri
}

output "frontend_url" {
  description = "The URL of the Frontend Cloud Run service"
  value       = google_cloud_run_v2_service.frontend.uri
}

output "storage_bucket_name" {
  description = "The name of the GCS bucket"
  value       = google_storage_bucket.ims_bucket.name
}
