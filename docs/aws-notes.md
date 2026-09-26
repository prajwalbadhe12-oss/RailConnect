# RailConnect AWS Notes

## Region

ap-south-1

## Planned Services

### Compute
- Amazon EC2

### Load Balancing
- Application Load Balancer
- Target Group

### Scaling
- Auto Scaling Group
- Launch Template
- AMI

### Monitoring
- Amazon CloudWatch

### Networking
- VPC
- Subnets
- Security Groups

### Identity
- IAM

## Security Principles

- Do not commit credentials.
- Restrict SSH access.
- EC2 application traffic should primarily come from
  the ALB Security Group.
- Do not unnecessarily expose application ports.
- Use /health for Target Group health checks.

## Phase 1 CI/CD Boundary

GitHub Actions:

YES:
- dependency installation
- frontend validation
- backend tests
- build validation
- CI reporting

NO:
- automatic AWS deployment
- GitHub OIDC deployment role
- production deployment pipeline