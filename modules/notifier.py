import smtplib
import requests
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict
from .database import Article


class Notifier:
    """Gestione notifiche (Email, Discord, HTML)"""

    def __init__(self, config: Dict):
        self.config = config

    def send_email_digest(self, articles: List[Article], date: datetime, email_config: Dict):
        """Invia digest via email"""
        try:
            # Usa variabili d'ambiente se config vuota
            sender = email_config.get('sender', os.getenv('EMAIL_SENDER', ''))
            recipient = email_config.get('recipient', os.getenv('EMAIL_RECIPIENT', ''))
            smtp_host = email_config.get('smtp', {}).get('host', os.getenv('SMTP_HOST', 'smtp.gmail.com'))
            smtp_port = int(email_config.get('smtp', {}).get('port', os.getenv('SMTP_PORT', 587)))
            smtp_tls = email_config.get('smtp', {}).get('tls', os.getenv('SMTP_TLS', 'true').lower() == 'true')
            smtp_user = email_config.get('smtp', {}).get('username', os.getenv('SMTP_USERNAME', ''))
            smtp_pass = email_config.get('smtp', {}).get('password', os.getenv('SMTP_PASSWORD', ''))

            if not sender or not recipient:
                print("  ❌ Email config incompleta")
                return

            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"AI & Crypto News - {date.strftime('%d/%m/%Y')}"
            msg['From'] = sender
            msg['To'] = recipient

            # Genera HTML
            html = self._generate_email_html(articles, date)
            msg.attach(MIMEText(html, 'html'))

            # Invia
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                if smtp_tls:
                    server.starttls()
                if smtp_user and smtp_pass:
                    server.login(smtp_user, smtp_pass)
                server.send_message(msg)

            print(f"  ✓ Email inviata a {recipient}")

        except Exception as e:
            print(f"  ❌ Errore email: {e}")

    def send_discord_digest(self, articles: List[Article], discord_config: Dict):
        """Invia digest su Discord via webhook"""
        try:
            webhook_url = discord_config.get('webhook_url', os.getenv('DISCORD_WEBHOOK_URL', ''))

            if not webhook_url:
                print("  ❌ Discord webhook non configurato")
                return

            # Costruisce embed
            embed = {
                "title": f"📰 AI & Crypto News - {datetime.now().strftime('%d/%m/%Y')}",
                "color": 0x00ff00,
                "fields": [],
                "footer": {"text": f"{len(articles)} articoli"}
            }

            for article in articles[:5]:  # Max 5 articoli
                field = {
                    "name": article.title[:100],
                    "value": f"[{article.source}]({article.url}) - Score: {article.score:.1f}\n{article.summary[:200]}...",
                    "inline": False
                }
                embed["fields"].append(field)

            payload = {"embeds": [embed]}

            response = requests.post(webhook_url, json=payload)
            if response.status_code == 204:
                print("  ✓ Messaggio Discord inviato")
            else:
                print(f"  ❌ Errore Discord: {response.status_code}")

        except Exception as e:
            print(f"  ❌ Errore Discord: {e}")

    def _generate_email_html(self, articles: List[Article], date: datetime) -> str:
        """Genera HTML per email"""
        html = f"""<html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
<h1 style="color: #667eea;">🤖 AI & Crypto News Digest</h1>
<p>Data: {date.strftime('%d/%m/%Y %H:%M')}</p>
<p>Articoli: {len(articles)}</p>
<hr>
"""
        for i, article in enumerate(articles, 1):
            html += f"""<div style="margin: 20px 0; padding: 15px; border-left: 3px solid #667eea; background: #f5f5f5;">
<h2 style="font-size: 1.2em;">{i}. {article.title}</h2>
<p style="color: #666;">Fonte: {article.source} | Score: {article.score:.1f}</p>
<p>{article.summary}</p>
<a href="{article.url}" style="color: #667eea;">Leggi →</a>
</div>"""

        html += "</body></html>"
        return html

    def generate_html_digest(self, articles: List[Article], digest_id: str, config: Dict) -> str:
        """Genera pagina HTML navigabile"""
        html_config = config.get("output", {}).get("html", {})
        output_dir = html_config.get("output_dir", "output")

        os.makedirs(output_dir, exist_ok=True)

        html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI & Crypto News - {datetime.now().strftime('%d/%m/%Y %H:%M')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; text-align: center; border-radius: 10px; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header .date {{ opacity: 0.9; font-size: 1.1em; }}
        .stats {{ display: flex; justify-content: space-around; margin-bottom: 30px; }}
        .stat-box {{ background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1); flex: 1; margin: 0 10px; }}
        .stat-box .number {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .stat-box .label {{ color: #666; margin-top: 5px; }}
        .articles {{ display: flex; flex-direction: column; gap: 20px; }}
        .article {{ background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-left: 4px solid #667eea; }}
        .article-header {{ display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px; }}
        .article-title {{ font-size: 1.3em; font-weight: bold; color: #333; margin-right: 20px; }}
        .article-score {{ background: #667eea; color: white; padding: 5px 10px; border-radius: 20px; font-size: 0.9em; font-weight: bold; }}
        .article-source {{ color: #667eea; font-size: 0.9em; margin-bottom: 10px; font-weight: 500; }}
        .article-summary {{ color: #555; margin-bottom: 15px; line-height: 1.7; }}
        .article-link {{ color: #667eea; text-decoration: none; font-weight: 500; }}
        .article-link:hover {{ text-decoration: underline; }}
        .category {{ display: inline-block; padding: 3px 10px; border-radius: 15px; font-size: 0.8em; font-weight: bold; margin-right: 10px; }}
        .category.ai {{ background: #e8f5e8; color: #2d862d; }}
        .category.crypto {{ background: #fff3e0; color: #e65100; }}
        .category.tech {{ background: #e3f2fd; color: #1565c0; }}
        .footer {{ text-align: center; margin-top: 40px; padding: 20px; color: #999; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI & Crypto News Digest</h1>
            <div class="date">{datetime.now().strftime('%A %d %B %Y %H:%M')}</div>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="number">{len(articles)}</div>
                <div class="label">Articoli</div>
            </div>
            <div class="stat-box">
                <div class="number">{sum(1 for a in articles if any(kw in (a.title + a.summary).lower() for kw in ['ai','gpt','chatgpt','machine','llm','anthropic']))}</div>
                <div class="label">AI</div>
            </div>
            <div class="stat-box">
                <div class="number">{sum(1 for a in articles if any(kw in (a.title + a.summary).lower() for kw in ['bitcoin','crypto','ethereum','blockchain','defi']))}</div>
                <div class="label">Crypto</div>
            </div>
        </div>

        <div class="articles">
"""

        category_class_map = {"AI": "ai", "CRYPTO": "crypto", "TECH": "tech"}

        for i, article in enumerate(articles, 1):
            category = article.category or "ALTRO"
            cat_class = category_class_map.get(category, "")
            cat_badge = f'<span class="category {cat_class}">{category}</span>' if cat_class else ""

            html += f"""
            <div class="article">
                <div class="article-header">
                    <div>
                        {cat_badge}
                        <span class="article-source">{article.source}</span>
                    </div>
                    <span class="article-score">{article.score:.1f} ⭐</span>
                </div>
                <h2 class="article-title">{i}. {article.title}</h2>
                <p class="article-summary">{article.summary}</p>
                <a href="{article.url}" class="article-link" target="_blank">Leggi l'articolo completo →</a>
            </div>
"""

        html += """
        </div>

        <div class="footer">
            Generato automaticamente da AI & Crypto News Digest<br>
            <a href="#" style="color: #667eea;">Iscriviti alla newsletter</a> |
            <a href="#" style="color: #667eea;">Gestisci preferenze</a>
        </div>
    </div>
</body>
</html>
"""

        filepath = os.path.join(output_dir, f"digest_{digest_id}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        return filepath
