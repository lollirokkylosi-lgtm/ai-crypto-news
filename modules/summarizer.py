from typing import Optional
from .database import Article


class AISummarizer:
    """Genera riassunti con IA"""

    def __init__(self):
        self.client = None
        self.model = None

    def _ensure_client(self, config: dict):
        """Inizializza client AI se necessario"""
        if self.client is None:
            model = config.get('model', 'gpt-3.5-turbo')

            # Prova OpenAI
            try:
                import openai
                openai.api_key = __import__('os').environ.get('OPENAI_API_KEY', '')
                if openai.api_key:
                    self.client = openai
                    self.model = model
                    self.provider = 'openai'
                    return
            except ImportError:
                pass

            # Prova Anthropic
            try:
                import anthropic
                anthropic_api_key = __import__('os').environ.get('ANTHROPIC_API_KEY', '')
                if anthropic_api_key:
                    self.client = anthropic.Anthropic(api_key=anthropic_api_key)
                    self.model = model
                    self.provider = 'anthropic'
                    return
            except ImportError:
                pass

    def summarize(self, article: Article, config: dict) -> str:
        """Genera riassunto IA"""
        self._ensure_client(config)

        if self.client is None:
            # Fallback: estrai prime frasi
            text = article.summary or article.title
            sentences = text.split('. ')[:3]
            return '. '.join(sentences) + '.' if sentences else "Nessun riassunto disponibile"

        system_prompt = config.get('system_prompt', 'Scrivi un riassunto breve e chiaro.')
        user_prompt = f"""Articolo: {article.title}

Testo: {article.summary[:2000] if article.summary else ''}

Scrivi un riassunto in italiano (max 150 parole)."""

        try:
            if self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=300,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()

            elif self.provider == 'anthropic':
                response = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=300,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                return response.content[0].text.strip()

        except Exception as e:
            print(f"  ❌ Errore IA: {e}")
            # Fallback
            text = article.summary or article.title
            sentences = text.split('. ')[:3]
            return '. '.join(sentences) + '.' if sentences else "Riassunto non disponibile"

        return "Riassunto non disponibile"
