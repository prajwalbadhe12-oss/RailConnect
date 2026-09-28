# RailConnect



## Highly Available and Auto-Scaling Railway Ticket Booking Platform Using AWS



RailConnect is a cloud-focused railway ticket booking



demonstration platform designed to demonstrate:



- High availability



- Horizontal scalability



- Load balancing



- Auto Scaling



- Health monitoring



- Fault tolerance



- Infrastructure standardization



- Secure AWS architecture



## Current Phase



Phase 1



## Technology Stack



### Frontend



- React



- JavaScript ES6+



- React Router



- CSS3



### Backend



- Python



- Flask



- Gunicorn



### Cloud



- Amazon EC2



- Application Load Balancer



- Target Group



- Auto Scaling Group



- Launch Template



- AMI



- CloudWatch



- IAM



- VPC



- Security Groups



### CI



- Git



- GitHub



- GitHub Actions



## Current Application Workflow



```text



Home



  ↓



Search Trains



  ↓



Search Results



  ↓



Select Train



  ↓



Passenger Details



  ↓



Booking Summary



  ↓



Confirm Booking



  ↓



Booking Confirmation

## Phase 1 AWS Validation & Evidence

### High Availability
- Application deployed behind an AWS Application Load Balancer.
- Auto Scaling Group configured with minimum 2, desired 2, maximum 4 instances.
- Instances distributed across ap-south-1b and ap-south-1c.
- ALB Target Group currently reports 2 healthy targets.

### Load Balancing Validation
- `/health` endpoint successfully returned `{"status":"healthy"}` through the ALB.
- `/api/server-info` returned different EC2 instance identities through repeated ALB requests.
- Requests were observed reaching instances in both ap-south-1b and ap-south-1c.

### Scaling Validation
- Scale-out test: desired capacity increased from 2 to 3.
- Auto Scaling Group successfully launched an additional EC2 instance.
- Scale-in test: desired capacity reduced from 3 to 2.
- Auto Scaling Group successfully removed the additional instance.

### Failure Recovery Validation
- An ASG instance was stopped/terminated to simulate an instance failure.
- Auto Scaling Group detected the unhealthy instance.
- The unhealthy instance was terminated.
- A replacement EC2 instance was automatically launched.
- Target Group returned to 2 healthy targets.

### CloudWatch Monitoring
- CloudWatch dashboard: `RailConnect-Phase1-Monitoring`
- CPU Utilization monitoring configured.
- ALB HealthyHostCount monitoring configured.
- ALB RequestCount monitoring configured.
- CPU alarm: `RailConnect-High-CPU`
- ALB health alarm: `RailConnect-ALB-Unhealthy-Host`
- Both alarms currently report OK.

### Application API Validation
- `/health` verified through ALB.
- `/api/server-info` verified through ALB.
- `/api/v1/trains` returned 5 clearly identified demo railway records.
- `/api/v1/bookings` successfully created a demonstration booking through the ALB.

### AWS Infrastructure Constraint Observed
- During one instance refresh, an EC2 launch failed because the AWS account reached its available 8-vCPU limit for the relevant instance bucket.
- Subsequent instance launches succeeded after the refresh/recovery process.
- This was an AWS account capacity limitation, not an application failure.