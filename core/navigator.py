# core/navigator.py

import os
from datetime import datetime
from pathlib import Path

from core.breath_engine import take_breath

# Try to import signer if available
try:
    from tools import self_sign
    SIGNING_AVAILABLE = True
except ImportError:
    SIGNING_AVAILABLE = False

# Paths
BREATH_JOURNAL = Path("codex/breath_journal.md")
KEYS_DIR = Path("keys")
KEYS_DIR.mkdir(exist_ok=True)

def run_cycle(cycle_note: str, sign: bool = False):
    """
    Run a breath cycle:
    - Append a new entry to the breath journal
    - Optionally sign the entry using Ed25519
    """
    timestamp = datetime.utcnow().isoformat()

    # Write entry through breath_engine
    entry = take_breath(cycle_note)

    # Save entry into journal
    with open(BREATH_JOURNAL, "a") as f:
        f.write(entry + "\n")

    print(f"✅ Breath cycle recorded at {timestamp}")

    # Optional signing
    if sign and SIGNING_AVAILABLE:
        key_path = KEYS_DIR / "secret.key"
        pub_path = KEYS_DIR / "public.key"

        # If no keys exist, generate
        if not key_path.exists():
            sk_hex, pk_hex = self_sign.generate_keypair()
            key_path.write_text(sk_hex)
            pub_path.write_text(pk_hex)
            print("🔑 New keypair generated.")

        # Load secret key
        sk_hex = key_path.read_text().strip()
        signature = self_sign.sign_content(sk_hex, entry)

        # Append signature to the journal
        with open(BREATH_JOURNAL, "a") as f:
            f.write(f"\n**Signature:** {signature}\n---\n")

        print("📝 Entry signed with Ed25519.")

    elif sign:
        print("⚠️ Signing requested but self_sign.py not available.")

    return entry