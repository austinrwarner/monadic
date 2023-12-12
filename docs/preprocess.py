from typing import Dict, Optional, List
import pathlib

import json
import sys


def load_file(path: str) -> str:
    with open(path, "r") as f:
        readme = f.read()
    return readme


def parse_md(md: List[str], level: int = 1) -> Dict[Optional[str], List[str]]:
    heading_marker = "#" * level + " "

    contents: Dict[Optional[str], List[str]] = {}

    current_heading = None
    current_content = contents.setdefault(current_heading, [])

    for line in md:
        if line.startswith(heading_marker):
            current_heading = line.replace(heading_marker, "").strip()
            current_content = contents.setdefault(current_heading, [])
        else:
            if line.startswith("#" * (level + 1)):
                line = line[level - 1:]

            current_content.append(line)

    return contents


def main(
        readme_path: str,
        index_path: str,
        output_dir: str,
        level: int
):
    readme = load_file(readme_path)
    index = load_file(index_path)
    readme_contents = parse_md(readme.splitlines(), level)

    for section, content in readme_contents.items():
        if section is None:
            continue
        elif f"<{section.lower()}>" in index:
            print(f"Found {section.lower()} in index")
            with open(pathlib.Path(output_dir).joinpath(f"{section.lower()}.md"), "w") as f:
                f.write(f'# {section}\n\n')
                f.write("\n".join(content))
        else:
            print(f"Did not find {section.lower()} in index")


if __name__ == "__main__":
    _readme_path = str(pathlib.Path(__file__).parent.parent.joinpath("README.md"))
    _docs_path = str(pathlib.Path(__file__).parent.parent.joinpath("docs", "source"))
    _index_path = str(pathlib.Path(_docs_path).joinpath("index.rst"))
    _level = 2
    main(_readme_path, _index_path, _docs_path, _level)
