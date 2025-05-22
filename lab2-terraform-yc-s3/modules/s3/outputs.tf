output "bucket_name" {
  value = yandex_storage_bucket.s3.bucket
}

output "bucket_domain" {
  value = yandex_storage_bucket.s3.bucket_domain_name
}