#!/usr/bin/env python3
"""
Railway.app Deployment Configuration
Optimized for Railway's infrastructure
"""

import os
import sys
from app import app

# Railway-specific configuration
class RailwayConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'railway-writeup-ai-tool-v2')
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024
    UPLOAD_FOLDER = '/tmp/uploads'  # Railway uses ephemeral storage
    
    # Railway environment variables
    PORT = int(os.environ.get('PORT', 8080))
    RAILWAY_ENVIRONMENT = os.environ.get('RAILWAY_ENVIRONMENT', 'production')

app.config.from_object(RailwayConfig)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

if __name__ == "__main__":
    port = app.config['PORT']
    
    print("Enhanced Writeup Automation AI Tool v2.0")
    print("Railway Deployment - Production Ready")
    print(f"Server starting on port {port}")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )