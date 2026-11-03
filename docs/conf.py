# Configuration file for the Sphinx documentation builder.
import os
import sys
from pathlib import Path

# Ajouter src au sys.path pour permettre a autodoc d'importer iatos_core
DOCS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DOCS_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(PROJECT_ROOT))

# Project information
project = "iatos_core"
copyright = "2026, Équipe Pédagogique OPCO Atlas / Simplon & Atos"
author = "Équipe Pédagogique OPCO Atlas"
release = "0.1.0"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
language = "fr"

# Napoleon settings (Google style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False

# Autodoc settings
autodoc_member_order = "bysource"
autodoc_typehints = "description"

# HTML output theme
html_theme = "furo"
html_title = "Documentation Technique iatos_core"
html_static_path = ["_static"]

html_theme_options = {
    "sidebar_hide_name": False,
    "light_css_variables": {
        "color-brand-primary": "#0c5699",
        "color-brand-content": "#4c3e7a",
    },
    "dark_css_variables": {
        "color-brand-primary": "#569cd6",
        "color-brand-content": "#9cdcfe",
    },
}
