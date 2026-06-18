import requests
from bs4 import BeautifulSoup
from pathlib import Path
import logging
import time

logger = logging.getLogger(__name__)


def scrape_url(url: str, save_dir: Path = None) -> dict:
    """Scrape le contenu textuel d'une URL."""
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except Exception as e:
        logger.warning(f"Impossible de récupérer {url}: {e}")
        return {"text": "", "source": url, "type": "web", "skipped": True}

    html = response.text

    if save_dir:
        save_dir.mkdir(parents=True, exist_ok=True)
        safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_")[:100]
        (save_dir / f"{safe_name}.html").write_text(html, encoding="utf-8")

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)

    if len(text.strip()) < 50:
        return {"text": "", "source": url, "type": "web", "skipped": True}

    return {"text": text, "source": url, "type": "web", "skipped": False}


def scrape_urls(urls: list[str], save_dir: Path = None, delay: float = 1.0) -> list[dict]:
    """Scrape une liste d'URLs avec délai entre chaque requête."""
    results = []
    for url in urls:
        results.append(scrape_url(url, save_dir=save_dir))
        time.sleep(delay)
    return results
