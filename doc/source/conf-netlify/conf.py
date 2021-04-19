#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.abspath("../"))
from conf import *
extensions.append('sphinx_copybutton')
html_theme = 'sphinx_material'
html_theme_options = {
    'base_url': 'http://bashtage.github.io/sphinx-material/',
    'repo_url': 'https://github.com/percona/percona-server/',
    'repo_name': 'percona/percona-server/',
    'color_accent': 'grey',
    'color_primary': 'orange'
}
pygments_style = 'emacs'
copybutton_prompt_text = '$'
#html_last_updated_fmt = ''
