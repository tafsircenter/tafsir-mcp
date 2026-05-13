"""رفع Dataset Card إلى Hugging Face."""
import os
import sys

from huggingface_hub import HfApi, login

REPO_ID = "tafsircenter/tafsir-mcp-data"

DATASET_CARD = """---
license: cc-by-4.0
language:
- ar
- en
- bn
tags:
- quran
- tafsir
- islamic
- arabic-nlp
- mcp
- model-context-protocol
size_categories:
- 1K<n<10K
pretty_name: Tafsir MCP — Quranic Database
---

# Tafsir MCP — Quranic Database

<div align="center">

**قاعدة بيانات القرآن الكريم والتفاسير لمشروع [tafsir-mcp](https://github.com/tafsircenter/tafsir-mcp)**

برعاية [مركز تفسير للدراسات القرآنية](https://tafsir.net)

</div>

---

## 📖 Overview

This dataset is the data backbone for [`tafsir-mcp`](https://github.com/tafsircenter/tafsir-mcp),
a Model Context Protocol (MCP) server providing scholarly, offline-first access to the Holy Quran
for AI assistants like Claude Code, Cursor, and any MCP-compatible client.

All content is sourced from and reviewed by **Markaz Tafsir for Quranic Studies**
([tafsir.net](https://tafsir.net)).

---

## 📊 Content

| Category | Count |
|---|---|
| Surahs (chapters) | **114** |
| Ayahs (verses) | **6,236** |
| Words (Othmani script) | **77,432** |
| Distinct Arabic roots | **1,891** |
| Classical tafsirs (full coverage) | **5** |
| Mukhtasar tafsir languages | **3** (AR, EN, BN) |
| Ayahs with asbab al-nuzool | **201** |
| Mushaf pages (with extracted fawaed) | **604** |
| File size | **~214 MB** |

### Classical Tafsirs Included

| Tafsir | Author | Death Year (AH) |
|---|---|---|
| Jami' al-Bayan (الطبري) | Abu Ja'far al-Tabari | 310 |
| Tafsir al-Quran al-Azim (ابن كثير) | Ibn Kathir | 774 |
| Ma'alim al-Tanzil (البغوي) | al-Baghawi | 510 |
| Taysir al-Karim al-Rahman (السعدي) | al-Sa'di | 1376 |
| al-Tafsir al-Muyassar | King Fahd Complex | Contemporary |
| al-Mukhtasar fi al-Tafsir | Markaz Tafsir | Contemporary |

---

## 📂 File Format

Single SQLite 3.x database (`quran.db`).

---

## 🚀 Usage

### Via tafsir-mcp (recommended)

```bash
pip install tafsir-mcp
# Database auto-downloads from this dataset on first run
```

### Direct SQLite access

```python
from huggingface_hub import hf_hub_download
import sqlite3

db_path = hf_hub_download(
    repo_id="tafsircenter/tafsir-mcp-data",
    filename="quran.db",
    repo_type="dataset",
)
conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
```

---

## 📜 License — CC BY 4.0

- ✅ Share, adapt, use commercially
- 📌 Attribution required: "Markaz Tafsir for Quranic Studies (https://tafsir.net)"

Full license: [creativecommons.org/licenses/by/4.0](https://creativecommons.org/licenses/by/4.0/)

---

## 🏛️ Source

Sourced from official content systems of **Markaz Tafsir for Quranic Studies**,
used in production and reviewed by the Center's scholars.

---

## 📧 Contact

- 🌐 [tafsir.net](https://tafsir.net)
- 📧 cloud@tafsir.net
- 🐙 [github.com/tafsircenter/tafsir-mcp](https://github.com/tafsircenter/tafsir-mcp)
"""


def main() -> int:
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("❌ ضع التوكن: export HF_TOKEN=hf_xxx", file=sys.stderr)
        return 1

    login(token=token, add_to_git_credential=False)
    api = HfApi()
    api.upload_file(
        path_or_fileobj=DATASET_CARD.encode("utf-8"),
        path_in_repo="README.md",
        repo_id=REPO_ID,
        repo_type="dataset",
        commit_message="docs: comprehensive bilingual dataset card",
    )
    print(f"✅ Dataset card رُفع: https://huggingface.co/datasets/{REPO_ID}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
