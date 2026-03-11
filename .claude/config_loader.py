import os
import json
import re

_ENV_PATTERN = re.compile(r"^\${([A-Z0-9_]+)}$")

def _resolve(obj):
    if isinstance(obj, str):
        m = _ENV_PATTERN.match(obj)
        if m:
            name = m.group(1)
            return os.environ.get(name)
        return obj
    if isinstance(obj, dict):
        return {k: _resolve(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_resolve(v) for v in obj]
    return obj

def load_config(path=None):
    # Resolution order:
    # 1. explicit path argument
    # 2. env var CLAUDE_CODE_ROUTER_CONFIG
    # 3. repo-local config.json (same dir as this file)
    # 4. user's home ~/.claude-code-router/config.json
    candidates = []
    if path:
        candidates.append(path)
    env_path = os.environ.get('CLAUDE_CODE_ROUTER_CONFIG')
    if env_path:
        candidates.append(env_path)
    repo_path = os.path.join(os.path.dirname(__file__), 'config.json')
    candidates.append(repo_path)
    home_path = os.path.join(os.path.expanduser('~'), '.claude-code-router', 'config.json')
    candidates.append(home_path)

    selected = None
    for p in candidates:
        try:
            if p and os.path.isfile(p):
                selected = p
                break
        except Exception:
            continue

    if not selected:
        raise FileNotFoundError('No config.json found. Searched: ' + ', '.join(candidates))

    with open(selected, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    cfg = _resolve(cfg)
    # warn on any unresolved placeholders
    def _find_placeholders(o, path=''):
        missing = []
        if isinstance(o, dict):
            for k, v in o.items():
                missing += _find_placeholders(v, f"{path}.{k}" if path else k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                missing += _find_placeholders(v, f"{path}[{i}]")
        elif isinstance(o, str) and _ENV_PATTERN.match(o):
            missing.append((path, o))
        return missing

    missing = _find_placeholders(cfg)
    if missing:
        for p, val in missing:
            print(f"Warning: config placeholder {val} at {p} was not replaced (env var missing)")
    return cfg

if __name__ == '__main__':
    try:
        cfg = load_config()
    except FileNotFoundError as e:
        print('Error loading config:', e)
        raise
    print('Loaded config from:', os.environ.get('CLAUDE_CODE_ROUTER_CONFIG') or os.path.join(os.path.dirname(__file__), 'config.json'))
    print('Providers:')
    for p in cfg.get('Providers', []):
        print('-', p.get('name'), 'api_key set?' , bool(p.get('api_key')))
