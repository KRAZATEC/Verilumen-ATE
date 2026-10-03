"""
Verilumen ATE Intelligence Platform - Streamlit Entry Point
"""

import sys
from pathlib import Path

# Ensure root directory is always on python sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Execute the core Streamlit application
from backend.app.streamlit_app import *
