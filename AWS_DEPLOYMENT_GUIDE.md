# 🚀 AWS Deployment Guide - Enhanced Writeup Automation AI Tool v2.0

## 📋 Table of Contents
1. [Quick AWS Deployment Options](#quick-deployment)
2. [AWS Elastic Beanstalk (Recommended)](#elastic-beanstalk)
3. [AWS EC2 with Docker](#ec2-docker)
4. [AWS ECS (Container Service)](#ecs-deployment)
5. [AWS Lambda + API Gateway](#serverless)
6. [AWS App Runner](#app-runner)
7. [Production Setup](#production-setup)
8. [Cost Optimization](#cost-optimization)
9. [Monitoring & Logging](#monitoring)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Quick AWS Deployment Options

### Option 1: AWS Elastic Beanstalk (Easiest)
**Best for**: Quick deployment, auto-scaling, managed infrastructure
**Cost**: ~$10-50/month
**Time**: 10 minutes

### Option 2: AWS EC2 + Docker
**Best for**: Full control, custom configurations
**Cost**: ~$8-30/month
**Time**: 20 minutes

### Option 3: AWS ECS (Container Service)
**Best for**: Production workloads, microservices
**Cost**: ~$15-60/month
**Time**: 30 minutes

### Option 4: AWS App Runner
**Best for**: Containerized apps, auto-scaling
**Cost**: ~$12-40/month
**Time**: 15 minutes

---

## 🌱 AWS Elastic Beanstalk Deployment (Recommended)

### Prerequisites
```bash
# Install AWS CLI
pip install awscli awsebcli

# Configure AWS credentials
aws configure
```

### Step 1: Prepare Application
```bash
# Create application.py (required for Beanstalk)
cp aws_deploy.py application.py
```

### Step 2: Create Beanstalk Configuration
```bash
# Initialize Elastic Beanstalk
eb init

# Select:
# - Region: us-east-1 (or your preferred region)
# - Application name: writeup-ai-tool-v2
# - Platform: Python 3.9
# - SSH: Yes (recommended)
```

### Step 3: Deploy
```bash
# Create environment and deploy
eb create production --instance-type t3.small

# Deploy updates
eb deploy
```

### Step 4: Configure Environment Variables
```bash
eb setenv SECRET_KEY=your-super-secret-key-here
eb setenv AWS_S3_BUCKET=your-s3-bucket-name
eb setenv AWS_REGION=us-east-1
```

### Step 5: Access Your Application
```bash
# Open in browser
eb open
```

**Your app will be available at**: `http://writeup-ai-tool-v2.us-east-1.elasticbeanstalk.com`

---

## 🖥️ AWS EC2 + Docker Deployment

### Step 1: Launch EC2 Instance
1. **Go to AWS Console → EC2**
2. **Launch Instance**:
   - AMI: Amazon Linux 2
   - Instance Type: t3.small (2 vCPU, 2GB RAM)
   - Security Group: Allow HTTP (80), HTTPS (443), SSH (22)
   - Key Pair: Create or select existing

### Step 2: Connect and Setup
```bash
# Connect to instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Docker
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 3: Deploy Application
```bash
# Clone your repository or upload files
git clone https://github.com/your-username/ct_review_tool_9.git
cd ct_review_tool_9

# Build and run
docker build -t writeup-ai-tool .
docker run -d --name writeup-ai-tool -p 80:5005 --restart unless-stopped writeup-ai-tool
```

### Step 4: Setup Nginx (Optional)
```bash
# Install nginx
sudo yum install nginx -y

# Configure nginx
sudo tee /etc/nginx/conf.d/writeup-ai.conf << EOF
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5005;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Start nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## 🐳 AWS ECS Deployment

### Step 1: Create ECR Repository
```bash
# Create repository
aws ecr create-repository --repository-name writeup-ai-tool

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
```

### Step 2: Build and Push Image
```bash
# Build image
docker build -t writeup-ai-tool .

# Tag image
docker tag writeup-ai-tool:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/writeup-ai-tool:latest

# Push image
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/writeup-ai-tool:latest
```

### Step 3: Create ECS Task Definition
```json
{
  "family": "writeup-ai-tool",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "writeup-ai-tool",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/writeup-ai-tool:latest",
      "portMappings": [
        {
          "containerPort": 5005,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "SECRET_KEY",
          "value": "your-secret-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/writeup-ai-tool",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Step 4: Create ECS Service
```bash
# Create cluster
aws ecs create-cluster --cluster-name writeup-ai-cluster

# Create service
aws ecs create-service \
  --cluster writeup-ai-cluster \
  --service-name writeup-ai-service \
  --task-definition writeup-ai-tool:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
```

---

## ⚡ AWS Lambda + API Gateway (Serverless)

### Step 1: Install Serverless Framework
```bash
npm install -g serverless
npm install serverless-wsgi serverless-python-requirements
```

### Step 2: Create serverless.yml
```yaml
service: writeup-ai-tool

provider:
  name: aws
  runtime: python3.9
  region: us-east-1
  timeout: 30
  memorySize: 1024

functions:
  app:
    handler: wsgi_handler.handler
    events:
      - http: ANY /
      - http: 'ANY {proxy+}'

plugins:
  - serverless-wsgi
  - serverless-python-requirements

custom:
  wsgi:
    app: app.app
    packRequirements: false
  pythonRequirements:
    dockerizePip: non-linux
```

### Step 3: Deploy
```bash
# Deploy to AWS
serverless deploy
```

---

## 🏃 AWS App Runner

### Step 1: Create apprunner.yaml
```yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - pip install -r requirements.txt
run:
  runtime-version: 3.9.16
  command: python aws_deploy.py
  network:
    port: 8080
    env: PORT
  env:
    - name: PORT
      value: "8080"
    - name: SECRET_KEY
      value: "your-secret-key"
```

### Step 2: Deploy via Console
1. Go to **AWS App Runner Console**
2. **Create Service**
3. **Source**: Container registry or Source code repository
4. **Configure**: Use apprunner.yaml
5. **Deploy**

---

## 🏭 Production Setup

### 1. S3 Storage Configuration
```bash
# Create S3 bucket
aws s3 mb s3://writeup-ai-tool-storage-bucket

# Set environment variables
export AWS_S3_BUCKET=writeup-ai-tool-storage-bucket
export AWS_REGION=us-east-1
```

### 2. RDS Database (Optional)
```bash
# Create RDS instance for persistent storage
aws rds create-db-instance \
  --db-instance-identifier writeup-ai-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password your-password \
  --allocated-storage 20
```

### 3. CloudFront CDN
```bash
# Create CloudFront distribution
aws cloudfront create-distribution \
  --distribution-config file://cloudfront-config.json
```

### 4. Route 53 Domain
```bash
# Create hosted zone
aws route53 create-hosted-zone \
  --name yourdomain.com \
  --caller-reference $(date +%s)
```

### 5. SSL Certificate
```bash
# Request SSL certificate
aws acm request-certificate \
  --domain-name yourdomain.com \
  --domain-name www.yourdomain.com \
  --validation-method DNS
```

---

## 💰 Cost Optimization

### Monthly Cost Estimates

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| **Elastic Beanstalk** | t3.small | $15-25 |
| **EC2 + Docker** | t3.small | $12-20 |
| **ECS Fargate** | 0.5 vCPU, 1GB | $18-30 |
| **Lambda** | 1M requests | $5-15 |
| **App Runner** | 1 vCPU, 2GB | $20-35 |

### Cost Optimization Tips
```bash
# Use spot instances for EC2
aws ec2 request-spot-instances --spot-price "0.05" --instance-count 1

# Enable auto-scaling
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name writeup-ai-asg \
  --min-size 1 \
  --max-size 3 \
  --desired-capacity 1

# Use S3 Intelligent Tiering
aws s3api put-bucket-intelligent-tiering-configuration \
  --bucket writeup-ai-tool-storage \
  --id EntireBucket \
  --intelligent-tiering-configuration Id=EntireBucket,Status=Enabled
```

---

## 📊 Monitoring & Logging

### 1. CloudWatch Setup
```bash
# Create log group
aws logs create-log-group --log-group-name /aws/writeup-ai-tool

# Create custom metrics
aws cloudwatch put-metric-data \
  --namespace "WriteupAI/Application" \
  --metric-data MetricName=DocumentsProcessed,Value=1,Unit=Count
```

### 2. Application Monitoring
```python
# Add to your app.py
import boto3

cloudwatch = boto3.client('cloudwatch')

def log_metric(metric_name, value, unit='Count'):
    cloudwatch.put_metric_data(
        Namespace='WriteupAI/Application',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit
            }
        ]
    )
```

### 3. Health Checks
```bash
# Create health check endpoint
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0'
    })
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Memory Issues
```bash
# Increase instance size
eb config
# Change InstanceType to t3.medium

# Or for ECS
aws ecs update-service \
  --cluster writeup-ai-cluster \
  --service writeup-ai-service \
  --task-definition writeup-ai-tool:2
```

#### 2. File Upload Issues
```bash
# Check S3 permissions
aws s3api get-bucket-policy --bucket your-bucket-name

# Increase upload limits
export MAX_CONTENT_LENGTH=67108864  # 64MB
```

#### 3. SSL Certificate Issues
```bash
# Check certificate status
aws acm list-certificates

# Validate certificate
aws acm describe-certificate --certificate-arn your-cert-arn
```

#### 4. Performance Issues
```bash
# Enable CloudFront caching
aws cloudfront create-cache-policy \
  --cache-policy-config file://cache-policy.json

# Add Redis for session storage
pip install redis flask-session
```

### Debugging Commands
```bash
# Elastic Beanstalk logs
eb logs

# EC2 instance logs
sudo tail -f /var/log/docker

# ECS service logs
aws logs get-log-events \
  --log-group-name /ecs/writeup-ai-tool \
  --log-stream-name ecs/writeup-ai-tool/task-id

# Lambda logs
aws logs tail /aws/lambda/writeup-ai-tool --follow
```

---

## 🚀 Quick Deployment Commands

### Elastic Beanstalk (Fastest)
```bash
eb init --platform python-3.9 --region us-east-1
eb create production --instance-type t3.small
eb setenv SECRET_KEY=your-secret-key
eb open
```

### EC2 Docker (Most Control)
```bash
# Launch t3.small instance, then:
sudo yum update -y && sudo yum install docker -y
sudo service docker start
docker run -d -p 80:5005 --restart unless-stopped your-dockerhub-username/writeup-ai-tool
```

### App Runner (Easiest Container)
```bash
# Push to ECR, then create App Runner service via console
# Point to your ECR image
# Set PORT=8080 environment variable
```

---

## 📞 Support & Next Steps

### After Deployment Checklist
- [ ] Application accessible via public URL
- [ ] File uploads working correctly
- [ ] Chat functionality operational
- [ ] Analysis engine processing documents
- [ ] SSL certificate configured (production)
- [ ] Custom domain configured (optional)
- [ ] Monitoring and alerts setup
- [ ] Backup strategy implemented
- [ ] Cost monitoring enabled

### Production Recommendations
1. **Use Application Load Balancer** for high availability
2. **Enable auto-scaling** for traffic spikes
3. **Setup CloudWatch alarms** for monitoring
4. **Implement backup strategy** for user data
5. **Use AWS Secrets Manager** for sensitive data
6. **Enable AWS WAF** for security
7. **Setup CI/CD pipeline** for deployments

**Your Enhanced Writeup Automation AI Tool v2.0 is now ready for AWS deployment! 🚀**

Choose the deployment method that best fits your needs and budget. Elastic Beanstalk is recommended for beginners, while EC2 offers more control for advanced users.