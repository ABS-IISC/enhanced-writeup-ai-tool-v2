#!/usr/bin/env python3
"""
Complete Railway Deployment Fix
Addresses all localhost vs Railway differences
"""

import os
import sys
from app import app
from flask import jsonify

# Railway Production Configuration
class RailwayProductionConfig:
    # Basic Flask settings
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'railway-secure-key-2024')
    
    # File upload settings
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB
    UPLOAD_FOLDER = '/tmp/uploads'  # Railway ephemeral storage
    
    # Railway specific
    PORT = int(os.environ.get('PORT', 8080))
    RAILWAY_ENVIRONMENT = 'production'
    
    # Performance optimizations
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year cache
    PERMANENT_SESSION_LIFETIME = 1800     # 30 minutes
    
    # Security headers
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

# Apply configuration
app.config.from_object(RailwayProductionConfig)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Add Railway-specific routes
@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'service': 'Enhanced Writeup AI Tool v2.0',
        'environment': 'Railway Production',
        'upload_folder': app.config['UPLOAD_FOLDER'],
        'port': app.config['PORT']
    }), 200

@app.route('/railway-info')
def railway_info():
    """Railway deployment information"""
    return jsonify({
        'deployment': 'Railway',
        'storage': 'Ephemeral (/tmp)',
        'warning': 'Files will be deleted on container restart',
        'recommendation': 'Use cloud storage for production',
        'health_check': '/health'
    }), 200

# Add error handlers for Railway
@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        'error': 'File too large',
        'max_size': '32MB',
        'railway_limit': 'Ephemeral storage limited'
    }), 413

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'railway_note': 'Check Railway logs for details',
        'health_check': '/health'
    }), 500

if __name__ == "__main__":
    port = app.config['PORT']
    
    print("Enhanced Writeup Automation AI Tool v2.0")
    print("Railway Production Deployment - Fixed Version")
    print(f"Server starting on port {port}")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"Health check: /health")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )