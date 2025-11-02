#!/usr/bin/env python3
"""
AWS Deployment Configuration
For EC2, Elastic Beanstalk, or ECS deployment
"""

import os
import sys
import boto3
from app import app

# AWS-specific configuration
class AWSConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'aws-writeup-ai-tool-v2')
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024
    
    # Use S3 for file storage in production
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/tmp/uploads')
    AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET', None)
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    
    # AWS environment variables
    PORT = int(os.environ.get('PORT', 8080))

app.config.from_object(AWSConfig)

# Initialize S3 client if bucket is configured
s3_client = None
if app.config['AWS_S3_BUCKET']:
    try:
        s3_client = boto3.client('s3', region_name=app.config['AWS_REGION'])
        print(f"S3 storage configured: {app.config['AWS_S3_BUCKET']}")
    except Exception as e:
        print(f"S3 configuration failed: {e}")
        s3_client = None

# Ensure local upload directory exists as fallback
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

if __name__ == "__main__":
    port = app.config['PORT']
    
    print("Enhanced Writeup Automation AI Tool v2.0")
    print("AWS Deployment - Enterprise Ready")
    print(f"Server starting on port {port}")
    print(f"Storage: {'S3' if s3_client else 'Local'}")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )