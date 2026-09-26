# RailConnect Deployment

## Phase 1 Deployment Model

The application is manually deployed to AWS.

GitHub Actions is used for CI validation only.

There is no automated AWS deployment in Phase 1.

## Planned Deployment Sequence

1. Prepare EC2
2. Install Python and application dependencies
3. Configure Flask application
4. Configure Gunicorn
5. Verify application locally on EC2
6. Configure Security Groups
7. Create AMI
8. Create Launch Template
9. Create Target Group
10. Configure Application Load Balancer
11. Create Auto Scaling Group
12. Configure CloudWatch monitoring
13. Perform controlled scaling test
14. Perform controlled failure test
15. Capture evidence

## AWS Region

ap-south-1

## Current Status

AWS deployment: NOT STARTED