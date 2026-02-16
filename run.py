#!/usr/bin/env python3
"""
Точка входа в программу.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import main

if __name__ == "__main__":
    sys.exit(main())