from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def main() -> None:
    context_path = Path(required_env("DYNAMIC_MODULES_PREPARE_CONTEXT"))
    output_path = Path(required_env("DYNAMIC_MODULES_PREPARE_OUTPUT"))
    host_root = Path(required_env("DYNAMIC_MODULES_HOST_ROOT"))
    build_dir = Path(required_env("DYNAMIC_MODULES_BUILD_DIR"))
    module_id = os.environ.get("DYNAMIC_MODULES_PREPARE_PLUGIN_MODULE", "dynamic-assets")

    context = json.loads(context_path.read_text(encoding="utf-8"))
    asset_index_path = build_dir / "assets" / "index.json"
    asset_index = {
        "api_version": 1,
        "load_order": context.get("load_order", []),
        "modules": {
            item_id: {
                "asset_files": item.get("asset_files", []),
                "patterns": item.get("build", {}).get("assets", []),
            }
            for item_id, item in context.get("modules", {}).items()
            if item.get("asset_files") or item.get("build", {}).get("assets")
        },
    }
    write_json(asset_index_path, asset_index)

    write_json(
        output_path,
        {
            "generated": {
                "dynamic_assets_index_file": relative_to_host(host_root, asset_index_path),
            },
            "modules": {
                module_id: {
                    "dynamic_assets": {
                        "api_version": 1,
                        "capabilities": ["asset_metadata_index"],
                    },
                },
            },
        },
    )


def required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


def relative_to_host(host_root: Path, path: Path) -> str:
    return path.resolve().relative_to(host_root.resolve()).as_posix()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
