#!/usr/bin/env python3
"""
Render.com Deployment Configuration
Optimized for Render's infrastructure
"""

import os
import sys
from app import app

# Render-specific configuration
class RenderConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'render-writeup-ai-tool-v2')
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024
    UPLOAD_FOLDER = '/tmp/uploads'  # Render uses ephemeral storage
    
    # Render environment variables
    PORT = int(os.environ.get('PORT', 10000))
    RENDER_SERVICE_NAME = os.environ.get('RENDER_SERVICE_NAME', 'writeup-ai-tool')

app.config.from_object(RenderConfig)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

if __name__ == "__main__":
    port = app.config['PORT']
    
    print("Enhanced Writeup Automation AI Tool v2.0")
    print("Render Deployment - Production Ready")
    print(f"Server starting on port {port}")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )