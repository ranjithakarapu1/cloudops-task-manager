variable "aws_region" {
  description = "AWS region for the lab"
  type        = string
  default     = "ap-south-1"
}
variable "project_name" {
  type    = string
  default = "cloudops-lab"
}
variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}
variable "azs" {
  type    = list(string)
  default = ["ap-south-1a", "ap-south-1b"]
}
variable "app_repo_url" {
  description = "Public HTTPS Git clone URL; used by the EC2 bootstrap script"
  type        = string
}
variable "db_name" {
  type    = string
  default = "tasks"
}
variable "db_username" {
  type    = string
  default = "taskadmin"
}
variable "db_password" {
  description = "Lab only. Prefer Secrets Manager for production."
  type        = string
  sensitive   = true
}
