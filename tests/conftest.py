"""Configuration et fixtures pytest."""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Injecter la racine du projet et le dossier src dans sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

for path in [str(PROJECT_ROOT), str(SRC_DIR)]:
    if path not in sys.path:
        sys.path.insert(0, path)

from backend.main import app


@pytest.fixture(scope="session")
def client():
    """Fixture retournant un client de test FastAPI."""
    with TestClient(app) as test_client:
        yield test_client
