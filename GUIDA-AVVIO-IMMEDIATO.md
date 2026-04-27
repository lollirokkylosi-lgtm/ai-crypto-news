# 🚀 Guida Avvio Immediato

Inizia in **5 minuti** con AI & Crypto News Digest!

## 1. Installazione Rapida

```bash
cd /path/to/ai-crypto-news
pip install -r requirements.txt
```

## 2. Configurazione Base

```bash
cp .env.example .env
# Modifica .env con le tue chiavi API (opzionale)
```

## 3. Test del Sistema

```bash
python main.py --dry-run
```

Questo scaricherà le notizie e genererà un HTML senza inviare notifiche.

## 4. Esecuzione Reale

```bash
python main.py
```

Nota: senza API IA configurate, il sistema usa riassunti di fallback (primi paragrafi).

## 5. Automazione Giornaliera

### Linux/Mac (Cron)
```bash
0 8 * * * cd /path/to/ai-crypto-news && python main.py >> logs/digest.log 2>&1
```

### Windows (Task Scheduler)
1. Apri Task Scheduler
2. Crea task giornaliero alle 8:00
3. Azione: `python C:\path\main.py`
4. Cartella: `C:\path\ai-crypto-news`

## 6. Personalizzazione Veloce

Modifica `config.yaml`:

```yaml
scoring:
  min_score: 5.0  # Più basso = più articoli

output:
  html:
    enabled: true
  max_articles: 20  # Più articoli nel digest
```

## 7. Verifica Output

Apri il file generato:
```bash
open output/digest_*.html
```

## 🎯 FAQ

**D: Il digest è vuoto?**
R: Controlla che le URL RSS siano raggiungibili. Alcune potrebbero essere temporaneamente offline.

**D: Gli articoli sono vecchi?**
R: Il sistema filtra automaticamente articoli >7 giorni. Configura `days_back` se necessario.

**D: Come aggiungo nuove fonti?**
R: Modifica `config.yaml` → `sources.rss` con nome e URL del feed RSS.

**D: Posso usare Claude invece di GPT?**
R: Sì! Imposta `ANTHROPIC_API_KEY` nel .env e modifica `ai.model`.

**D: Qual è la soglia minima di score?**
R: 6.0 di default. Modifica `scoring.min_score`.

## 📊 Esempio Output

```
📡 Raccolta notizie...
  ✓ OpenAI Blog: 5 articoli
  ✓ CoinDesk: 8 articoli
  ✓ vLLM: 0 release

📊 Totale articoli raccolti: 69

🧹 Rimozione duplicati...
  ✓ Articoli unici: 69

⭐ Calcolo punteggi...
  ✓ Articoli rilevanti (score ≥ 6.0): 10

🧠 Generazione riassunti IA...
  [1/10] Riassumo: Bitcoin reaches new high...

🌐 Generazione pagina HTML...
  ✓ Pagina: output/digest_20260427_0824.html

✅ Digest completato!
📄 Articoli: 10
```

## 🔧 Troubleshooting

### Timeout RSS
Aumenta il timeout in `modules/fetcher.py`:
```python
response = self.session.get(url, timeout=20)  # default 10
```

### Rate Limit GitHub
Ottieni un token gratuito da https://github.com/settings/tokens

### Nessun riassunto IA
Imposta `OPENAI_API_KEY` o `ANTHROPIC_API_KEY` nel .env

## 📈 Prossimi Passi

1. Configura invio email (SMTP)
2. Aggiungi webhook Discord
3. Personalizza keyword di scoring
4. Aggiungi nuove fonti RSS

---

**Buon divertimento! 🚀**