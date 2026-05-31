#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line interface for CodeSnap
"""

import sys
import os
import tempfile
import subprocess
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich import box
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from .core import SnippetManager
from .models import Snippet


console = Console()


def get_manager() -> SnippetManager:
    """Get snippet manager instance."""
    data_dir = os.environ.get('CODESNAP_DATA_DIR')
    return SnippetManager(data_dir)


@click.group()
@click.version_option(version='1.0.0', prog_name='codesnap')
def cli():
    """🚀 CodeSnap - A blazing fast terminal code snippet manager
    
    Manage your code snippets directly from the terminal.
    Quick, efficient, and developer-friendly.
    
    Aliases: codesnap, csp
    """
    pass


@cli.command()
@click.option('--title', '-t', prompt='Title', help='Snippet title')
@click.option('--code', '-c', help='Code content (or use --file, --editor, --stdin)')
@click.option('--file', '-f', type=click.Path(exists=True), help='Read code from file')
@click.option('--language', '-l', default='auto', help='Programming language (auto-detected if not specified)')
@click.option('--description', '-d', default='', help='Snippet description')
@click.option('--tags', help='Comma-separated tags')
@click.option('--source', '-s', default='', help='Source URL or reference')
@click.option('--editor', '-e', is_flag=True, help='Open editor to input code')
@click.option('--stdin', 'use_stdin', is_flag=True, help='Read code from stdin')
def add(title, code, file, language, description, tags, source, editor, use_stdin):
    """➕ Add a new code snippet"""
    manager = get_manager()
    
    # Get code content
    if file:
        with open(file, 'r') as f:
            code = f.read()
        if language == 'auto':
            # Try to detect from file extension
            ext = os.path.splitext(file)[1].lower()
            ext_map = {
                '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
                '.sh': 'bash', '.bash': 'bash', '.zsh': 'zsh',
                '.go': 'go', '.rs': 'rust', '.java': 'java',
                '.cpp': 'cpp', '.c': 'c', '.h': 'c',
                '.rb': 'ruby', '.php': 'php', '.sql': 'sql',
                '.html': 'html', '.css': 'css', '.json': 'json',
                '.yaml': 'yaml', '.yml': 'yaml', '.md': 'markdown',
            }
            language = ext_map.get(ext, 'auto')
    elif use_stdin:
        code = sys.stdin.read()
    elif editor:
        code = click.edit('')
        if code is None:
            console.print("[yellow]Cancelled.[/yellow]")
            return
    elif not code:
        console.print("[yellow]Please provide code using --code, --file, --editor, or --stdin[/yellow]")
        return
    
    if not code or not code.strip():
        console.print("[red]Error: Code content cannot be empty[/red]")
        return
    
    # Parse tags
    tag_list = [t.strip() for t in tags.split(',')] if tags else []
    
    # Auto-suggest tags if none provided
    if not tag_list:
        tag_list = manager.suggest_tags(title, code, description)
        if tag_list:
            console.print(f"[dim]Suggested tags: {', '.join(tag_list)}[/dim]")
            use_suggested = click.confirm("Use suggested tags?", default=True)
            if not use_suggested:
                tag_list = []
    
    snippet = manager.add_snippet(
        title=title,
        code=code,
        language=language,
        description=description,
        tags=tag_list,
        source=source
    )
    
    if snippet:
        console.print(f"[green]✓[/green] Snippet added successfully!")
        console.print(f"  ID: [cyan]{snippet.id}[/cyan]")
        console.print(f"  Title: [bold]{snippet.title}[/bold]")
        console.print(f"  Language: [yellow]{snippet.language}[/yellow]")
        if snippet.tags:
            console.print(f"  Tags: [magenta]{', '.join(snippet.tags)}[/magenta]")
    else:
        console.print("[red]✗ Failed to add snippet[/red]")


@cli.command()
@click.argument('query', default='')
@click.option('--language', '-l', help='Filter by language')
@click.option('--tag', multiple=True, help='Filter by tag (can be used multiple times)')
@click.option('--limit', '-n', default=20, help='Maximum number of results')
def search(query, language, tag, limit):
    """🔍 Search for code snippets"""
    manager = get_manager()
    
    tags = list(tag) if tag else None
    
    if not query and not language and not tags:
        # List all if no query
        snippets = manager.list_snippets(language=language, tags=tags, limit=limit)
        results = [(s, 0) for s in snippets]
    else:
        results = manager.search_snippets(query, language=language, tags=tags, limit=limit)
    
    if not results:
        console.print("[yellow]No snippets found.[/yellow]")
        return
    
    table = Table(box=box.ROUNDED, show_header=True)
    table.add_column("ID", style="cyan", width=12)
    table.add_column("Title", style="bold")
    table.add_column("Language", style="yellow", width=12)
    table.add_column("Tags", style="magenta")
    table.add_column("Score", style="dim", width=8)
    
    for snippet, score in results:
        tags_str = ', '.join(snippet.tags[:3]) if snippet.tags else ''
        score_str = f"{score}%" if score > 0 else '-'
        table.add_row(
            snippet.id[:8],
            snippet.title[:40],
            snippet.language,
            tags_str[:25],
            score_str
        )
    
    console.print(table)
    console.print(f"\n[dim]Found {len(results)} snippet(s)[/dim]")


@cli.command(name='list')
@click.option('--language', '-l', help='Filter by language')
@click.option('--tag', multiple=True, help='Filter by tag')
@click.option('--sort', '-s', default='created', 
              type=click.Choice(['created', 'updated', 'usage', 'title']),
              help='Sort by field')
@click.option('--limit', '-n', default=20, help='Maximum number of results')
def list_snippets(language, tag, sort, limit):
    """📋 List all code snippets"""
    manager = get_manager()
    tags = list(tag) if tag else None
    
    snippets = manager.list_snippets(
        language=language,
        tags=tags,
        sort_by=sort,
        limit=limit
    )
    
    if not snippets:
        console.print("[yellow]No snippets found.[/yellow]")
        return
    
    table = Table(box=box.ROUNDED, show_header=True)
    table.add_column("ID", style="cyan", width=12)
    table.add_column("Title", style="bold")
    table.add_column("Language", style="yellow", width=12)
    table.add_column("Tags", style="magenta")
    table.add_column("Used", style="dim", width=6)
    table.add_column("Updated", style="dim", width=10)
    
    for snippet in snippets:
        tags_str = ', '.join(snippet.tags[:2]) if snippet.tags else ''
        updated = snippet.updated_at[:10] if snippet.updated_at else '-'
        table.add_row(
            snippet.id[:8],
            snippet.title[:35],
            snippet.language,
            tags_str[:20],
            str(snippet.usage_count),
            updated
        )
    
    console.print(table)
    console.print(f"\n[dim]Showing {len(snippets)} snippet(s)[/dim]")


@cli.command()
@click.argument('snippet_id')
def show(snippet_id):
    """👁️  Display a snippet with syntax highlighting"""
    manager = get_manager()
    
    # Try to find by partial ID
    snippet = manager.get_snippet(snippet_id)
    if not snippet:
        # Search for partial match
        results = manager.search_snippets(snippet_id, limit=1)
        if results:
            snippet = results[0][0]
        else:
            console.print(f"[red]Snippet not found: {snippet_id}[/red]")
            return
    
    # Display snippet
    console.print(Panel(
        f"[bold]{snippet.title}[/bold]\n"
        f"[dim]ID:[/dim] {snippet.id}\n"
        f"[dim]Language:[/dim] {snippet.language}\n"
        f"[dim]Created:[/dim] {snippet.created_at[:19]}\n"
        f"[dim]Updated:[/dim] {snippet.updated_at[:19]}\n"
        f"[dim]Usage:[/dim] {snippet.usage_count} times",
        title="📄 Snippet Info",
        border_style="blue"
    ))
    
    if snippet.description:
        console.print(f"\n[italic]{snippet.description}[/italic]\n")
    
    if snippet.tags:
        console.print(f"Tags: [magenta]{', '.join(snippet.tags)}[/magenta]\n")
    
    # Code with syntax highlighting
    syntax = Syntax(
        snippet.code,
        snippet.language if snippet.language != 'text' else 'text',
        theme="monokai",
        line_numbers=True,
        word_wrap=True
    )
    console.print(Panel(syntax, border_style="green"))
    
    if snippet.source:
        console.print(f"\n[dim]Source: {snippet.source}[/dim]")


@cli.command()
@click.argument('snippet_id')
def copy(snippet_id):
    """📋 Copy snippet to clipboard"""
    manager = get_manager()
    
    snippet = manager.get_snippet(snippet_id)
    if not snippet:
        results = manager.search_snippets(snippet_id, limit=1)
        if results:
            snippet = results[0][0]
        else:
            console.print(f"[red]Snippet not found: {snippet_id}[/red]")
            return
    
    if manager.copy_to_clipboard(snippet.id):
        console.print(f"[green]✓[/green] Copied to clipboard: [bold]{snippet.title}[/bold]")
    else:
        console.print("[red]✗ Failed to copy to clipboard[/red]")


@cli.command()
@click.argument('snippet_id')
@click.option('--shell', '-s', default='bash', help='Shell to use for execution')
def run(snippet_id, shell):
    """▶️  Execute a snippet"""
    manager = get_manager()
    
    snippet = manager.get_snippet(snippet_id)
    if not snippet:
        results = manager.search_snippets(snippet_id, limit=1)
        if results:
            snippet = results[0][0]
        else:
            console.print(f"[red]Snippet not found: {snippet_id}[/red]")
            return
    
    console.print(f"[dim]Executing: {snippet.title} ({snippet.language})[/dim]\n")
    
    success, output = manager.execute_snippet(snippet.id, shell)
    
    if output:
        console.print(output)
    
    if success:
        console.print("\n[green]✓ Execution completed[/green]")
    else:
        console.print("\n[red]✗ Execution failed[/red]")


@cli.command()
@click.argument('snippet_id')
@click.option('--title', '-t', help='New title')
@click.option('--code', '-c', help='New code')
@click.option('--language', '-l', help='New language')
@click.option('--description', '-d', help='New description')
@click.option('--tags', help='New comma-separated tags')
@click.option('--editor', '-e', is_flag=True, help='Open editor to modify code')
def edit(snippet_id, title, code, language, description, tags, editor):
    """✏️  Edit an existing snippet"""
    manager = get_manager()
    
    snippet = manager.get_snippet(snippet_id)
    if not snippet:
        results = manager.search_snippets(snippet_id, limit=1)
        if results:
            snippet = results[0][0]
        else:
            console.print(f"[red]Snippet not found: {snippet_id}[/red]")
            return
    
    if editor:
        code = click.edit(snippet.code)
        if code is None:
            console.print("[yellow]Cancelled.[/yellow]")
            return
    
    tag_list = [t.strip() for t in tags.split(',')] if tags else None
    
    success = manager.update_snippet(
        snippet.id,
        title=title,
        code=code,
        language=language,
        description=description,
        tags=tag_list
    )
    
    if success:
        console.print(f"[green]✓[/green] Snippet updated: [bold]{snippet.title}[/bold]")
    else:
        console.print("[red]✗ Failed to update snippet[/red]")


@cli.command()
@click.argument('snippet_id')
@click.confirmation_option(prompt='Are you sure you want to delete this snippet?')
def delete(snippet_id):
    """🗑️  Delete a snippet"""
    manager = get_manager()
    
    snippet = manager.get_snippet(snippet_id)
    if not snippet:
        results = manager.search_snippets(snippet_id, limit=1)
        if results:
            snippet = results[0][0]
        else:
            console.print(f"[red]Snippet not found: {snippet_id}[/red]")
            return
    
    if manager.delete_snippet(snippet.id):
        console.print(f"[green]✓[/green] Deleted: [bold]{snippet.title}[/bold]")
    else:
        console.print("[red]✗ Failed to delete snippet[/red]")


@cli.command()
def stats():
    """📊 Show statistics"""
    manager = get_manager()
    stats = manager.get_stats()
    
    console.print(Panel(
        f"[bold]Total Snippets:[/bold] {stats['total_snippets']}\n"
        f"[bold]Total Usage:[/bold] {stats['total_usage']}\n"
        f"[bold]Storage Path:[/bold] {stats['storage_path']}",
        title="📈 Statistics",
        border_style="blue"
    ))
    
    if stats['languages']:
        console.print("\n[bold]Languages:[/bold]")
        for lang, count in sorted(stats['languages'].items(), key=lambda x: x[1], reverse=True):
            console.print(f"  {lang}: {count}")


@cli.command(name='export')
@click.argument('output_file')
def export_snippets(output_file):
    """📤 Export snippets to JSON file"""
    manager = get_manager()
    
    if manager.export_snippets(output_file):
        console.print(f"[green]✓[/green] Exported to: [bold]{output_file}[/bold]")
    else:
        console.print("[red]✗ Export failed[/red]")


@cli.command(name='import')
@click.argument('input_file')
@click.option('--merge/--replace', default=True, help='Merge with existing or replace')
def import_snippets(input_file, merge):
    """📥 Import snippets from JSON file"""
    manager = get_manager()
    
    if not os.path.exists(input_file):
        console.print(f"[red]File not found: {input_file}[/red]")
        return
    
    count = manager.import_snippets(input_file, merge=merge)
    console.print(f"[green]✓[/green] Imported [bold]{count}[/bold] snippet(s)")


@cli.command()
def languages():
    """🌐 List all languages used in snippets"""
    manager = get_manager()
    languages = manager.get_languages()
    
    if not languages:
        console.print("[yellow]No snippets found.[/yellow]")
        return
    
    console.print("[bold]Languages:[/bold]")
    for lang in languages:
        console.print(f"  • {lang}")


@cli.command()
def tags():
    """🏷️  List all tags used in snippets"""
    manager = get_manager()
    tags = manager.get_all_tags()
    
    if not tags:
        console.print("[yellow]No tags found.[/yellow]")
        return
    
    console.print("[bold]Tags:[/bold]")
    for tag in tags:
        console.print(f"  • {tag}")


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()
