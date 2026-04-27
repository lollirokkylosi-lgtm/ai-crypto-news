#!/bin/bash
# Script di setup per automazione giornaliera
# Esegue il digest ogni mattina alle 8:00

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/digest.log"

# Crea directory log se non esiste
mkdir -p "$LOG_DIR"

# Aggiungi cron job (solo se non già presente)
CRON_JOB="0 8 * * * cd $SCRIPT_DIR && /usr/bin/python3 main.py >> $LOG_FILE 2>&1"

# Controlla se cron job esiste già
if crontab -l 2>/dev/null | grep -q "ai-crypto-news"; then
    echo "✅ Cron job già presente"
else
    # Aggiungi cron job
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ Cron job aggiunto:"
    echo "   $CRON_JOB"
    echo ""
    echo "📄 Log: $LOG_FILE"
fi

# Mostra cron job attuali
echo ""
echo "📋 Cron job attuali:"
crontab -l 2>/dev/null || echo "   Nessun cron job"

# Test esecuzione
echo ""
echo "🧪 Test esecuzione (dry-run)..."
cd "$SCRIPT_DIR" && /usr/bin/python3 main.py --dry-run

echo ""
echo "✅ Setup completato!"
echo ""
echo "💡 Per modificare l'orario, esegui: crontab -e"
echo "💡 Per vedere i log: tail -f $LOG_FILE"
echo "💡 Per disabilitare: crontab -e e rimuovi la riga"
