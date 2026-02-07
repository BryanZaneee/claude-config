# Technology Insights

Framework-specific knowledge and platform-specific patterns.

## Python Module Invocation

Standard invocation pattern:
```bash
python3 -m package.module.submodule --step N
```

Working directory matters. Skills in `~/.claude/skills/scripts/` invoked as:
```bash
cd ~/.claude/skills/scripts && python3 -m skills.skill_name.module --step N
```

PYTHONPATH-based imports (no pyproject.toml in this architecture). Package structure requires `__init__.py` files.

## Git Commit Attribution

Co-authorship format for LLM-assisted commits:
```
Commit message summary.

Detailed description.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

Use HEREDOC to preserve formatting:
```bash
git commit -m "$(cat <<'EOF'
Message here.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

## Nginx SSL Configuration

Let's Encrypt via certbot requires:
1. Domain DNS pointing to server IP (A/AAAA records)
2. HTTP (port 80) accessible for ACME challenge
3. Nginx serving site with server_name matching domain

Auto-renewal via systemd timer (certbot.timer). Certificates stored in `/etc/letsencrypt/live/domain.com/`.

Common failure: DNS not pointing to correct IP. Verify with `host domain.com` matches `curl -s ifconfig.me`.

## SSH Key Management

Ed25519 preferred over RSA (smaller keys, faster, equivalent security):
```bash
ssh-keygen -t ed25519 -C "descriptive-comment" -f ~/.ssh/id_ed25519
```

Public key format: `ssh-ed25519 <base64-key> <comment>`

Add to GitHub: Settings → SSH and GPG keys → New SSH key.

## Pydantic Schema Validation

Use for data validation before file writes:
```python
class Schema(BaseModel):
    field: str
    optional_field: Optional[int] = None

data = Schema(**user_input)  # Raises ValidationError if invalid
write_file(data.model_dump())
```

Separates validation from business logic. Enables type-safe data handling.
