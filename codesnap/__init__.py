#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeSnap - A blazing fast terminal code snippet manager

A powerful CLI tool for managing code snippets directly from your terminal.
Supports adding, searching, copying, and executing code snippets with ease.
"""

__version__ = '1.0.0'
__author__ = 'CodeSnap Team'
__email__ = 'hello@codesnap.dev'
__license__ = 'MIT'
__url__ = 'https://github.com/yourusername/codesnap-cli'

from .core import SnippetManager
from .models import Snippet

__all__ = ['SnippetManager', 'Snippet']
