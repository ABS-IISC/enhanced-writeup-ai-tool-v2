#!/usr/bin/env python3
"""
Heroku Deployment Configuration
Optimized for Heroku's dyno system
"""

import os
import sys
from app import app

# Heroku-specific configuration
class HerokuConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'heroku-writeup-ai-tool-v2')
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024
    UPLOAD_FOLDER = '/tmp/uploads'  # Heroku uses ephemeral storage
    
    # Heroku environment variables
    PORT = int(os.environ.get('PORT', 5000))
    DYNO = os.environ.get('DYNO', 'web.1')

app.config.from_object(HerokuConfig)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

if __name__ == "__main__":
    port = app.config['PORT']
    
    print("Enhanced Writeup Automation AI Tool v2.0")
    print("Heroku Deployment - Production Ready")
    print(f"Server starting on port {port}")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )