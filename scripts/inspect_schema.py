"""Read-only schema inspection for data/quran.db — run before building tools."""

import os
import sqlite3
import sys

DB_PATH = os.environ.get("QURAN_DB_PATH", "data/quran.db")
SEP = "─" * 70

TABLES = [
    "surah_content", "surah_stats",
    "ayah_content_irab", "ayah_content_tajweed", "ayah_content_nozool",
    "tafsir_tabary", "tafsir_katheer", "tafsir_baghawy",
    "tafsir_saadi", "tafsir_moyassar", "QuranTafseer",
    "word_content_rasm", "word_content_meaning",
    "word_content_irab", "word_content_sarf",
    "word_statistics", "qeraat_info", "mokhtasar_fawaed",
]


def fmt_row(row: sqlite3.Row, max_val: int = 120) -> str:
    parts = []
    for k in row.keys():
        v = row[k]
        s = str(v).replace("\n", "↵").replace("\r", "") if v is not None else "NULL"
        parts.append(f"  {k}: {s[:max_val]}{'…' if len(s) > max_val else ''}")
    return "\n".join(parts)


def section(title: str) -> None:
    print(f"\n{'═'*70}")
    print(f"  {title}")
    print('═' * 70)


# ── connect ──────────────────────────────────────────────────────────────────
conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA query_only = ON")

# ══════════════════════════════════════════════════════════════════════════════
# القسم 1: Schema كل الجداول
# ══════════════════════════════════════════════════════════════════════════════
section("القسم 1 — Schema الجداول")

for table in TABLES:
    print(f"\n┌── {table}")
    cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
    for c in cols:
        pk   = " [PK]" if c["pk"] else ""
        null = " NOT NULL" if c["notnull"] else " nullable"
        dflt = f" default={c['dflt_value']}" if c["dflt_value"] is not None else ""
        print(f"│  col[{c['cid']:02d}] {c['name']:<35} {c['type']:<12}{pk}{null}{dflt}")
    print("└" + SEP[1:])

# ══════════════════════════════════════════════════════════════════════════════
# القسم 2: عينات بيانات
# ══════════════════════════════════════════════════════════════════════════════
section("القسم 2 — عينات بيانات")

queries = [
    # A
    ("A1 surah_content WHERE surahNo=1",
     "SELECT * FROM surah_content WHERE surahNo = 1"),
    ("A2 surah_stats WHERE surahNo=1",
     "SELECT * FROM surah_stats WHERE surahNo = 1"),
    # B
    ("B1 tafsir_saadi 2:255",
     "SELECT * FROM tafsir_saadi WHERE sura = 2 AND aya = 255"),
    ("B2 tafsir_moyassar 2:255",
     "SELECT * FROM tafsir_moyassar WHERE sura = 2 AND aya = 255"),
    ("B3 QuranTafseer 2:255",
     "SELECT * FROM QuranTafseer WHERE surahNo = 2 AND ayahNo = 255"),
    # C
    ("C1 ayah_content_irab 1:1",
     "SELECT * FROM ayah_content_irab WHERE surahNo = 1 AND ayahNo = 1"),
    ("C2 ayah_content_tajweed 1:1",
     "SELECT * FROM ayah_content_tajweed WHERE surahNo = 1 AND ayahNo = 1"),
    # D
    ("D ayah_content_nozool LIMIT 3",
     "SELECT * FROM ayah_content_nozool LIMIT 3"),
    # E
    ("E1 word_content_rasm 1:1",
     "SELECT * FROM word_content_rasm WHERE surahNo=1 AND ayahNo=1 ORDER BY wordNo"),
    ("E2 word_content_meaning 1:1",
     "SELECT * FROM word_content_meaning WHERE surahNo=1 AND ayahNo=1 ORDER BY wordNo"),
    ("E3 word_content_irab 1:1",
     "SELECT * FROM word_content_irab WHERE surahNo=1 AND ayahNo=1 ORDER BY wordNo"),
    ("E4 word_content_sarf 1:1",
     "SELECT * FROM word_content_sarf WHERE surahNo=1 AND ayahNo=1 ORDER BY wordNo"),
    ("E5 word_statistics 1:1",
     "SELECT * FROM word_statistics WHERE surahNo=1 AND ayahNo=1 ORDER BY wordNo"),
    # F
    ("F qeraat_info 1:4",
     "SELECT * FROM qeraat_info WHERE surahNo=1 AND ayahNo=4"),
    # G
    ("G mokhtasar_fawaed page=1",
     "SELECT * FROM mokhtasar_fawaed WHERE page=1 LIMIT 3"),
]

