from difflib import SequenceMatcher
from typing import List
from .database import Article


class Deduplicator:
    """Rimuove articoli duplicati o molto simili"""

    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold

    def remove_duplicates(self, articles: List[Article]) -> List[Article]:
        """Rimuove duplicati basati su similarità testo"""
        unique_articles = []
        seen_texts = []

        for article in articles:
            # Testo da confrontare (titolo + summary)
            text = (article.title + " " + article.summary).lower().strip()

            # Salta se testo troppo corto
            if len(text) < 10:
                unique_articles.append(article)
                continue

            # Controlla similarità con testi già visti
            is_duplicate = False
            for seen_text in seen_texts:
                similarity = self._similarity(text, seen_text)
                if similarity >= self.similarity_threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_articles.append(article)
                seen_texts.append(text)

        return unique_articles

    def _similarity(self, text1: str, text2: str) -> float:
        """Calcola similarità tra due testi"""
        return SequenceMatcher(None, text1, text2).ratio()
