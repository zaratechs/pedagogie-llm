import pandas as pd
import re
import hashlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """Nettoie le texte brut : supprime les numéros de page, espaces excessifs."""
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def build_dataframe(documents: list[dict]) -> pd.DataFrame:
    """Convertit une liste de dicts en DataFrame nettoyé et dédupliqué."""
    df = pd.DataFrame(documents)

    skipped = df[df["skipped"] == True]
    if not skipped.empty:
        logger.warning(f"Documents ignorés : {len(skipped)} — {skipped['source'].tolist()}")

    df = df[df["skipped"] == False].copy()
    df["text"] = df["text"].apply(clean_text)
    df = df[df["text"].str.len() >= 50].copy()
    df["content_hash"] = df["text"].apply(lambda t: hashlib.sha256(t.encode()).hexdigest())
    df = df.drop_duplicates(subset=["content_hash"]).reset_index(drop=True)

    return df[["text", "source", "type", "content_hash"]]


def save_skipped(documents: list[dict], errors_dir: Path) -> None:
    """Sauvegarde les documents ignorés dans un CSV pour révision."""
    errors_dir.mkdir(parents=True, exist_ok=True)
    skipped = [d for d in documents if d.get("skipped")]
    if skipped:
        pd.DataFrame(skipped).to_csv(errors_dir / "skipped.csv", index=False)
