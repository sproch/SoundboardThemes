"""Check public theme manifests and file hashes before uploading to GitHub."""
from pathlib import Path
import hashlib
import json
import re


def validate(path):
    theme = json.loads(path.read_text())
    assert theme["schemaVersion"] == 1
    assert re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,79}", theme["id"]) and ".." not in theme["id"]
    assert isinstance(theme["version"], int) and theme["version"] > 0
    assert theme["name"] and theme["author"] and theme["license"]
    buttons = theme["buttons"]
    assert 1 <= len(buttons) <= 24 and len({b["id"] for b in buttons}) == len(buttons)
    if theme["appearance"]["layout"] == "radial":
        assert 2 <= len(buttons) <= 8
    for button in buttons:
        assert theme["assets"][button["sound"]]["kind"] == "audio"
        if button.get("image"):
            assert theme["assets"][button["image"]]["kind"] == "image"
    total = 0
    seen = set()
    for asset in theme["assets"].values():
        relative = asset["path"]
        assert relative not in seen
        seen.add(relative)
        assert not relative.startswith("/") and all(p and p not in (".", "..") for p in relative.split("/"))
        assert not any(c in relative for c in "\\%:?#~")
        file = path.parent / relative
        assert not file.is_symlink() and file.resolve().is_relative_to(path.parent.resolve())
        extensions = {"image": {".png", ".jpg", ".jpeg"}, "audio": {".wav", ".m4a", ".mp3", ".caf"}}
        assert file.suffix.lower() in extensions[asset["kind"]]
        data = file.read_bytes()
        assert len(data) == asset["bytes"]
        assert hashlib.sha256(data).hexdigest() == asset["sha256"]
        total += len(data)
    assert total <= 50_000_000
    print(f"OK: {theme['name']} · {len(buttons)} buttons · {total:,} bytes")


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    manifests = list(root.glob("*/theme.json"))
    assert manifests, "No themes found"
    for manifest in manifests:
        validate(manifest)
