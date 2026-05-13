"""Build FTS5 search index and performance indexes in data/quran.db.

Run once (read-write). Safe to re-run — drops and recreates ayah_fts.
Usage: uv run python scripts/build_fts.py
"""

import os
import sqlite3
import sys
import time

sys.path.insert(0, "src")
from tafsir.normalize import normalize_arabic  # noqa: E402

DB_PATH = os.environ.get("QURAN_DB_PATH", "data/quran.db")
BATCH_SIZE = 500

# ── connect read-write ────────────────────────────────────────────────────────
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

# ══════════════════════════════════════════════════════════════════════════════
# 1. Performance indexes
# ══════════════════════════════════════════════════════════════════════════════
print("Creating indexes…")
indexes = [
    "CREATE INDEX IF NOT EXISTS idx_rasm_sa      ON word_content_rasm(surahNo, ayahNo)",
    "CREATE INDEX IF NOT EXISTS idx_meaning_sa   ON word_content_meaning(surahNo, ayahNo)",
    "CREATE INDEX IF NOT EXISTS idx_wirab_sa     ON word_content_irab(surahNo, ayahNo)",
    "CREATE INDEX IF NOT EXISTS idx_sarf_sa      ON word_content_sarf(surahNo, ayahNo)",
    "CREATE INDEX IF NOT EXISTS idx_stats_sa     ON word_statistics(surahNo, ayahNo)",
    "CREATE INDEX IF NOT EXISTS idx_stats_root   ON word_statistics(root)",
    "CREATE INDEX IF NOT EXISTS idx_qeraat_sa    ON qeraat_info(surahNo, ayahNo)",
    "CREATE INDEX IF NOT EXISTS idx_tabary_sa    ON tafsir_tabary(sura, aya)",
    "CREATE INDEX IF NOT EXISTS idx_katheer_sa   ON tafsir_katheer(sura, aya)",
    "CREATE INDEX IF NOT EXISTS idx_baghawy_sa   ON tafsir_baghawy(sura, aya)",
    "CREATE INDEX IF NOT EXISTS idx_saadi_sa     ON tafsir_saadi(sura, aya)",
    "CREATE INDEX IF NOT EXISTS idx_moyassar_sa  ON tafsir_moyassar(sura, aya)",
    "CREATE INDEX IF NOT EXISTS idx_qurantafs_sa ON QuranTafseer(surahNo, ayahNo)",
    "CREATE INDEX IF NOT EXISTS idx_nozool_sa    ON ayah_content_nozool(surahNo, ayahNo)",
    "CREATE INDEX IF NOT EXISTS idx_tajweed_sa   ON ayah_content_tajweed(surahNo, ayahNo)",
    "CREATE INDEX IF NOT EXISTS idx_airab_sa     ON ayah_content_irab(surahNo, ayahNo)",
    "CREATE INDEX IF NOT EXISTS idx_fawaed_page  ON mokhtasar_fawaed(page)",
]

t0 = time.perf_counter()
for sql in indexes:
    conn.execute(sql)
conn.commit()
print(f"  ✓ {len(indexes)} indexes created/verified in {time.perf_counter()-t0:.2f}s")

# ══════════════════════════════════════════════════════════════════════════════
# 2. Build FTS5 virtual table
# ══════════════════════════════════════════════════════════════════════════════
print("\nBuilding FTS5 table ayah_fts…")
t1 = time.perf_counter()

conn.execute("DROP TABLE IF EXISTS ayah_fts")
conn.execute("""
    CREATE VIRTUAL TABLE ayah_fts USING fts5(
        surahNo    UNINDEXED,
        ayahNo     UNINDEXED,
        text_normalized,
        text_original,
        tokenize='unicode61 remove_diacritics 2'
    )
""")

# Build ayah texts from word_content_rasm
print("  Loading ayah words…")
rows = conn.execute(
    "SELECT surahNo, ayahNo, word FROM word_content_rasm"
    " ORDER BY surahNo, ayahNo, wordNo"
).fetchall()

# Group into {(surahNo, ayahNo): [word, ...]}
ayahs: dict[tuple[int, int], list[str]] = {}
for row in rows:
    key = (row["surahNo"], row["ayahNo"])
    ayahs.setdefault(key, []).append(row["word"])

print(f"  Grouped {len(ayahs)} ayahs, inserting in batches of {BATCH_SIZE}…")

batch: list[tuple] = []
inserted = 0
for (surah_no, ayah_no), words in ayahs.items():
    text_original = " ".join(words)
    text_normalized = normalize_arabic(text_original)
    batch.append((surah_no, ayah_no, text_normalized, text_original))
    if len(batch) >= BATCH_SIZE:
        conn.executemany(
            "INSERT INTO ayah_fts(surahNo, ayahNo, text_normalized, text_original)"
            " VALUES (?,?,?,?)",
            batch,
        )
        inserted += len(batch)
        batch = []
        print(f"    {inserted} / {len(ayahs)}", end="\r")

if batch:
    conn.executemany(
        "INSERT INTO ayah_fts(surahNo, ayahNo, text_normalized, text_original)"
        " VALUES (?,?,?,?)",
        batch,
    )
    inserted += len(batch)

conn.commit()
elapsed = time.perf_counter() - t1

# ══════════════════════════════════════════════════════════════════════════════
# 3. Verify
# ══════════════════════════════════════════════════════════════════════════════
count = conn.execute("SELECT COUNT(*) FROM ayah_fts").fetchone()[0]
db_size_mb = os.path.getsize(DB_PATH) / 1_048_576

conn.execute("PRAGMA optimize")
conn.close()

print(f"\n  ✓ Inserted {count} ayahs in {elapsed:.2f}s")
print(f"  ✓ DB size after FTS: {db_size_mb:.1f} MB")

if count != 6236:
    print(f"  ✗ Expected 6236, got {count}", file=sys.stderr)
    sys.exit(1)

print("\n✓ build_fts.py complete — ayah_fts ready for search.")
