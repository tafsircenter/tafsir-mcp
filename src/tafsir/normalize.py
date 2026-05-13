"""Arabic text normalization utilities."""

import re

import pyarabic.araby as araby

_ALEF_VARIANTS = re.compile(r"[آأإٱ]")
_WHITESPACE = re.compile(r"\s+")


def normalize_arabic(text: str, unify_taa_marbouta: bool = False) -> str:
    text = araby.strip_tashkeel(text)
    text = _ALEF_VARIANTS.sub("ا", text)
    text = text.replace("ى", "ي")
    text = text.replace("ء", "")
    if unify_taa_marbouta:
        text = text.replace("ة", "ه")
    text = _WHITESPACE.sub(" ", text)
    return text.strip()


def reconstruct_ayah(rasm_rows: list[dict]) -> str:
    sorted_rows = sorted(rasm_rows, key=lambda r: r["wordNo"])
    return " ".join(row["word"] for row in sorted_rows)
