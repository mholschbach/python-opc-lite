# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'python-opc-lite'
copyright = '2023, Karim S'
author = 'Karim S'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
    "sphinx_removed_in",
    "sphinxext.opengraph",

]

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

pygments_style = "sphinx"

autodoc_member_order = "groupwise"

rst_epilog = """

.. include:: /include/links.rst

.. |pol| replace:: `python-opc-lite`_
.. |kas| replace:: `Karim S`_

.. |part| replace:: :class:`.Part`
.. |relspart| replace:: :class:`.RelsPart`
.. |dt| replace:: :class:`.Dt`
.. |cp| replace:: :class:`.CoreProperties`
.. |package| replace:: :class:`.Package`
.. |rels| replace:: :class:`.Relationships`
.. |ct| replace:: :class:`.Types`
.. |uri| replace:: :class:`.Uri`
.. |pi| replace:: :class:`.PropertyItem`
.. |parser| replace:: :class:`.Parser`
.. |eb| replace:: :class:`.ElementBase`
.. |add_part| replace:: :meth:`add_part<opc.package.Package.add_part>`
"""
