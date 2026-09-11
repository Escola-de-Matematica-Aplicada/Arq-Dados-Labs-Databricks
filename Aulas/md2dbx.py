#!/usr/bin/env python3
"""Converte um LAB .md em notebook no formato Databricks (estilo ex-formato-databrick-notebook.ipynb).

Regras:
- Conteudo markdown vira celulas "markdown", quebradas em titulos H2/H3 (H1 fica com o bloco inicial).
- Blocos de codigo cercados por ``` viram celulas "code" (linguagem no metadata, fence removido).
- Metadados Databricks (nuid uuid4, cellMetadata/inputWidgets/showTitle/tableResultSettingsMap/title)
  identicos ao notebook-exemplo; notebookName = nome do arquivo.
"""
import json
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


def convert(md_path, ipynb_path):
    md_text = Path(md_path).read_text(encoding="utf-8")
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
