# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ducpdf'
copyright = '2025, Ducflair'
author = 'Ducflair'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ['_static']

extensions.append('autoapi.extension')
autoapi_dirs = ["../src/ducpdf"]
# autoapi_keep_files = True
autoapi_root = "autoapi"
autoapi_add_toctree_entry = True
autoapi_options = [
    'members',
    'undoc-members',
    'private-members',
    'show-inheritance',
    'show-module-summary',
    'special-members',
]
autoapi_python_use_implicit_namespaces = True
autoapi_python_class_content = 'both'
autoapi_module_name_override = {
    'src.ducpdf': 'ducpdf',
}