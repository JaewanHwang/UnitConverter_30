"""프로젝트 루트를 sys.path에 올려 `import unit_converter`를 보장한다."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
