"""Pydantic v2 response models for Quranic Scholar MCP."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, model_validator

# عدد آيات كل سورة — مستخرج من surah_stats
SURAH_AYAH_COUNTS: dict[int, int] = {
    1: 7, 2: 286, 3: 200, 4: 176, 5: 120, 6: 165, 7: 206, 8: 75, 9: 129,
    10: 109, 11: 123, 12: 111, 13: 43, 14: 52, 15: 99, 16: 128, 17: 111,
    18: 110, 19: 98, 20: 135, 21: 112, 22: 78, 23: 118, 24: 64, 25: 77,
    26: 227, 27: 93, 28: 88, 29: 69, 30: 60, 31: 34, 32: 30, 33: 73,
    34: 54, 35: 45, 36: 83, 37: 182, 38: 88, 39: 75, 40: 85, 41: 54,
    42: 53, 43: 89, 44: 59, 45: 37, 46: 35, 47: 38, 48: 29, 49: 18,
    50: 45, 51: 60, 52: 49, 53: 62, 54: 55, 55: 78, 56: 96, 57: 29,
    58: 22, 59: 24, 60: 13, 61: 14, 62: 11, 63: 11, 64: 18, 65: 12,
    66: 12, 67: 30, 68: 52, 69: 52, 70: 44, 71: 28, 72: 28, 73: 20,
    74: 56, 75: 40, 76: 31, 77: 50, 78: 40, 79: 46, 80: 42, 81: 29,
    82: 19, 83: 36, 84: 25, 85: 22, 86: 17, 87: 19, 88: 26, 89: 30,
    90: 20, 91: 15, 92: 21, 93: 11, 94: 8, 95: 8, 96: 19, 97: 5,
    98: 8, 99: 8, 100: 11, 101: 11, 102: 8, 103: 3, 104: 9, 105: 5,
    106: 4, 107: 7, 108: 3, 109: 6, 110: 3, 111: 5, 112: 4, 113: 5,
    114: 6,
}


class TafsirSource(StrEnum):
    tabary = "tabary"
    katheer = "katheer"
    baghawy = "baghawy"
    saadi = "saadi"
    moyassar = "moyassar"
    mukhtasar_ar = "mukhtasar_ar"
    mukhtasar_en = "mukhtasar_en"
    mukhtasar_bn = "mukhtasar_bn"


TAFSIR_ATTRIBUTIONS: dict[TafsirSource, str] = {
    TafsirSource.tabary:      "تفسير الإمام الطبري (جامع البيان)، أبو جعفر الطبري (ت. 310هـ)",
    TafsirSource.katheer:     "تفسير ابن كثير، أبو الفداء إسماعيل بن كثير (ت. 774هـ)",
    TafsirSource.baghawy:     "تفسير البغوي (معالم التنزيل)، الحسين بن مسعود البغوي (ت. 510هـ)",
    TafsirSource.saadi:       "تيسير الكريم الرحمن، عبد الرحمن بن ناصر السعدي (ت. 1376هـ)",
    TafsirSource.moyassar:    "التفسير الميسر، مجمع الملك فهد لطباعة المصحف الشريف",
    TafsirSource.mukhtasar_ar: "المختصر في تفسير القرآن الكريم (عربي)",
    TafsirSource.mukhtasar_en: "Concise Quran Commentary (English)",
    TafsirSource.mukhtasar_bn: "সংক্ষিপ্ত তাফসীর (Bengali)",
}


class AyahReference(BaseModel):
    surah: int = Field(ge=1, le=114, description="رقم السورة")
    ayah: int = Field(ge=1, description="رقم الآية")

    @model_validator(mode="after")
    def ayah_within_surah_bounds(self) -> "AyahReference":
        max_ayah = SURAH_AYAH_COUNTS[self.surah]
        if self.ayah > max_ayah:
            raise ValueError(
                f"السورة {self.surah} تحتوي على {max_ayah} آية فقط، "
                f"الرقم المُدخل {self.ayah} خارج النطاق."
            )
        return self


class AyahResponse(BaseModel):
    surah: int
    ayah: int
    text: str
    tajweed: str | None = None
    irab: str | None = None
    word_count: int


class TafsirEntry(BaseModel):
    source: TafsirSource
    attribution: str
    text: str


class TafsirResponse(BaseModel):
    surah: int
    ayah: int
    tafsirs: list[TafsirEntry]


class WordAnalysis(BaseModel):
    word_no: int
    word: str
    meaning: str | None = None
    irab: str | None = None
    sarf: str | None = None
    root: str | None = None
    frequency: int | None = None


class SurahInfo(BaseModel):
    surah_no: int
    names: list[str]
    revelation_type: str
    ayah_count: int
    revelation_order: int
    virtues: str | None
    objectives: str | None
    statistics: dict[str, Any]
