variable "yc_token" {
  description = "Yandex Cloud OAuth token"
  type        = string
  sensitive   = true
}

variable "yc_cloud_id" {
  description = "Yandex Cloud Cloud ID"
  type        = string
}

variable "yc_folder_id" {
  description = "Yandex Cloud Folder ID"
  type        = string
}

variable "bucket_name" {
  description = "Base name for the S3 bucket"
  type        = string
  default     = "mlflow"
}

variable "versioning_enabled" {
  description = "Enable bucket versioning"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags for the bucket"
  type        = map(string)
  default     = {
    Environment = "Test"
    Terraform   = "true"
  }
}