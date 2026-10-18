"""Prepare Flask's source assets for Vercel's static CDN."""
from pathlib import Path
from shutil import copytree

BASE = Path(__file__).resolve().parent


def build_assets(destination=None):
    target = Path(destination) if destination else BASE / "public" / "static"
    copytree(BASE / "static", target, dirs_exist_ok=True)
    return target


if __name__ == "__main__":
    build_assets()
    print("Prepared public/static for Vercel CDN.")
