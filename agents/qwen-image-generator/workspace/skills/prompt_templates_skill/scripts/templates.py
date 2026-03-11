#!/usr/bin/env python3
"""
Manage prompt templates for image generation.
Templates are stored in templates.json in the current working directory.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

DEFAULT_DB = "templates.json"


def get_db_path() -> Path:
    """Get path to templates database."""
    return Path(os.environ.get("PROMPT_TEMPLATES_DB", DEFAULT_DB))


def load_templates(db_path: Optional[Path] = None) -> dict:
    """Load templates from database file."""
    path = db_path or get_db_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_templates(templates: dict, db_path: Optional[Path] = None) -> None:
    """Save templates to database file."""
    path = db_path or get_db_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(templates, f, indent=2, ensure_ascii=False)


def normalize_name(name: str) -> str:
    """Normalize template name (lowercase, trim)."""
    return name.lower().strip()


def cmd_list(db_path: Optional[Path] = None) -> None:
    """List all templates."""
    templates = load_templates(db_path)
    if not templates:
        print(json.dumps([], ensure_ascii=False))
        return

    result = []
    for name, data in templates.items():
        prompt = data.get("prompt", "")
        preview = prompt[:60] + "..." if len(prompt) > 60 else prompt
        result.append({"name": name, "preview": preview})

    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_get(name: str, db_path: Optional[Path] = None) -> None:
    """Get a template by name."""
    templates = load_templates(db_path)
    normalized = normalize_name(name)

    # Try exact match first, then case-insensitive
    if normalized in templates:
        data = templates[normalized]
        result = {"name": normalized, **data}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # Case-insensitive search
    for key, data in templates.items():
        if key.lower() == normalized:
            result = {"name": key, **data}
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return

    print(json.dumps(None))


def cmd_save(
    name: str,
    prompt: str,
    size: str = "1280*1280",
    model: str = "wan2.6-t2i",
    n: int = 1,
    negative: str = "",
    db_path: Optional[Path] = None,
) -> None:
    """Save a template."""
    templates = load_templates(db_path)
    normalized = normalize_name(name)

    templates[normalized] = {
        "prompt": prompt,
        "parameters": {"size": size, "model": model, "n": n},
    }
    if negative:
        templates[normalized]["parameters"]["negative_prompt"] = negative

    save_templates(templates, db_path)
    print(json.dumps({"saved": True, "name": normalized}))


def cmd_delete(name: str, db_path: Optional[Path] = None) -> None:
    """Delete a template."""
    templates = load_templates(db_path)
    normalized = normalize_name(name)

    # Try exact match
    if normalized in templates:
        del templates[normalized]
        save_templates(templates, db_path)
        print(json.dumps({"deleted": True}))
        return

    # Case-insensitive search
    for key in list(templates.keys()):
        if key.lower() == normalized:
            del templates[key]
            save_templates(templates, db_path)
            print(json.dumps({"deleted": True}))
            return

    print(json.dumps({"deleted": False, "reason": "not found"}))


def main():
    parser = argparse.ArgumentParser(description="Manage prompt templates")
    parser.add_argument(
        "--db", help="Path to templates database (default: templates.json)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # list
    subparsers.add_parser("list", help="List all templates")

    # get
    get_parser = subparsers.add_parser("get", help="Get a template by name")
    get_parser.add_argument("name", help="Template name")

    # save
    save_parser = subparsers.add_parser("save", help="Save a template")
    save_parser.add_argument("name", help="Template name")
    save_parser.add_argument("prompt", help="Prompt text")
    save_parser.add_argument(
        "--size", default="1280*1280", help="Image size (default: 1280*1280)"
    )
    save_parser.add_argument(
        "--model", default="wan2.6-t2i", help="Model (default: wan2.6-t2i)"
    )
    save_parser.add_argument(
        "--n", type=int, default=1, help="Number of images (default: 1)"
    )
    save_parser.add_argument("--negative", default="", help="Negative prompt")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a template")
    delete_parser.add_argument("name", help="Template name")

    args = parser.parse_args()

    db_path = Path(args.db) if args.db else None

    if args.command == "list":
        cmd_list(db_path)
    elif args.command == "get":
        cmd_get(args.name, db_path)
    elif args.command == "save":
        cmd_save(
            args.name,
            args.prompt,
            args.size,
            args.model,
            args.n,
            args.negative,
            db_path,
        )
    elif args.command == "delete":
        cmd_delete(args.name, db_path)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
