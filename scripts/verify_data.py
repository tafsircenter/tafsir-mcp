"""Verify integrity of data/quran.db against expected row counts."""

import os
import sqlite3
import sys

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

DB_PATH = os.environ.get("QURAN_DB_PATH", "data/quran.db")

CHECKS = [
    ("surah_stats — عدد السور",           "SELECT COUNT(*) FROM surah_stats",                                                          114),
    ("word_content_rasm — آيات فريدة",    "SELECT COUNT(DISTINCT surahNo || '-' || ayahNo) FROM word_content_rasm",                    6236),
    ("word_content_rasm — كلمات كلي",     "SELECT COUNT(*) FROM word_content_rasm",                                                    77432),
    ("tafsir_tabary — صفوف",              "SELECT COUNT(*) FROM tafsir_tabary",                                                        6236),
    ("tafsir_katheer — صفوف",             "SELECT COUNT(*) FROM tafsir_katheer",                                                       6236),
    ("tafsir_baghawy — صفوف",             "SELECT COUNT(*) FROM tafsir_baghawy",                                                       6236),
    ("tafsir_saadi — صفوف",               "SELECT COUNT(*) FROM tafsir_saadi",                                                         6236),
    ("tafsir_moyassar — صفوف",            "SELECT COUNT(*) FROM tafsir_moyassar",                                                      6236),
    ("word_statistics — جذور مختلفة",     "SELECT COUNT(DISTINCT root) FROM word_statistics",                                          1891),
    ("mokhtasar_fawaed — صفحات",          "SELECT COUNT(DISTINCT page) FROM mokhtasar_fawaed",                                         604),
    ("ayah_content_nozool — آيات نزول",   "SELECT COUNT(*) FROM ayah_content_nozool",                                                  201),
]


def main() -> int:
    print(f"\n{BOLD}=== Quranic Scholar DB Verification ==={RESET}")
    print(f"Database: {DB_PATH}\n")

    if not os.path.exists(DB_PATH):
        print(f"{RED}ERROR: Database not found at '{DB_PATH}'{RESET}")
        return 1

    conn = sqlite3.connect(DB_PATH)
    all_passed = True

    for label, sql, expected in CHECKS:
        try:
            actual = conn.execute(sql).fetchone()[0]
            ok = actual == expected
            mark = f"{GREEN}✓{RESET}" if ok else f"{RED}✗{RESET}"
            status = f"got {actual}" if not ok else str(actual)
            print(f"  {mark}  {label:<45} {status}  (expected {expected})")
            if not ok:
                all_passed = False
        except sqlite3.OperationalError as e:
            print(f"  {RED}✗{RESET}  {label:<45} ERROR: {e}")
            all_passed = False

    conn.close()

    print()
    if all_passed:
        print(f"{GREEN}{BOLD}✓ All checks passed — database is valid.{RESET}\n")
        return 0
    else:
        print(f"{RED}{BOLD}✗ Some checks failed — review output above.{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
