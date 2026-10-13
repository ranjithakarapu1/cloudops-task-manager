output "application_url" {
  value       = "http://${aws_lb.app.dns_name}"
  description = "HTTP lab endpoint; add ACM/TLS before production"
}
output "rds_endpoint" {
  value       = aws_db_instance.mysql.address
  description = "Private MySQL endpoint"
}
output "efs_id" {
  value = aws_efs_file_system.shared.id
}
output "autoscaling_group_name" {
  value = aws_autoscaling_group.app.name
}
