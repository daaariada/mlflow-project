module "s3" {
  source = "./modules/s3"

  bucket_name        = var.bucket_name
  folder_id         = var.yc_folder_id
  versioning_enabled = var.versioning_enabled
  tags               = var.tags
}