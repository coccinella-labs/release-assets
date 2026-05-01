# release-assets

Reusable GitHub Actions workflow for building, packaging, signing, manifesting, smoke-testing, and publishing release assets for Rust CLIs.

## What it does

This workflow is intended to run after a separate release-orchestration step has already decided the version and tag.

It handles:
- cross-platform target matrix builds
- archive packaging
- SHA-256 checksums
- detached Ed25519 signatures
- release manifest generation
- optional smoke validation
- GitHub Release asset upload

It does not handle:
- version bumping
- release PR creation
- tag selection
- changelog generation

Those concerns belong in a separate release orchestration action such as `libnudget/release`.

## Reusable workflow

File:
- `.github/workflows/release-assets.yml`

### Inputs

- `release_tag`
- `release_target_sha`
- `binary_name`
- `package_path`
- `targets_json`
- `manifest_name`
- `cargo_build_args`
- `public_key_b64`

### Secrets

- `github_token`
- `signing_key_pem_b64`

## Target schema

`targets_json` is a JSON array. Example:

```json
[
  {
    "target_key": "linux-x86_64",
    "runner": "ubuntu-latest",
    "rust_target": "x86_64-unknown-linux-gnu",
    "binary_path": "target/x86_64-unknown-linux-gnu/release/harper",
    "archive_name": "harper-linux-x86_64.tar.gz",
    "archive_format": "tar.gz",
    "smoke": true,
    "setup_script": ""
  }
]
```

Optional target fields:
- `smoke_command`
- `setup_script`

## Signing model

The workflow signs packaged artifacts with the `signing_key_pem_b64` secret and verifies that the derived public key matches `public_key_b64` before publishing.

## Manifest contract

Each artifact entry includes:
- `url`
- `sha256`
- `signature`