for label, sql in queries:
    print(f"\n── {label}")
    rows = conn.execute(sql).fetchall()
    if not rows:
        print("  (no rows)")
    for i, row in enumerate(rows):
        print(f"  [row {i}]\n{fmt_row(row)}")

# ══════════════════════════════════════════════════════════════════════════════
# القسم 3: تحقق من أعمدة حساسة
# ══════════════════════════════════════════════════════════════════════════════
section("القسم 3 — أعمدة حساسة")

checks = {
    "ayah_content_irab":    [r[1] for r in conn.execute("PRAGMA table_info(ayah_content_irab)").fetchall()],
    "ayah_content_tajweed": [r[1] for r in conn.execute("PRAGMA table_info(ayah_content_tajweed)").fetchall()],
    "ayah_content_nozool":  [r[1] for r in conn.execute("PRAGMA table_info(ayah_content_nozool)").fetchall()],
    "word_statistics":      [r[1] for r in conn.execute("PRAGMA table_info(word_statistics)").fetchall()],
    "qeraat_info":          [r[1] for r in conn.execute("PRAGMA table_info(qeraat_info)").fetchall()],
    "surah_content":        [r[1] for r in conn.execute("PRAGMA table_info(surah_content)").fetchall()],
    "surah_stats":          [r[1] for r in conn.execute("PRAGMA table_info(surah_stats)").fetchall()],
}

print("\n1. ayah_content_irab columns:", checks["ayah_content_irab"])
print("2. ayah_content_tajweed columns:", checks["ayah_content_tajweed"])
print("3. ayah_content_nozool columns:", checks["ayah_content_nozool"])
print("4. word_statistics columns:", checks["word_statistics"])
print("5. qeraat_info columns:", checks["qeraat_info"])
print("6. surah_content columns:", checks["surah_content"])
print("7. surah_stats columns:", checks["surah_stats"])

# ══════════════════════════════════════════════════════════════════════════════
# القسم 4: حالات حافة
# ══════════════════════════════════════════════════════════════════════════════
section("القسم 4 — حالات حافة (edge cases)")

edge = [
    ("نزول في الفاتحة",
     "SELECT COUNT(*) FROM ayah_content_nozool WHERE surahNo = 1"),
    ("NULL في tafsir_saadi",
     "SELECT COUNT(*) FROM tafsir_saadi WHERE tafsir IS NULL OR tafsir = ''"),
    ("كلمات 2:255 (رسم)",
     "SELECT wordNo, word FROM word_content_rasm WHERE surahNo=2 AND ayahNo=255 ORDER BY wordNo"),
    ("كلمات 3:1 (رسم)",
     "SELECT wordNo, word FROM word_content_rasm WHERE surahNo=3 AND ayahNo=1 ORDER BY wordNo"),
    ("كلمات 36:1 (رسم)",
     "SELECT wordNo, word FROM word_content_rasm WHERE surahNo=36 AND ayahNo=1 ORDER BY wordNo"),
    ("QuranTafseer — آيات فريدة",
     "SELECT COUNT(DISTINCT surahNo||':'||ayahNo) FROM QuranTafseer"),
    ("QuranTafseer — Mukhtasaren NULL",
     "SELECT COUNT(*) FROM QuranTafseer WHERE Mukhtasaren IS NULL OR Mukhtasaren = ''"),
    ("QuranTafseer — Mukhtasarbn NULL",
     "SELECT COUNT(*) FROM QuranTafseer WHERE Mukhtasarbn IS NULL OR Mukhtasarbn = ''"),
]

for label, sql in edge:
    rows = conn.execute(sql).fetchall()
    if len(rows) == 1 and len(rows[0]) == 1:
        print(f"  {label}: {rows[0][0]}")
    else:
        print(f"  {label}:")
        for r in rows:
            print(f"    {tuple(r)}")

conn.close()
print(f"\n{'═'*70}")
print("  فحص مكتمل — لم تُجرَ أي تعديلات على قاعدة البيانات")
print('═' * 70)
