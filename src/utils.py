import hashlib


def _hash_pwd(raw: str) -> str:
    """Very light SHA‑256 hash helper (demo only)."""
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
