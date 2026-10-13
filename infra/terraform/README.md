# Terraform infrastructure starter

This folder provisions a lab VPC, two public subnets for the ALB, two private app subnets,
a private DB subnet group, an internet gateway, ALB, EC2 Auto Scaling Group, EFS and RDS MySQL.

## Important design note
To avoid NAT Gateway charges in this starter, the private application instances are not placed
in private subnets with no egress. The current sample uses public-subnet EC2 instances with
public IP assignment disabled, which will not have internet egress and therefore cannot clone
the GitHub repo or install packages. Before applying, complete one of these deliberate lab paths:
1. Add one NAT Gateway and a private route for app subnets (simplest to get working; extra cost), or
2. Build a custom AMI containing Python/app/dependencies, and use SSM/VPC endpoints for operations, or
3. For a temporary lab only, place instances in public subnets with public IPs and restrict inbound
   traffic to the ALB security group (less secure; not the recommended final architecture).

This warning is intentional: do not apply a half-working architecture and assume the instances
can access package repositories. The Terraform is a scaffold to learn resource relationships,
not a one-click production module.

## Usage
- Install Terraform and configure AWS CLI with a named profile.
- Copy `terraform.tfvars.example` to `terraform.tfvars` and fill in values.
- Review every resource and your region/AZ quota.
- Run `terraform init`, `terraform fmt -check`, `terraform validate`, `terraform plan`.
- Apply only after you have selected and implemented an app egress/deployment strategy.
- After practice, run `terraform destroy` and inspect the AWS console for remaining resources.

RDS credentials are lab variables and can appear in Terraform state. Use Secrets Manager and a
carefully protected remote state backend for a more production-like exercise.
