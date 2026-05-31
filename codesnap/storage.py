#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Storage backend for CodeSnap snippets
"""

import os
import json
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
import yaml

from .models import Snippet


class SnippetStorage:
    """Manages persistent storage of code snippets."""
    
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = Path.home() / '.codesnap'
        
        self.snippets_dir = self.data_dir / 'snippets'
        self.config_file = self.data_dir / 'config.yaml'
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.snippets_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_snippet_path(self, snippet_id: str) -> Path:
        """Get file path for a snippet."""
        return self.snippets_dir / f"{snippet_id}.yaml"
    
    def save(self, snippet: Snippet) -> bool:
        """Save a snippet to storage."""
        try:
            snippet_path = self._get_snippet_path(snippet.id)
            with open(snippet_path, 'w', encoding='utf-8') as f:
                f.write(snippet.to_yaml())
            return True
        except Exception as e:
            print(f"Error saving snippet: {e}")
            return False
    
    def load(self, snippet_id: str) -> Optional[Snippet]:
        """Load a snippet by ID."""
        snippet_path = self._get_snippet_path(snippet_id)
        if not snippet_path.exists():
            return None
        
        try:
            with open(snippet_path, 'r', encoding='utf-8') as f:
                return Snippet.from_yaml(f.read())
        except Exception as e:
            print(f"Error loading snippet: {e}")
            return None
    
    def load_all(self) -> List[Snippet]:
        """Load all snippets from storage."""
        snippets = []
        for snippet_file in self.snippets_dir.glob('*.yaml'):
            try:
                with open(snippet_file, 'r', encoding='utf-8') as f:
                    snippet = Snippet.from_yaml(f.read())
                    snippets.append(snippet)
            except Exception as e:
                print(f"Error loading {snippet_file}: {e}")
        return snippets
    
    def delete(self, snippet_id: str) -> bool:
        """Delete a snippet by ID."""
        snippet_path = self._get_snippet_path(snippet_id)
        if snippet_path.exists():
            snippet_path.unlink()
            return True
        return False
    
    def exists(self, snippet_id: str) -> bool:
        """Check if a snippet exists."""
        return self._get_snippet_path(snippet_id).exists()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        snippets = self.load_all()
        languages = {}
        total_usage = 0
        
        for snippet in snippets:
            languages[snippet.language] = languages.get(snippet.language, 0) + 1
            total_usage += snippet.usage_count
        
        return {
            'total_snippets': len(snippets),
            'languages': languages,
            'total_usage': total_usage,
            'storage_path': str(self.data_dir)
        }
    
    def export_to_json(self, output_path: str) -> bool:
        """Export all snippets to JSON file."""
        try:
            snippets = self.load_all()
            data = {
                'export_date': __import__('datetime').datetime.now().isoformat(),
                'version': '1.0.0',
                'snippets': [s.to_dict() for s in snippets]
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting: {e}")
            return False
    
    def import_from_json(self, input_path: str, merge: bool = True) -> int:
        """Import snippets from JSON file."""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            imported = 0
            for snippet_data in data.get('snippets', []):
                snippet = Snippet.from_dict(snippet_data)
                if not merge and self.exists(snippet.id):
                    continue
                if self.save(snippet):
                    imported += 1
            return imported
        except Exception as e:
            print(f"Error importing: {e}")
            return 0
    
    def backup(self, backup_dir: Optional[str] = None) -> str:
        """Create a backup of all snippets."""
        if backup_dir is None:
            backup_dir = self.data_dir / 'backups'
        else:
            backup_dir = Path(backup_dir)
        
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = backup_dir / f"codesnap_backup_{timestamp}"
        
        shutil.copytree(self.snippets_dir, backup_path / 'snippets')
        return str(backup_path)
