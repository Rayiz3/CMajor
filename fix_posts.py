import re
from pathlib import Path

posts = Path('_posts')
pattern = re.compile(
    r"\*\*\s*([^\(\*]+?)\s*\(\s*([A-Za-z][A-Za-z0-9]*(?:[\s\-][A-Za-z][A-Za-z0-9]*)*)\s*\)\s*\*\*"
)


def normalize_eng(eng: str) -> str:
    def fix(word: str) -> str:
        if word.isupper():
            return word
        return word[0].upper() + word[1:].lower() if word else word

    return " ".join(fix(word) for word in eng.split())


def replacement(match: re.Match) -> str:
    kor = match.group(1).strip()
    eng = normalize_eng(match.group(2))
    return f"**{kor}**<sup>{eng}</sup>"


def process_file(path: Path) -> int:
    text = path.read_text(encoding='utf-8')
    if not text:
        return 0

    updated_lines = []
    replacement_count = 0
    for line in text.splitlines(True):
        if line.lstrip().startswith('#'):
            updated_lines.append(line)
            continue

        new_line, count = pattern.subn(replacement, line)
        replacement_count += count
        updated_lines.append(new_line)

    if replacement_count:
        path.write_text(''.join(updated_lines), encoding='utf-8')

    return replacement_count


updated_total = 0
for path in sorted(posts.glob('*.md')):
    updated_total += process_file(path)

print('updated', updated_total, 'matches')
