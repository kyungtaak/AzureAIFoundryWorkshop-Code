"""검증 하네스 — 노트북·문서·SDK 임포트를 한 번에 점검한다.

사용법:
    pip install -r requirements.txt nbformat pyyaml
    python .github/scripts/verify.py

Windows/macOS/Linux 동일하게 동작하며, 실패가 하나라도 있으면 exit code 1을 반환한다.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EXCLUDE_DIRS = {".venv", "venv", ".git", "node_modules", "__pycache__", ".ipynb_checkpoints"}

OK = "[OK]"
FAIL = "[FAIL]"


def _iter_files(pattern: str):
    for path in sorted(REPO_ROOT.glob(pattern)):
        if EXCLUDE_DIRS.isdisjoint(path.parts):
            yield path


def _rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def check_notebooks() -> list[str]:
    """노트북 스키마 유효성, 코드 셀 문법, 출력 클리어 여부를 확인한다."""
    import nbformat

    errors: list[str] = []
    found = False
    for path in _iter_files("**/*.ipynb"):
        found = True
        rel = _rel(path)
        try:
            nb = nbformat.read(path, as_version=4)
            nbformat.validate(nb)
        except Exception as exc:
            errors.append(f"{rel}: 노트북 유효성 오류 — {exc}")
            continue

        cell_errors: list[str] = []
        for index, cell in enumerate(nb.cells, start=1):
            if cell.cell_type != "code":
                continue
            if cell.get("outputs"):
                cell_errors.append(f"{rel}: 셀 {index} 출력이 클리어되지 않음")
            try:
                ast.parse(cell.source)
            except SyntaxError as exc:
                cell_errors.append(f"{rel}: 셀 {index} 문법 오류 — {exc}")

        errors.extend(cell_errors)
        if not cell_errors:
            print(f"  {OK} {rel}")

    if not found:
        errors.append("검사할 .ipynb 파일을 찾지 못함")
    return errors


def check_docs() -> list[str]:
    """frontmatter YAML 파싱과 상대 링크 대상 존재 여부를 확인한다."""
    import yaml

    link_pattern = re.compile(r"\]\((?!https?:|mailto:|#)([^)]+)\)")
    errors: list[str] = []
    for path in _iter_files("**/*.md"):
        rel = _rel(path)
        text = path.read_text(encoding="utf-8")

        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) < 3:
                errors.append(f"{rel}: frontmatter 종료 구분자(---) 없음")
            else:
                try:
                    yaml.safe_load(parts[1])
                except yaml.YAMLError as exc:
                    errors.append(f"{rel}: frontmatter YAML 오류 — {exc}")

        for match in link_pattern.finditer(text):
            target = match.group(1).split("#")[0].strip()
            if not target:
                continue
            if not (path.parent / target).resolve().exists():
                errors.append(f"{rel}: 깨진 링크 → {match.group(1)}")

        print(f"  {OK} {rel}")
    return errors


def check_imports() -> list[str]:
    """실습 노트북이 의존하는 SDK 표면을 임포트만으로 확인한다 (API 호출 없음)."""
    errors: list[str] = []
    try:
        import azure.ai.projects  # noqa: F401
        import azure.identity  # noqa: F401
        import azure.search.documents  # noqa: F401
        import openai
        from azure.ai.projects.models import PromptAgentDefinition  # noqa: F401
    except ImportError as exc:
        return [f"SDK 임포트 실패 — {exc}"]

    from openai import OpenAI

    for attr in ("chat", "embeddings", "responses", "conversations"):
        if not hasattr(OpenAI, attr):
            errors.append(f"openai {openai.__version__}: 클라이언트에 '{attr}' 속성 없음")

    if not errors:
        print(f"  {OK} SDK 임포트 및 openai {openai.__version__} API 표면 확인")
    return errors


CHECKS = {
    "notebooks": ("노트북 유효성 + 코드 문법 + 출력 클리어", check_notebooks),
    "docs": ("frontmatter 파싱 + 상대 링크 생존", check_docs),
    "imports": ("SDK 임포트 스모크 테스트", check_imports),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="워크샵 리포지토리 검증 하네스")
    parser.add_argument(
        "--only",
        choices=sorted(CHECKS),
        action="append",
        help="지정한 검사만 실행 (반복 지정 가능, 기본값: 전체)",
    )
    args = parser.parse_args()
    selected = args.only or list(CHECKS)

    all_errors: list[str] = []
    for index, name in enumerate(selected, start=1):
        label, func = CHECKS[name]
        print(f"\n[{index}/{len(selected)}] {label}")
        all_errors.extend(func())

    print()
    if all_errors:
        for error in all_errors:
            print(f"{FAIL} {error}")
        print(f"\n{FAIL} 실패 {len(all_errors)}건")
        return 1

    print(f"{OK} 전체 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
