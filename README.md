# 🤖 AI & Crypto News Digest

Sistema avanzato per l'aggregazione automatica, l'analisi e la distribuzione di notizie su Intelligenza Artificiale e Criptovalute.

## 🌟 Caratteristiche

- **Multi-source**: Raccoglie da 15+ feed RSS, GitHub releases
- **Smart Scoring**: Algoritmo personalizzato per prioritizzare notizie rilevanti
- **AI Summarization**: Genera riassunti in italiano con OpenAI/Anthropic
- **Duplicates Removal**: Elimina articoli simili o duplicati
- **Multi-format Output**: HTML, Email, Discord, JSON
- **Personalizzazione**: Aggiungi facilmente nuove fonti RSS
- **Categorie automatiche**: AI, Crypto, Tech, Altro

## 📦 Installazione

### 1. Requisiti
```bash
Python 3.8+
```

### 2. Configurazione
```bash
cd ai-crypto-news
cp .env.example .env
# Modifica .env con le tue API keys
```

### 3. Installa dipendenze
```bash
pip install -r requirements.txt
```

## 🚀 Utilizzo

### Modalità Test (Dry Run)
```bash
python main.py --dry-run
```
Genera il digest senza inviare notifiche.

### Modalità Normale
```bash
python main.py
```

### Opzioni
```bash
python main.py --days 2    # Ultimi 2 giorni
python main.py --limit 5   # Solo 5 articoli
python main.py --config custom.yaml
```

## 📝 Configurazione

Modifica `config.yaml` per personalizzare:

- **Fonti RSS**: Aggiungi i tuoi feed preferiti
- **Scoring**: Regola pesi e soglie
- **Output**: Attiva/disattiva canali notifica
- **AI**: Configura modello e prompt

### Fonti Incluse (Default)

**AI/ML:**
- OpenAI Blog
- Anthropic News  
- MIT Tech Review
- Hacker News (AI)
- TechCrunch AI
- VentureBeat AI
- Wired AI

**Crypto:**
- CoinDesk
- CoinTelegraph
- The Block
- Decrypt
- CryptoSlate

**GitHub:**
- OpenAI GPT
- vLLM
- LangChain
- Ollama
- Bitcoin Core
- Ethereum

## 🔧 Come Funziona

```
1. Fetch     → RSS + GitHub → Articoli raw
   ↓
2. Dedup     → Rimuove duplicati (85% similarità)
   ↓
3. Score     → Calcola rilevanza (0-10)
   ↓
4. Filter    → Toglie sotto la soglia (6.0)
   ↓
5. Summarize → Genera riassunti con IA
   ↓
6. Output    → HTML + Email + Discord
```

## 📊 Algoritmo di Scoring

Ogni articolo riceve un punteggio base **5.0**:

| Fattore | Bonus/Penalty |
|---------|---------------|
| Fonte prioritaria | +2.0 |
| Meno di 24h | +1.5 |
| AI keyword | +0.5-0.8 |
| Crypto keyword | +0.8-1.0 |
| Summary lunga | +0.5 |
| Dominio non affidabile | -1.0 |
| Oltre 7 giorni | -2.0 |

**Soglia minima**: 6.0 (configurabile)

## 🎯 Output

### HTML Page
Pagina web responsive con:
- Statistiche (totale, AI, Crypto)
- Cards per ogni articolo
- Categorie colorate (AI 🟢, Crypto 🟠)
- Link diretti

### Email Digest
Inviata via SMTP con:
- Formattazione HTML
- Sintesi di ogni articolo
- Link originali

### Discord
Embed con:
- Top 5 articoli
- Score e categoria
- Link immediati

## 🔐 Sicurezza

- **Niente chiavi nel Git**: Tutto in `.env` (nel `.gitignore`)
- **Rate limit**: Gestione automatica API GitHub
- **Error handling**: Fallback senza IA se API mancante

## ⚙️ Automazione

### Linux/Mac (Cron)
```bash
# Ogni mattina alle 8
0 8 * * * cd /path/to/ai-crypto-news && python main.py >> logs/digest.log 2>&1
```

### Windows (Task Scheduler)
1. Task Scheduler → Create Task
2. Trigger: Daily 8:00
3. Action: `python C:\path\main.py`
4. Start in: `C:\path\ai-crypto-news`

## 📈 Estensioni

### Aggiungere Nuova Fonte RSS
```yaml
sources:
  rss:
    - name: "Mio Blog Preferito"
      url: "https://blog.example.com/feed.xml"
```

### Aggiungere Repository GitHub
```yaml
sources:
  github:
    - name: "Mio Progetto"
      owner: "username"
      name: "repo"
```

### Nuove Keyword
```yaml
scoring:
  keyword_boosts:
    "rag": 0.8  # Retrieval-Augmented Generation
    "mcp": 0.6  # Model Context Protocol
```

## 📞 Supporto

Per problemi o suggerimenti, controlla:
1. Log file: `ai_crypto_news.log`
2. Output console: `--dry-run` per debug

## 📄 Licenza

MIT - Liberamente modificabile

## 🙏 Crediti

Basato sul pattern multi-source di awesome-openclaw-usecases

---

**Happy Coding! 🚀**