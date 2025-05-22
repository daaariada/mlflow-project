variable "bucket_name" {
  description = "Base name for the S3 bucket"
  type        = string
}

variable "versioning_enabled" {
  description = "Enable bucket versioning"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags for the bucket"
  type        = map(string)
  default     = {}
}

variable "folder_id" {
  description = "Yandex Cloud Folder ID"
  type        = string
}
