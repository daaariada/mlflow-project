resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "yandex_storage_bucket" "s3" {
  bucket     = "${var.bucket_name}-${random_id.bucket_suffix.hex}"  # Уникальное имя с суффиксом
  acl        = "private"
  folder_id  = var.folder_id
  
  versioning {
    enabled = var.versioning_enabled
  }

  tags = var.tags
}