#!/usr/bin/env python3
"""
Railway.app Deployment Configuration
Optimized for Railway's infrastructure with fixes
"""

import os
import sys
from app import app

# Railway-specific configuration with fixes
class RailwayConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'railway-writeup-ai-tool-v2-secure')
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024
    UPLOAD_FOLDER = '/tmp/uploads'  # Railway uses ephemeral storage
    
    # Railway environment variables
    PORT = int(os.environ.get('PORT', 8080))
    RAILWAY_ENVIRONMENT = os.environ.get('RAILWAY_ENVIRONMENT', 'production')
    
    # Additional Railway optimizations
    SEND_FILE_MAX_AGE_DEFAULT = 31536000
    PERMANENT_SESSION_LIFETIME = 1800

app.config.from_object(RailwayConfig)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Add health check endpoint for Railway
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'service': 'writeup-ai-tool-v2'}, 200

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