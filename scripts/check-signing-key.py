#!/usr/bin/env python3

import argparse
import base64
import pathlib
import subprocess
import tempfile


def extract_public_key_b64(private_key_pem_b64: str) -> str:
    private_key_bytes = base64.b64decode(private_key_pem_b64.strip())
    with tempfile.TemporaryDirectory() as tmpdir:
        private_key_path = pathlib.Path(tmpdir) / "signing.pem"
        public_key_der_path = pathlib.Path(tmpdir) / "public.der"
        private_key_path.write_bytes(private_key_bytes)
        subprocess.run(
            [
                "openssl",
                "pkey",
                "-in",
                str(private_key_path),
                "-pubout",
                "-outform",
                "DER",
                "-out",
                str(public_key_der_path),
            ],
            check=True,
            capture_output=True,
        )
        public_key_der = public_key_der_path.read_bytes()
        return base64.b64encode(public_key_der[-32:]).decode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-key-b64", required=True)
    parser.add_argument("--public-key-b64", required=True)
    args = parser.parse_args()

    derived = extract_public_key_b64(args.private_key_b64)
    expected = args.public_key_b64.strip()
    if derived != expected:
        raise SystemExit("signing key mismatch: private key does not match supplied public key")

    print("signing key matches supplied public key")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
