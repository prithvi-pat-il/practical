#!/usr/bin/python3.9

import sys
import os

# Add your project directory to Python path
sys.path.insert(0, '/home/yourusername/college_practical_helper')

from app import app as application

if __name__ == "__main__":
    application.run()
