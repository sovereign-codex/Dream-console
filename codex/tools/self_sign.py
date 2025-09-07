# tools/self_sign.py
import nacl.signing
import nacl.encoding
from pathlib import Path

def generate_keypair():
    sk = nacl.signing.SigningKey.generate()
    pk = sk.verify_key
    return (
        sk.encode(encoder=nacl.encoding.HexEncoder).decode("utf-8"),
        pk.encode(encoder=nacl.encoding.HexEncoder).decode("utf-8")
    )

def sign_content(sk_hex: str, content: str) -> str:
    sk = nacl.signing.SigningKey(sk_hex, encoder=nacl.encoding.HexEncoder)
    signed = sk.sign(content.encode("utf-8"))
    return nacl.encoding.HexEncoder.encode(signed.signature).decode("utf-8")

def verify_content(pk_hex: str, content: str, signature: str) -> bool:
    pk = nacl.signing.VerifyKey(pk_hex, encoder=nacl.encoding.HexEncoder)
    try:
        pk.verify(content.encode("utf-8"), nacl.encoding.HexEncoder.decode(signature))
        return True
    except Exception:
        return False