"""Build, commit and push the website. Run with --check for build-only validation."""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, encoding='utf-8',
                            errors='replace', stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    if result.stdout:
        print(result.stdout, end='', flush=True)
    if result.returncode:
        raise RuntimeError(f'Command failed ({result.returncode}): {args[0]}')
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description='Build and publish the iris website')
    parser.add_argument('--check', action='store_true', help='Build and validate without committing or pushing')
    parser.add_argument('-m', '--message', help='Git commit message')
    args = parser.parse_args()
    try:
        branch = run('git', 'branch', '--show-current')
        if branch != 'main':
            raise RuntimeError('Please switch to main before publishing.')
        remote = run('git', 'remote', 'get-url', 'origin')
        if remote.removesuffix('.git').rstrip('/') not in (
            'https://github.com/cppywh/cppywh.github.io',
            'git@github.com:cppywh/cppywh.github.io',
        ):
            raise RuntimeError('Unexpected origin repository; publishing stopped.')
        python = ROOT / '.venv/Scripts/python.exe'
        run(str(python) if python.exists() else sys.executable,
            str(ROOT / 'tools/build_site.py'))
        run('git', 'diff', '--check')
        if args.check:
            print('Build verified. No commit or push performed.')
            return 0
        # This command publishes all website changes, including new PDFs.
        print('Publishing all website changes:')
        run('git', 'status', '--short')
        run('git', 'add', '--all')
        staged = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=ROOT)
        if staged.returncode == 1:
            run('git', 'commit', '-m', args.message or
                f'Update iris website {datetime.now():%Y-%m-%d %H:%M}')
        elif staged.returncode != 0:
            raise RuntimeError('Failed to inspect staged changes.')
        run('git', 'push', 'origin', 'main')
        print('Pushed successfully. GitHub Pages will deploy shortly: https://cppywh.github.io/')
        return 0
    except (RuntimeError, OSError) as error:
        print(f'Publishing stopped: {error}', file=sys.stderr)
        print('Changes are preserved. Fix the error and run this script again.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
