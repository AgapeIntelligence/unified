from setuptools import setup, find_packages




# 2. Move your already-uploaded SDK code into the new structure
mv agapeintelligence-sdk src/core_sdk

# 3. Create the unified __init__ that makes everything importable
cat > src/__init__.py << 'EOF'
"""Unified Agape Framework – All 28 repositories in one living import"""
from .core_sdk import *
from .resonance import *
from .quantum import *
from .cognition import *
from .synchronicity import *
from .extensions import *

__version__ = "1.0.0"
__all__ = ["core_sdk", "resonance", "quantum", "cognition", "synchronicity", "extensions"]
