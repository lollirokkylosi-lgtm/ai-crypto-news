#!/usr/bin/env python3
"""
AI & Crypto News Digest
Aggrega notizie di Intelligenza Artificiale e Criptovalute
"""

import os
import sys
import yaml
import argparse
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from modules.database import NewsDatabase
from modules.fetcher import NewsFetcher
from modules.deduplicator import Deduplicator
from modules.scorer import NewsScorer
from modules.summarizer import AISummarizer
from modules.notifier import Notifier

console = Console()

# Carica configurazione
def load_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def create_digest(config, days_back=1, dry_run=False):
    """
    Crea il digest giornaliero di notizie AI & Crypto
    """
    console.rule("[bold magenta]🤖 AI & Crypto News Digest[/bold magenta]")
    console.print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    console.print(f"🔍 Ricerca notizie degli ultimi {days_back} giorno/i\n")

    # Inizializza componenti
    db = NewsDatabase()
    fetcher = NewsFetcher(config["sources"])
    deduplicator = Deduplicator()
    scorer = NewsScorer(config["scoring"])
    summarizer = AISummarizer()
    notifier = Notifier(config.get("notifications", {}))

    # --- FASE 1: Raccolta ---
    console.print("[cyan]📡 Raccolta notizie...[/cyan]")
    all_articles = []

    # RSS Sources
    for source in config["sources"]["rss"]:
        articles = fetcher.fetch_rss(source["url"], source["name"], days_back)
        all_articles.extend(articles)
        console.print(f"  ✓ {source['name']}: {len(articles)} articoli")

    # GitHub Releases
    if config["sources"].get("github"):
        for repo in config["sources"]["github"]:
            releases = fetcher.fetch_github_releases(repo, days_back)
            all_articles.extend(releases)
            console.print(f"  ✓ {repo['name']}: {len(releases)} release")

    # Twitter/KOL (Placeholder)
    if config["sources"].get("twitter"):
        console.print("  🐦 Twitter: [dim]skippato (richiede API)[/dim]")

    # Web Search
    if config["sources"].get("web_search"):
        for query in config["sources"]["web_search"]:
            results = fetcher.search_web(query, days_back)
            all_articles.extend(results)
            console.print(f"  ✓ Web: {len(results)} risultati per '{query}'")

    console.print(f"\n📊 Totale articoli raccolti: [bold]{len(all_articles)}[/bold]")

    if not all_articles:
        console.print("[yellow]⚠️ Nessuna notizia trovata[/yellow]")
        return

    # --- FASE 2: Deduplicazione ---
    console.print(f"\n[cyan]🧹 Rimozione duplicati...[/cyan]")
    unique_articles = deduplicator.remove_duplicates(all_articles)
    console.print(f"  ✓ Articoli unici: {len(unique_articles)}")

    # --- FASE 3: Scoring ---
    console.print(f"\n[cyan]⭐ Calcolo punteggi...[/cyan]")
    scored_articles = []
    for article in unique_articles:
        score = scorer.calculate_score(article)
        article.score = score
        if score >= config["scoring"]["min_score"]:
            scored_articles.append(article)

    # Ordina per punteggio
    scored_articles.sort(key=lambda x: x.score, reverse=True)
    console.print(f"  ✓ Articoli rilevanti (score ≥ {config['scoring']['min_score']}): {len(scored_articles)}")

    # Mostra top 10
    if not dry_run:
        table = Table(title="📰 Top 10 Notizie")
        table.add_column("#", style="dim")
        table.add_column("Titolo", max_width=60)
        table.add_column("Fonte")
        table.add_column("Score", justify="right", style="green")

        for i, art in enumerate(scored_articles[:10], 1):
            table.add_row(str(i), art.title[:60], art.source, f"{art.score:.1f}")
        console.print(table)

    # --- FASE 4: Riassunto con IA ---
    console.print(f"\n[cyan]🧠 Generazione riassunti IA...[/cyan]")
    summary_limit = min(config["output"].get("max_articles", 10), len(scored_articles))

    if dry_run:
        console.print("  [dim]Modalità test - saltata generazione IA[/dim]")
        summarized = scored_articles[:summary_limit]
    else:
        summarized = []
        for i, article in enumerate(scored_articles[:summary_limit], 1):
            try:
                console.print(f"  [{i}/{summary_limit}] Riassumo: {article.title[:40]}...")
                summary = summarizer.summarize(article, config["ai"])
                article.summary = summary
                summarized.append(article)
            except Exception as e:
                console.print(f"  ❌ Errore: {e}")
                article.summary = "Riassunto non disponibile"
                summarized.append(article)

    # --- FASE 5: Salvataggio e Notifica ---
    console.print(f"\n[cyan]💾 Salvataggio...[/cyan]")

    # Salva nel DB
    for article in summarized:
        db.save_article(article)

    stats = db.get_stats()
    console.print(f"  ✓ Database: {stats['total_articles']} articoli totali")

    # Genera digest
    digest_id = datetime.now().strftime("%Y%m%d_%H%M")

    # Invia notifiche
    if not dry_run and config["notifications"]["email"]["enabled"]:
        console.print(f"\n[cyan]📧 Invio email...[/cyan]")
        notifier.send_email_digest(
            articles=summarized,
            date=datetime.now(),
            email_config=config["notifications"]["email"]
        )

    if not dry_run and config["notifications"]["discord"]["enabled"]:
        console.print(f"[cyan]💬 Invio Discord...[/cyan]")
        notifier.send_discord_digest(summarized, config["notifications"]["discord"])

    # Genera file HTML
    if config["output"]["html"]["enabled"]:
        console.print(f"[cyan]🌐 Generazione pagina HTML...[/cyan]")
        html_path = notifier.generate_html_digest(summarized, digest_id, config)
        console.print(f"  ✓ Pagina: {html_path}")

    console.print(f"\n[bold green]✅ Digest completato![/bold green]")
    console.print(f"📁 ID: {digest_id}")
    console.print(f"📄 Articoli: {len(summarized)}")

    return True


def main():
    parser = argparse.ArgumentParser(description="AI & Crypto News Digest Generator")
    parser.add_argument("--dry-run", action="store_true", help="Esegui senza inviare notifiche")
    parser.add_argument("--days", type=int, default=1, help="Giorni indietro (default: 1)")
    parser.add_argument("--limit", type=int, default=10, help="Limita articoli (default: 10)")
    parser.add_argument("--config", default="config.yaml", help="File config")

    args = parser.parse_args()

    config = load_config(args.config)

    # Override limiti
    if args.limit:
        config["output"]["max_articles"] = args.limit

    try:
        create_digest(config, days_back=args.days, dry_run=args.dry_run)
    except Exception as e:
        console.print(f"[bold red]❌ Errore: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
