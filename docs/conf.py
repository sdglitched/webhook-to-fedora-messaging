# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import re
import sys


topdir = os.path.abspath("../")
sys.path.insert(0, topdir)

import webhook_to_fedora_messaging  # NOQA


# -- Project information -----------------------------------------------------

project = "Webhook to Fedora Messaging"
copyright = "2024, Contributors to the Fedora Project"
author = "Fedora Infrastructure"

# The short X.Y version
version = ".".join(webhook_to_fedora_messaging.__version__.split(".")[:2])

# The full version, including alpha/beta/rc tags
release = webhook_to_fedora_messaging.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "myst_parser",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Explcitely set the master doc
# https://github.com/readthedocs/readthedocs.org/issues/2569
master_doc = "index"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "github_user": "fedora-infra",
    "github_repo": "webhook-to-fedora-messaging",
    "page_width": "1040px",
    "show_related": True,
    "sidebar_collapse": True,
    "caption_font_size": "140%",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Extension configuration -------------------------------------------------

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

myst_enable_extensions = [
    "colon_fence",
]
myst_heading_anchors = 3


# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sqlalchemy": ("http://docs.sqlalchemy.org/en/stable", None),
}


# -- Misc -----


def run_apidoc(_):
    from sphinx.ext import apidoc

    apidoc.main(
        [
            "-f",
            "-o",
            os.path.join(topdir, "docs", "_source"),
            "-T",
            "-e",
            "-M",
            os.path.join(topdir, "webhook_to_fedora_messaging"),
            # exclude patterns:
            os.path.join(topdir, "webhook_to_fedora_messaging", "migrations"),
        ]
    )


github_url = "http://github.com/fedora-infra/webhook-to-fedora-messaging"


def changelog_github_links(app, docname, source):
    if docname != "release_notes":
        return
    github_issue_re = re.compile(r"#(\d+)")
    for docnr, doc in enumerate(source):
        source[docnr] = github_issue_re.sub(f"[#\\1]({github_url}/issues/\\1)", doc)


def setup(app):
    app.connect("builder-inited", run_apidoc)
    app.connect("source-read", changelog_github_links)
