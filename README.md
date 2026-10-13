# CloudOps Task Manager — AWS DevOps Lab

A small FastAPI + MySQL task API intended for learning AWS architecture and DevOps.

## Components
- FastAPI application
- MySQL persistence (SQLAlchemy)
- EFS-compatible shared directory for file uploads
- Dockerfile for local container practice
- Terraform starter architecture for VPC, public ALB, private EC2 Auto Scaling Group,
  EFS, and RDS MySQL
- GitHub Actions CI test workflow

> This is a learning starter, not a production-certified deployment. Review the Terraform,
> secrets handling, patching, TLS, logging, backups, and network egress before production use.

## 1. Run locally
Requires Python 3.11+ and MySQL, or Docker Compose.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows; on macOS/Linux use: cp .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs and http://127.0.0.1:8000/health.

For local development, set `DATABASE_URL` to a reachable MySQL database. If no database URL
is configured, the app uses a local SQLite file for easy first-run practice.

## 2. Docker
```bash
docker build -t cloudops-task-manager .
docker run --rm -p 8000:8000 -e DATABASE_URL=sqlite:///./tasks.db cloudops-task-manager
```

## 3. GitHub
Create a GitHub repository, then push this folder:
```bash
git init
git add .
git commit -m "Initial CloudOps Task Manager"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/cloudops-task-manager.git
git push -u origin main
```

GitHub Actions runs the unit tests on pushes and pull requests.

## 4. Terraform starter
See `infra/terraform/README.md` before running Terraform. Do not commit `terraform.tfvars`,
state files, database passwords, private keys, or AWS credentials.

The infrastructure starter intentionally requires you to supply the Git clone URL and database
password through local Terraform variables. It does not create NAT Gateways to keep lab costs
lower; the instances use public-subnet routing in this starter and are restricted by security
groups. For a stronger production design, use private app subnets with NAT or suitable VPC
endpoints and a controlled deployment/artifact path.

## 5. Recommended learning sequence
1. Run and test locally.
2. Push to GitHub and observe CI.
3. Build the Docker image.
4. Review and apply Terraform in a test AWS account.
5. Test ALB health checks and ASG replacement.
6. Upload a file and verify it is visible through EFS from either instance.
7. Add CodePipeline/CodeDeploy or GitHub Actions OIDC deployment.
8. Add CloudWatch alarms, Secrets Manager, TLS, WAF, and RDS Multi-AZ as separate exercises.
9. Destroy all lab resources when finished.
