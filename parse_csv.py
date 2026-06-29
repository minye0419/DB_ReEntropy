import pandas as pd
from config import TENSILE_KEYWORDS, PROCESS_KEYWORDS, CRYO_KEYWORDS


def _contains_keyword(text: str, keywords: list[str]) -> bool:
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def _build_search_text(row: pd.Series) -> str:
    parts = [
        str(row.get("Abstract", "") or ""),
        str(row.get("Author Keywords", "") or ""),
        str(row.get("Keywords Plus", "") or ""),
    ]
    return " ".join(parts)


def _priority_grade(tensile: bool, process: bool, cryo: bool) -> str:
    if tensile and process and cryo:
        return "⭐⭐⭐"
    if tensile and process:
        return "⭐⭐"
    if tensile or process:
        return "⭐"
    return "📄"


def _format_author_year(row: pd.Series) -> str:
    author = str(row.get("Author", "") or "").strip()
    year = str(row.get("Publication Year", "") or "").strip()

    if author:
        first_author = author.split(";")[0].strip()
        last_name = first_author.split(",")[0].strip()
        author_str = f"{last_name} et al." if ";" in author else last_name
    else:
        author_str = "Unknown"

    return f"{author_str}, {year}" if year else author_str


PRIORITY_ORDER = {"⭐⭐⭐": 0, "⭐⭐": 1, "⭐": 2, "📄": 3}


def analyze(df: pd.DataFrame) -> pd.DataFrame:
    results = []

    for _, row in df.iterrows():
        text = _build_search_text(row)
        tensile = _contains_keyword(text, TENSILE_KEYWORDS)
        process = _contains_keyword(text, PROCESS_KEYWORDS)
        cryo = _contains_keyword(text, CRYO_KEYWORDS)
        grade = _priority_grade(tensile, process, cryo)

        results.append(
            {
                "Title": str(row.get("Title", "") or ""),
                "Author / Year": _format_author_year(row),
                "DOI": str(row.get("DOI", "") or "").strip(),
                "Document Type": str(row.get("Item Type", "") or "").strip(),
                "인장물성": "✅" if tensile else "❌",
                "공정변수": "✅" if process else "❌",
                "77K": "⭐" if cryo else "❌",
                "우선순위": grade,
                "_sort_key": PRIORITY_ORDER[grade],
            }
        )

    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values("_sort_key").drop(columns=["_sort_key"]).reset_index(drop=True)
    return result_df


def load_and_analyze(file) -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(file, encoding="utf-8-sig")
    result_df = analyze(df)

    total = len(result_df)
    counts = result_df["우선순위"].value_counts()
    stats = {
        "total": total,
        "⭐⭐⭐": int(counts.get("⭐⭐⭐", 0)),
        "⭐⭐": int(counts.get("⭐⭐", 0)),
        "⭐": int(counts.get("⭐", 0)),
        "📄": int(counts.get("📄", 0)),
    }
    return result_df, stats
