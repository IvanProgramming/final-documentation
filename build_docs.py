#!/usr/bin/env python3
"""
build_docs.py – сборка документации из Markdown-файлов.

Требует установленного:
    • pandoc  (конвертация .md → .tex)
    • latexmk (автоматическая сборка PDF)

Использование:
    python build_docs.py build     # конвертация + сборка PDF
    python build_docs.py clean     # удалить build/ и служебные файлы
"""

import argparse
import subprocess
import shutil
from pathlib import Path
import sys
import os

SRC_DIR   = Path("src")
BUILD_DIR = Path("build")
MAIN_TEX  = Path("main.tex")
OUTPUT_PDF = MAIN_TEX.with_suffix(".pdf")

def convert_md_to_tex() -> None:
    """Пробегаемся по SRC/*.md и получаем build/*.tex."""
    if not SRC_DIR.is_dir():
        sys.exit(f"Каталог {SRC_DIR} не найден.")

    BUILD_DIR.mkdir(exist_ok=True)
    for md in sorted(SRC_DIR.glob("*.md")):
        tex_out = BUILD_DIR / md.with_suffix(".tex").name
        print(f"→ {md}  →  {tex_out}")
        subprocess.run(
            [
                "pandoc",
                "-f", "markdown",
                "--lua-filter=image.lua",
                "-t", "latex",      # без -s ⇒ без \documentclass и \begin{document}
                str(md),
                "-o", str(tex_out),
            ],
            check=True,
        )

def compile_pdf() -> None:
    """Собираем main.tex → PDF (latexmk сам вызовет xelatex/pdflatex)."""
    os.chdir(BUILD_DIR)  # переходим в build/ для сборки PDF
    print("cd ", BUILD_DIR.resolve())
    if not MAIN_TEX.is_file():
        sys.exit(f"Файл {MAIN_TEX} не найден.")
    print(f"⧗ Компиляция {MAIN_TEX} …")
    try:
        subprocess.run(
            ["pdflatex", "-pdf", "-interaction=nonstopmode", "-synctex=1", "-shell-escape", str(MAIN_TEX)], 
            check=True,
        )
    except subprocess.CalledProcessError:
        print("Ошибка, проверяю наличие PDF")
        if not OUTPUT_PDF.is_file():
            print("PDF не найден, проверьте ошибки в LaTeX-файлах.")
            sys.exit(1)
    os.chdir("..")  # возвращаемся в исходный каталог
    print(f"✓ Готово: {OUTPUT_PDF.resolve()}")

def clean() -> None:
    """Удаляем build/ и временные LaTeX-файлы."""
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        print(f"Удалён каталог {BUILD_DIR}/")
    aux_ext = [".aux", ".log", ".out", ".toc", ".fls", ".fdb_latexmk"]
    for ext in aux_ext + [".pdf"]:
        for f in Path(".").glob(f"*{ext}"):
            if f.is_file():
                f.unlink()
                print(f"Удалён {f}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Сборка документации проекта.")
    parser.add_argument("command", choices=["build", "clean"],
                        help="build – собрать PDF; clean – убрать временные файлы.")
    args = parser.parse_args()

    if args.command == "build":
        convert_md_to_tex()
        compile_pdf()
    elif args.command == "clean":
        clean()

if __name__ == "__main__":
    main()
