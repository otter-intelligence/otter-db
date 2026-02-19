"""
Generate AGENTS.md and CLAUDE.md from the source .cursor rules files.
This extracts the Python and general rule files and writes them out.
"""
from pathlib import Path


def main():
    base = Path('.').resolve()
    gen = base / '.cursor' / 'rules' / 'general.mdc'
    py = base / '.cursor' / 'rules' / 'python.mdc'
    content = ''
    if gen.exists():
        content += gen.read_text(encoding='utf-8')
    if py.exists():
        content += py.read_text(encoding='utf-8')

    for out in ('CLAUDE.md', 'AGENTS.md'):
        Path(out).write_text(content, encoding='utf-8')
        print(f'Wrote {out}')


if __name__ == '__main__':
    main()
