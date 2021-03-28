# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = u'AsceticBear'
copyright = u'2021, bear'
author = u'bear'

# The short X.Y version
version = u''
# The full version, including alpha/beta/rc tags
release = u'0.3.0'


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# extensions = ['recommonmark']
# -- Extensions --------------------------------------------------------------
extensions = [
    "recommonmark",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
source_suffix = ['.rst', '.md']
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [u'_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
# html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = [
    '_static/css/custom.css',
]


# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# html_title = "{} {}".format(project, release)
html_short_title = "Home"

html_theme = 'p-greenblue'
import os
from PSphinxTheme import utils

p, html_theme, needs_sphinx = utils.set_psphinxtheme(html_theme)
html_theme_path = p

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'beardoc'

# -- Options for manual page output ------------------------------------------
# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'bear', u'bear docs',
     [author], 1)
]

# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# latex_elements={# The paper size ('letterpaper' or 'a4paper').
# 'papersize':'letterpaper',# The font size ('10pt', '11pt' or '12pt').
# 'pointsize':'12pt','classoptions':',oneside','babel':'',#必須
# 'inputenc':'',#必須
# 'utf8extra':'',#必須
# # Additional stuff for the LaTeX preamble.
# 'preamble': r"""
# \usepackage{xeCJK}
# \usepackage{indentfirst}
# \setlength{\parindent}{2em}
# \setCJKmainfont{WenQuanYi Micro Hei}
# \setCJKmonofont[Scale=0.9]{WenQuanYi Micro Hei Mono}
# \setCJKfamilyfont{song}{WenQuanYi Micro Hei}
# \setCJKfamilyfont{sf}{WenQuanYi Micro Hei}
# \XeTeXlinebreaklocale "zh"
# \XeTeXlinebreakskip = 0pt plus 1pt
# """}