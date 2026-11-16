"""Usage: python3 build_package.py ThemeFolder"""
from pathlib import Path
import base64
import hashlib
import json
import sys


def build(folder):
    folder = Path(folder).resolve()
    manifest = json.loads((folder / "theme.json").read_text())
    files = {}
    total = 0
    for key, asset in manifest["assets"].items():
        path = asset["path"]
        parts = path.split("/")
        if any(not p or p in (".", "..") for p in parts) or any(c in path for c in "\\%:?#~"):
            raise ValueError(f"Unsafe media path: {path}")
        file = (folder / path).resolve()
        if not file.is_relative_to(folder) or file.is_symlink():
            raise ValueError(f"Media left its theme folder: {path}")
        data = file.read_bytes()
        limit = 8_000_000 if asset["kind"] == "image" else 12_000_000
        if not 0 < len(data) <= limit:
            raise ValueError(f"Media exceeds size limit: {path}")
        total += len(data)
        if total > 50_000_000:
            raise ValueError("Theme exceeds 50 MB")
        asset["bytes"] = len(data)
        asset["sha256"] = hashlib.sha256(data).hexdigest()
        files[key] = base64.b64encode(data).decode()
    (folder / "theme.json").write_text(json.dumps(manifest, indent=2) + "\n")
    destination = folder.with_suffix(".soundboardtheme")
    destination.write_text(json.dumps(dict(manifest=manifest, files=files), separators=(",", ":")))
    print(destination.name, f"({total:,} bytes of media)")


if __name__ == "__main__":
    build(sys.argv[1])
