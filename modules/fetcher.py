import feedparser
import requests
import os
from datetime import datetime, timedelta
from typing import List
from .database import Article


class NewsFetcher:
    """Recupera notizie da RSS, GitHub e Web"""

    def __init__(self, sources_config: dict):
        self.sources = sources_config
        # Configura User-Agent per evitare blocchi
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AI-Crypto-News-Digest/1.0'
        })

    def fetch_rss(self, url: str, source_name: str, days_back: int = 1) -> List[Article]:
        """Recupera articoli da un feed RSS"""
        articles = []
        cutoff_date = datetime.now() - timedelta(days=days_back)

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            feed = feedparser.parse(response.content)

            for entry in feed.entries:
                # Parsing data pubblicazione
                published_date = self._parse_date(entry)

                # Salta articoli troppo vecchi
                if published_date and published_date < cutoff_date:
                    continue

                # Crea articolo
                article = Article(
                    title=entry.get('title', 'Senza titolo'),
                    url=entry.get('link', ''),
                    source=source_name,
                    publish_date=published_date.strftime('%Y-%m-%d %H:%M') if published_date else datetime.now().strftime('%Y-%m-%d %H:%M'),
                    summary=entry.get('summary', '')[:500] if entry.get('summary') else '',
                    category='',  # Sarà categorizzato dopo
                    score=0.0
                )
                articles.append(article)

        except Exception as e:
            print(f"  ⚠️ Errore RSS {source_name}: {e}")

        return articles

    def fetch_github_releases(self, repo: dict, days_back: int = 1) -> List[Article]:
        """Recupera release GitHub"""
        articles = []
        cutoff_date = datetime.now() - timedelta(days=days_back)

        # Usa token se disponibile
        token = os.getenv('GITHUB_TOKEN', '')
        headers = {'Authorization': f'token {token}'} if token else {}

        try:
            url = f"https://api.github.com/repos/{repo['owner']}/{repo['name']}/releases"
            response = self.session.get(url, headers=headers, timeout=10)

            if response.status_code == 403:  # Rate limit
                print(f"  ⚠️ Rate limit GitHub per {repo['name']}")
                return articles

            response.raise_for_status()
            releases = response.json()

            for release in releases[:5]:  # Max 5 release
                published_date = datetime.strptime(
                    release['published_at'], '%Y-%m-%dT%H:%M:%SZ'
                )

                if published_date < cutoff_date:
                    continue

                article = Article(
                    title=f"[GitHub] {repo['name']}: {release['name']}",
                    url=release.get('html_url', ''),
                    source=repo['name'],
                    publish_date=published_date.strftime('%Y-%m-%d %H:%M'),
                    summary=release.get('body', '')[:500] if release.get('body') else '',
                    category='TECH',
                    score=0.0
                )
                articles.append(article)

        except Exception as e:
            print(f"  ⚠️ Errore GitHub {repo['name']}: {e}")

        return articles

    def search_web(self, query: str, days_back: int = 1) -> List[Article]:
        """Ricerca web (placeholder - richiede Brave API)"""
        # TODO: Implementare con Brave Search API
        return []

    def _parse_date(self, entry) -> datetime:
        """Parsa la data da un entry RSS"""
        date_fields = ['published_parsed', 'updated_parsed', 'created_parsed']

        for field in date_fields:
            if hasattr(entry, field) and getattr(entry, field):
                try:
                    from time import struct_time
                    date_tuple = getattr(entry, field)
                    if isinstance(date_tuple, struct_time):
                        return datetime(*date_tuple[:6])
                except Exception:
                    continue

        return None
