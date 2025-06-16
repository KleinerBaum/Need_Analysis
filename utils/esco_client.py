"""Client for interacting with the ESCO REST API."""

from __future__ import annotations

import logging
from typing import Dict, List, Union

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://ec.europa.eu/esco/api"


def search_skills(query: str, *, language: str = "en", limit: int = 10) -> List[str]:
    """Search skills in ESCO and return a list of titles.

    Args:
        query: Text query for the search endpoint.
        language: ISO language code, defaults to "en".
        limit: Maximum number of results to return.

    Returns:
        List of skill titles.
    """
    params: Dict[str, Union[str, int]] = {
        "text": query,
        "language": language,
        "type": "skill",
        "limit": limit,
    }
    try:
        response = requests.get(f"{BASE_URL}/search", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get("_embedded", {}).get("results", [])
        return [r.get("title") for r in results if r.get("title")]
    except Exception as exc:  # pragma: no cover - network
        logger.warning("ESCO API request failed: %s", exc)
        return []
