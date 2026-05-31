#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core functionality for CodeSnap
"""

import os
import re
import subprocess
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from fuzzywuzzy import fuzz, process

from .models import Snippet
from .storage import SnippetStorage


class SnippetManager:
    """Main manager class for code snippets."""
    
    # Language detection patterns
    LANGUAGE_PATTERNS = {
        'python': [r'\bdef\s+\w+\s*\(', r'\bimport\s+\w+', r'\bprint\s*\(', r'\bclass\s+\w+.*:', r':\s*$'],
        'javascript': [r'\bconst\s+\w+\s*=', r'\blet\s+\w+\s*=', r'\bvar\s+\w+\s*=', r'\bfunction\s+\w*\s*\(', r'=>\s*\{'],
        'typescript': [r'\binterface\s+\w+', r'\btype\s+\w+\s*=', r':\s*(string|number|boolean)\b', r'\bexport\s+\b'],
        'bash': [r'^#!/bin/bash', r'^#!/bin/sh', r'\becho\s+', r'\bif\s+\[.*\]', r'\bfor\s+\w+\s+in'],
        'sql': [r'\bSELECT\s+', r'\bINSERT\s+INTO\b', r'\bUPDATE\s+\w+\s+SET', r'\bCREATE\s+TABLE\b'],
        'html': [r'<\w+[^>]*>', r'</\w+>', r'<!DOCTYPE', r'<html'],
        'css': [r'\.[\w-]+\s*\{', r'#\w+\s*\{', r'@media\s+', r'\{[^}]*:\s*[^;]+;'],
        'json': [r'^\s*\{', r'^\s*\[', r'"\w+"\s*:\s*'],
        'yaml': [r'^\w+:\s*', r'^-\s+\w+', r'^---\s*$'],
        'go': [r'\bfunc\s+\w+', r'\bpackage\s+\w+', r'\bimport\s+\(', r'\bgo\s+\b'],
        'rust': [r'\bfn\s+\w+', r'\buse\s+\w+', r'\bimpl\s+', r'\bstruct\s+\w+', r'\benum\s+\w+'],
        'java': [r'\bpublic\s+class\b', r'\bprivate\s+\w+', r'\bSystem\.out\.print', r'\bimport\s+java\.'],
        'cpp': [r'#include\s*<', r'\bstd::', r'\bint\s+main\s*\(', r'\bcout\s*<<'],
        'ruby': [r'\bdef\s+\w+', r'\bend\s*$', r'\bputs\s+', r'\brequire\s+[\'"]'],
        'php': [r'<\?php', r'\$\w+\s*=', r'\becho\s+', r'\bfunction\s+\w+'],
    }
    
    def __init__(self, data_dir: Optional[str] = None):
        self.storage = SnippetStorage(data_dir)
        self._snippets_cache: Optional[List[Snippet]] = None
    
    def _invalidate_cache(self):
        """Invalidate the snippets cache."""
        self._snippets_cache = None
    
    def _get_all_snippets(self) -> List[Snippet]:
        """Get all snippets (with caching)."""
        if self._snippets_cache is None:
            self._snippets_cache = self.storage.load_all()
        return self._snippets_cache
    
    def detect_language(self, code: str) -> str:
        """Auto-detect programming language from code."""
        scores = {}
        for lang, patterns in self.LANGUAGE_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, code, re.MULTILINE | re.IGNORECASE):
                    score += 1
            if score > 0:
                scores[lang] = score
        
        if scores:
            return max(scores, key=scores.get)
        return 'text'
    
    def suggest_tags(self, title: str, code: str, description: str = '') -> List[str]:
        """Suggest tags based on content."""
        tags = set()
        content = f"{title} {code} {description}".lower()
        
        # Language-based tags
        lang = self.detect_language(code)
        if lang != 'text':
            tags.add(lang)
        
        # Common tag patterns
        tag_patterns = {
            'algorithm': ['sort', 'search', 'tree', 'graph', 'recursive', 'dynamic programming'],
            'web': ['http', 'api', 'rest', 'json', 'ajax', 'fetch', 'axios'],
            'database': ['sql', 'query', 'database', 'mongo', 'redis', 'postgresql'],
            'devops': ['docker', 'kubernetes', 'k8s', 'ci/cd', 'pipeline', 'deploy'],
            'frontend': ['react', 'vue', 'angular', 'dom', 'css', 'html'],
            'backend': ['server', 'api', 'route', 'middleware', 'auth'],
            'utility': ['helper', 'util', 'tool', 'function', 'common'],
            'cli': ['command', 'terminal', 'shell', 'bash', 'script'],
            'test': ['test', 'mock', 'jest', 'pytest', 'unittest'],
            'config': ['config', 'setup', 'init', 'settings'],
        }
        
        for tag, keywords in tag_patterns.items():
            if any(kw in content for kw in keywords):
                tags.add(tag)
        
        return list(tags)[:5]  # Limit to 5 tags
    
    def add_snippet(
        self,
        title: str,
        code: str,
        language: Optional[str] = None,
        description: str = '',
        tags: Optional[List[str]] = None,
        source: str = ''
    ) -> Optional[Snippet]:
        """Add a new snippet."""
        if not language or language == 'auto':
            language = self.detect_language(code)
        
        snippet = Snippet(
            title=title,
            code=code,
            language=language,
            description=description,
            tags=tags or [],
            source=source
        )
        
        if self.storage.save(snippet):
            self._invalidate_cache()
            return snippet
        return None
    
    def get_snippet(self, snippet_id: str) -> Optional[Snippet]:
        """Get a snippet by ID."""
        return self.storage.load(snippet_id)
    
    def update_snippet(
        self,
        snippet_id: str,
        title: Optional[str] = None,
        code: Optional[str] = None,
        language: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """Update an existing snippet."""
        snippet = self.get_snippet(snippet_id)
        if not snippet:
            return False
        
        if title is not None:
            snippet.title = title
        if code is not None:
            snippet.code = code
        if language is not None:
            snippet.language = language
        if description is not None:
            snippet.description = description
        if tags is not None:
            snippet.tags = tags
        
        snippet.updated_at = datetime.now().isoformat()
        
        if self.storage.save(snippet):
            self._invalidate_cache()
            return True
        return False
    
    def delete_snippet(self, snippet_id: str) -> bool:
        """Delete a snippet."""
        if self.storage.delete(snippet_id):
            self._invalidate_cache()
            return True
        return False
    
    def search_snippets(
        self,
        query: str,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 20
    ) -> List[Tuple[Snippet, int]]:
        """Search snippets with fuzzy matching."""
        snippets = self._get_all_snippets()
        results = []
        
        query_lower = query.lower()
        
        for snippet in snippets:
            # Filter by language
            if language and snippet.language != language.lower():
                continue
            
            # Filter by tags
            if tags and not any(tag in snippet.tags for tag in tags):
                continue
            
            # Calculate relevance score
            score = 0
            
            # Exact matches get higher scores
            if query_lower in snippet.title.lower():
                score += 100
            if query_lower in snippet.description.lower():
                score += 50
            if query_lower in snippet.code.lower():
                score += 30
            if any(query_lower in tag.lower() for tag in snippet.tags):
                score += 80
            
            # Fuzzy matching
            title_score = fuzz.partial_ratio(query_lower, snippet.title.lower())
            score += title_score * 0.5
            
            if score > 20:  # Minimum threshold
                results.append((snippet, int(score)))
        
        # Sort by score descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]
    
    def list_snippets(
        self,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None,
        sort_by: str = 'created',
        limit: int = 50
    ) -> List[Snippet]:
        """List snippets with optional filtering."""
        snippets = self._get_all_snippets()
        
        # Filter by language
        if language:
            snippets = [s for s in snippets if s.language == language.lower()]
        
        # Filter by tags
        if tags:
            snippets = [s for s in snippets if any(tag in s.tags for tag in tags)]
        
        # Sort
        if sort_by == 'created':
            snippets.sort(key=lambda s: s.created_at, reverse=True)
        elif sort_by == 'updated':
            snippets.sort(key=lambda s: s.updated_at, reverse=True)
        elif sort_by == 'usage':
            snippets.sort(key=lambda s: s.usage_count, reverse=True)
        elif sort_by == 'title':
            snippets.sort(key=lambda s: s.title.lower())
        
        return snippets[:limit]
    
    def get_languages(self) -> List[str]:
        """Get list of all languages used in snippets."""
        snippets = self._get_all_snippets()
        languages = set(s.language for s in snippets)
        return sorted(languages)
    
    def get_all_tags(self) -> List[str]:
        """Get list of all tags used in snippets."""
        snippets = self._get_all_snippets()
        tags = set()
        for snippet in snippets:
            tags.update(snippet.tags)
        return sorted(tags)
    
    def copy_to_clipboard(self, snippet_id: str) -> bool:
        """Copy snippet code to clipboard."""
        import pyperclip
        
        snippet = self.get_snippet(snippet_id)
        if not snippet:
            return False
        
        try:
            pyperclip.copy(snippet.code)
            snippet.increment_usage()
            self.storage.save(snippet)
            return True
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            return False
    
    def execute_snippet(self, snippet_id: str, shell: str = 'bash') -> Tuple[bool, str]:
        """Execute a snippet in shell."""
        snippet = self.get_snippet(snippet_id)
        if not snippet:
            return False, "Snippet not found"
        
        # Security check - only allow certain languages
        executable_languages = ['bash', 'sh', 'shell', 'python', 'python3', 'ruby', 'node']
        if snippet.language not in executable_languages:
            return False, f"Cannot execute {snippet.language} code (only: {', '.join(executable_languages)})"
        
        try:
            if snippet.language in ['python', 'python3']:
                result = subprocess.run(
                    ['python3', '-c', snippet.code],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            elif snippet.language in ['bash', 'sh', 'shell']:
                result = subprocess.run(
                    snippet.code,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            else:
                return False, f"Execution not implemented for {snippet.language}"
            
            snippet.increment_usage()
            self.storage.save(snippet)
            
            output = result.stdout
            if result.stderr:
                output += f"\n[stderr]: {result.stderr}"
            
            return result.returncode == 0, output
            
        except subprocess.TimeoutExpired:
            return False, "Execution timed out (30s limit)"
        except Exception as e:
            return False, f"Execution error: {e}"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        return self.storage.get_stats()
    
    def export_snippets(self, output_path: str) -> bool:
        """Export all snippets to file."""
        return self.storage.export_to_json(output_path)
    
    def import_snippets(self, input_path: str, merge: bool = True) -> int:
        """Import snippets from file."""
        count = self.storage.import_from_json(input_path, merge)
        if count > 0:
            self._invalidate_cache()
        return count
