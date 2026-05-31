#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data models for CodeSnap
"""

import uuid
import hashlib
from datetime import datetime
from typing import List, Optional, Dict, Any
import yaml


class Snippet:
    """Represents a code snippet with metadata."""
    
    def __init__(
        self,
        title: str,
        code: str,
        language: str = 'text',
        description: str = '',
        tags: List[str] = None,
        source: str = '',
        snippet_id: str = None,
        created_at: str = None,
        updated_at: str = None,
        usage_count: int = 0
    ):
        self.id = snippet_id or self._generate_id(code)
        self.title = title
        self.code = code
        self.language = language.lower()
        self.description = description
        self.tags = tags or []
        self.source = source
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or self.created_at
        self.usage_count = usage_count
    
    @staticmethod
    def _generate_id(code: str) -> str:
        """Generate a unique ID based on code content and timestamp."""
        content = f"{code}{datetime.now().timestamp()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert snippet to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'code': self.code,
            'language': self.language,
            'description': self.description,
            'tags': self.tags,
            'source': self.source,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'usage_count': self.usage_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Snippet':
        """Create snippet from dictionary."""
        return cls(
            snippet_id=data.get('id'),
            title=data.get('title', ''),
            code=data.get('code', ''),
            language=data.get('language', 'text'),
            description=data.get('description', ''),
            tags=data.get('tags', []),
            source=data.get('source', ''),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            usage_count=data.get('usage_count', 0)
        )
    
    def to_yaml(self) -> str:
        """Export snippet as YAML string."""
        return yaml.dump(self.to_dict(), allow_unicode=True, sort_keys=False)
    
    @classmethod
    def from_yaml(cls, yaml_str: str) -> 'Snippet':
        """Create snippet from YAML string."""
        data = yaml.safe_load(yaml_str)
        return cls.from_dict(data)
    
    def increment_usage(self):
        """Increment usage counter."""
        self.usage_count += 1
        self.updated_at = datetime.now().isoformat()
    
    def matches_search(self, query: str) -> bool:
        """Check if snippet matches search query."""
        query = query.lower()
        searchable_text = f"{self.title} {self.description} {self.code} {' '.join(self.tags)}"
        return query in searchable_text.lower()
    
    def __repr__(self) -> str:
        return f"<Snippet(id={self.id[:8]}, title='{self.title}', lang={self.language})>"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Snippet):
            return False
        return self.id == other.id
