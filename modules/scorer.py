from datetime import datetime, timedelta
from typing import List
from .database import Article


class NewsScorer:
    """Calcola punteggio rilevanza articoli"""

    def __init__(self, scoring_config: dict):
        self.config = scoring_config
        self.min_score = scoring_config.get('min_score', 5.0)
        self.priority_boost = scoring_config.get('priority_boost', 2.0)
        self.priority_sources = scoring_config.get('priority_sources', [])
        self.keyword_boosts = scoring_config.get('keyword_boosts', {})
        self.keyword_penalties = scoring_config.get('keyword_penalties', [])

    def calculate_score(self, article: Article) -> float:
        """Calcola punteggio per un articolo"""
        score = 5.0  # Punteggio base

        # Bonus fonte prioritaria
        if article.source in self.priority_sources:
            score += self.priority_boost

        # Bonus recency
        published = self._parse_date(article.publish_date)
        if published:
            age_hours = (datetime.now() - published).total_seconds() / 3600
            if age_hours < 24:
                score += 1.5
            elif age_hours < 48:
                score += 0.5

        # Keyword boosts
        text = (article.title + " " + article.summary).lower()
        for keyword, boost in self.keyword_boosts.items():
            if keyword.lower() in text:
                score += boost

        # Penalità
        for penalty_word in self.keyword_penalties:
            if penalty_word.lower() in text:
                score -= 1.0

        # Penalità articoli vecchi
        if published:
            age_days = (datetime.now() - published).days
            if age_days > 7:
                score -= 2.0

        # Dominio affidabilità (placeholder)
        if 'blogspot' in article.url or 'wordpress' in article.url:
            score -= 0.5

        return max(0.0, score)

    def _parse_date(self, date_str: str):
        """Parsa stringa data"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        except Exception:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d')
            except Exception:
                return None
