# File Utilities

A lightweight Home Assistant integration that provides **safe, generic file
read/write services** for use by other integrations, automations, and scripts.

This integration is intentionally **low-level** and **domain-agnostic**. It does
not interpret file contents and does not make assumptions about file purpose or
format.

---

## Features

- Read text files
- Write text files
- Atomic writes by default
- Path hardening and traversal protection
- Async-safe via internal locking
- Relative paths default to `/config`

---

## Design Principles

- **Generic**: No SmartQasa or application-specific logic
- **Safe by default**: Restricted filesystem access and atomic writes
- **Minimal API surface**: Two services only (`read`, `write`)
- **Composable**: Intended to be used _by_ other integrations

---

## Security Model

- All file access is restricted to allowed roots (default: `/config`)
- Path traversal (`..`) and symlink escapes are blocked
- Relative paths are resolved under `/config`
- Canonical path resolution is enforced before access

This matches Home Assistant core filesystem safety expectations.

---

## Services

### `file_utilities.read`

Reads the contents of a text file.

#### Fields

| Field      | Required | Description                                        |
| ---------- | -------- | -------------------------------------------------- |
| `path`     | yes      | File path (relative paths resolve under `/config`) |
| `encoding` | no       | Text encoding (default: `utf-8`)                   |

#### Example

```yaml
action: file_utilities.read
data:
  path: 'example.txt'
```

#### Response

```yaml
content: 'file contents here'
```

---

### `file_utilities.write`

Writes text content to a file.

Writes are **atomic by default**, meaning the file is written to a temporary
file and then replaced.

#### Fields

| Field      | Required | Description                                        |
| ---------- | -------- | -------------------------------------------------- |
| `path`     | yes      | File path (relative paths resolve under `/config`) |
| `content`  | yes      | Text content to write                              |
| `encoding` | no       | Text encoding (default: `utf-8`)                   |
| `create`   | no       | Create file if missing (default: `true`)           |
| `atomic`   | no       | Perform atomic write (default: `true`)             |

#### Example

```yaml
action: file_utilities.write
data:
  path: 'example.txt'
  content: 'Hello world'
```

---

## What This Integration Does _Not_ Do

- ❌ Parse YAML or JSON
- ❌ Understand file semantics
- ❌ Manage configuration files
- ❌ Expose entities or state
- ❌ Handle binary data (text only, for now)

Those responsibilities belong to higher-level integrations.

---

## Typical Use Cases

- Helper integrations that need safe file persistence
- Storing small JSON/YAML blobs
- Writing generated configuration fragments
- Controlled file access from automations

---

## Installation

Copy this integration into:

```
custom_components/file_utilities/
```

Restart Home Assistant.

No configuration is required.

---

## Development Notes

- Python async I/O with locking
- Designed for future extension (binary support, per-path locks)
- Stable public API

---
