#!/usr/bin/env python3
"""Converte um LAB .md em notebook no formato Databricks (estilo ex-formato-databrick-notebook.ipynb).

Regras:
- Conteudo markdown vira celulas "markdown", quebradas em titulos H2/H3 (H1 fica com o bloco inicial).
- Blocos de codigo cercados por ``` viram celulas "code" (linguagem no metadata, fence removido).
- Metadados Databricks (nuid uuid4, cellMetadata/inputWidgets/showTitle/tableResultSettingsMap/title)
  identicos ao notebook-exemplo; notebookName = nome do arquivo.
"""
import json
import posixpath
import re
import subprocess
import sys
import uuid
from pathlib import Path


def to_lines(text):
    """Fonte no formato Databricks/jupyter: lista de linhas com \\n no fim, exceto a ultima."""
    parts = text.split("\n")
    return [p + "\n" for p in parts[:-1]] + ([parts[-1]] if parts[-1] else [])


def cell_meta():
    return {
        "application/vnd.databricks.v1+cell": {
            "cellMetadata": {},
            "inputWidgets": {},
            "nuid": str(uuid.uuid4()),
            "showTitle": False,
            "tableResultSettingsMap": {},
            "title": "",
        }
    }


def split_cells(md_text):
    """Retorna lista (kind, lang, text): kind em {md, code}."""
    lines = md_text.split("\n")
    cells = []
    buf = []
    i = 0

    def flush():
        nonlocal buf
        if buf:
            txt = "\n".join(buf).strip("\n")
            if txt.strip():
                cells.append(("md", None, txt))
        buf = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("```"):
            lang = stripped[3:].strip() or "python"
            code = []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                code.append(lines[i])
                i += 1
            i += 1  # pula fence de fechamento
            # linhas de markdown apos o bloco comecam nova celula
            flush_prev = buf
            flush()
            cells.append(("code", lang, "\n".join(code)))
            continue
        # quebra em titulo H2/H3 (nao H1, para manter cabecalho junto)
        if (line.startswith("## ") or line.startswith("### ")) and buf and any(b.strip() for b in buf):
            flush()
        buf.append(line)
        i += 1
    flush()
    return cells


LINK_PAT = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')


def repo_base(md_path):
    """URL base 'https://.../blob/main' do repo git, ou None fora de repo."""
    try:
        root = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                              cwd=str(Path(md_path).parent), capture_output=True, text=True, check=True).stdout.strip()
        url = subprocess.run(["git", "config", "--get", "remote.origin.url"],
                             cwd=root, capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return None, None
    url = url.rstrip("/")
    url = re.sub(r"\.git$", "", url)
    m = re.match(r"git@github\.com:(.+)$", url)
    if m:
        url = "https://github.com/" + m.group(1)
    branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                            cwd=root, capture_output=True, text=True).stdout.strip() or "main"
    return f"{url}/blob/{branch}", root


def rewrite_links(md_text, base_url, repo_root, md_path):
    """Transforma links relativos em URLs GitHub absolutas (funcionam no Databricks)."""
    rel_dir = Path(md_path).resolve().parent.relative_to(repo_root).as_posix()

    def repl(m):
        text, url = m.group(1), m.group(2)
        if url.startswith(("http://", "https://", "mailto:", "#", "data:")):
            return m.group(0)
        clean = url.split("#", 1)[0]
        frag = url[len(clean):]
        if clean.startswith("/"):
            target = clean.lstrip("/")
        else:
            target = posixpath.normpath(posixpath.join(rel_dir, clean))
        target = target.rstrip("/")
        return f"[{text}]({base_url}/{target}{frag})"

    return LINK_PAT.sub(repl, md_text)


def convert(md_path, ipynb_path):
    md_text = Path(md_path).read_text(encoding="utf-8")
    base_url, repo_root = repo_base(md_path)
    if base_url:
        md_text = rewrite_links(md_text, base_url, repo_root, md_path)
    name = Path(ipynb_path).stem
    cells = []
    for kind, lang, text in split_cells(md_text):
        meta = cell_meta()
        if kind == "md":
            cells.append({"cell_type": "markdown", "metadata": meta, "source": to_lines(text)})
        else:
            if lang in ("sql", "sql-script"):
                src = "%sql\n\n" + text
            elif lang in ("python", "py"):
                src = text
            else:
                # linguagem desconhecida (bash, text...): mantem como markdown para nao quebrar execucao
                cells.append({"cell_type": "markdown", "metadata": meta, "source": to_lines("```" + lang + "\n" + text + "\n```")})
                continue
            meta["application/vnd.databricks.v1+cell"]["cellMetadata"] = {"language": lang}
            cells.append({"cell_type": "code", "execution_count": 0, "metadata": meta, "outputs": [], "source": to_lines(src)})
    nb = {
        "cells": cells,
        "metadata": {
            "application/vnd.databricks.v1+notebook": {
                "computePreferences": None,
                "dashboards": [],
                "environmentMetadata": {"base_environment": "", "environment_version": "5"},
                "inputWidgetPreferences": None,
                "language": "python",
                "notebookMetadata": {"pythonIndentUnit": 4},
                "notebookName": name,
                "widgets": {},
            },
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 0,
    }
    Path(ipynb_path).write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(cells)


if __name__ == "__main__":
    md, ipynb = sys.argv[1], sys.argv[2]
    n = convert(md, ipynb)
    print(f"{ipynb}: {n} celulas")
