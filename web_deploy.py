#!/usr/bin/env python3
"""
Web Deployment Script for Enhanced Writeup Automation AI Tool
Optimized for cloud deployment (Heroku, Railway, Render, etc.)
"""

import os
import sys
from app import app

# Production configuration
class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'enhanced-writeup-ai-tool-v2-production')
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB max file size
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')

# Apply production config
app.config.from_object(ProductionConfig)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

if __name__ == "__main__":
    # Get port from environment variable (for cloud deployment)
    port = int(os.environ.get('PORT', 5005))
    
    print("Enhanced Writeup Automation AI Tool v2.0")
    print("Advanced Split View | Enhanced Analysis | Improved Chat")
    print(f"Starting web server on port {port}...")
    print("=" * 60)
    
    # Run with production settings
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )