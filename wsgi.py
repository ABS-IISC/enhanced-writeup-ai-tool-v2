#!/usr/bin/env python3
"""
WSGI Entry Point for Enhanced Writeup Automation AI Tool
Production deployment configuration
"""

import os
import sys
from app import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5005))
    app.run(host='0.0.0.0', port=port, debug=False)