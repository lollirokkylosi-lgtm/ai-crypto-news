import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class Article:
    """Rappresenta un articolo"""
    title: str
    url: str
    source: str
    publish_date: str
    summary: str = ""
    category: str = ""
    score: float = 0.0

    def to_dict(self):
        return asdict(self)


class NewsDatabase:
    """Gestione database SQLite per archiviare articoli"""

    def __init__(self, db_path: str = "news_digest.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Inizializza le tabelle del database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                source TEXT NOT NULL,
                publish_date TEXT NOT NULL,
                summary TEXT,
                category TEXT DEFAULT '',
                score REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(url)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS execution_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                execution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_articles INTEGER,
                ai_articles INTEGER,
                crypto_articles INTEGER,
                avg_score REAL
            )
        """)

        conn.commit()
        conn.close()

    def save_article(self, article: Article) -> bool:
        """Salva un articolo nel database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT OR REPLACE INTO articles 
                (title, url, source, publish_date, summary, category, score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                article.title,
                article.url,
                article.source,
                article.publish_date,
                article.summary,
                article.category,
                article.score
            ))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Errore salvataggio articolo: {e}")
            return False
        finally:
            conn.close()

    def get_article(self, url: str) -> Optional[Article]:
        """Recupera un articolo per URL"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM articles WHERE url = ?", (url,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Article(
                id=row[0],
                title=row[1],
                url=row[2],
                source=row[3],
                publish_date=row[4],
                summary=row[5],
                category=row[6],
                score=row[7]
            )
        return None

    def get_recent_articles(self, limit: int = 10) -> List[Article]:
        """Recupera gli articoli più recenti"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM articles 
            ORDER BY publish_date DESC 
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        articles = []
        for row in rows:
            articles.append(Article(
                title=row[1],
                url=row[2],
                source=row[3],
                publish_date=row[4],
                summary=row[5],
                category=row[6],
                score=row[7]
            ))
        return articles

    def log_execution(self, stats: Dict):
        """Logga l'esecuzione"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO execution_log 
            (total_articles, ai_articles, crypto_articles, avg_score)
            VALUES (?, ?, ?, ?)
        """, (
            stats.get('total_articles', 0),
            stats.get('ai_articles', 0),
            stats.get('crypto_articles', 0),
            stats.get('avg_score', 0)
        ))

        conn.commit()
        conn.close()

    def get_stats(self) -> Dict:
        """Recupera statistiche database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM articles")
        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT AVG(score) FROM articles 
            WHERE score > 0
        """)
        avg_score = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT COUNT(*) FROM articles 
            WHERE category = 'AI'
        """)
        ai_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM articles 
            WHERE category = 'CRYPTO'
        """)
        crypto_count = cursor.fetchone()[0]

        conn.close()

        return {
            'total_articles': total,
            'avg_score': round(avg_score, 2),
            'ai_articles': ai_count,
            'crypto_articles': crypto_count
        }

    def clear_old_articles(self, days: int = 30):
        """Rimuove articoli più vecchi di N giorni"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM articles 
            WHERE publish_date < date('now', '-' || ? || ' days')
        """, (days,))

        conn.commit()
        deleted = cursor.rowcount
        conn.close()

        return deleted
