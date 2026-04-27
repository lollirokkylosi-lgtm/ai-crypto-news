import os
from datetime import datetime
from typing import List, Dict
from .database import Article


class ToolsDirectory:
    """Gestione directory di tool AI e Crypto"""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_tools_page(self, tools_data: Dict[str, List[Dict]], config: Dict) -> str:
        """
        Genera pagina HTML con directory di tool
        """
        ai_tools = tools_data.get('ai_tools', [])
        crypto_tools = tools_data.get('crypto_tools', [])

        # Ordina per voti
        ai_tools.sort(key=lambda x: x.get('votes', 0), reverse=True)
        crypto_tools.sort(key=lambda x: x.get('votes', 0), reverse=True)

        html = self._generate_html(ai_tools, crypto_tools)

        filename = f"tools_{datetime.now().strftime('%Y%m%d')}.html"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        return filepath

    def _generate_html(self, ai_tools: List[Dict], crypto_tools: List[Dict]) -> str:
        """Genera HTML completo"""
        return f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI & Crypto Tools Directory</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        .header h1 {{
            font-size: 3em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 1.2em;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }}
        .stat-box {{
            background: white;
            padding: 25px 40px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        .stat-box:hover {{
            transform: translateY(-5px);
        }}
        .stat-box .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-box .label {{
            color: #666;
            margin-top: 5px;
            font-size: 1.1em;
        }}
        .section {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        .section-title {{
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .section-title.ai {{
            color: #2d862d;
            border-color: #2d862d;
        }}
        .section-title.crypto {{
            color: #e65100;
            border-color: #e65100;
        }}
        .tools-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}
        .tool-card {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            transition: all 0.3s;
            border: 2px solid transparent;
            position: relative;
            overflow: hidden;
        }}
        .tool-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            border-color: #667eea;
        }}
        .tool-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            opacity: 0;
            transition: opacity 0.3s;
        }}
        .tool-card:hover::before {{
            opacity: 1;
        }}
        .tool-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .tool-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .tool-badge.ai {{
            background: #e8f5e8;
            color: #2d862d;
        }}
        .tool-badge.crypto {{
            background: #fff3e0;
            color: #e65100;
        }}
        .tool-description {{
            color: #666;
            margin-bottom: 15px;
            line-height: 1.6;
        }}
        .tool-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .tool-stats {{
            display: flex;
            gap: 15px;
            align-items: center;
        }}
        .stat-item {{
            display: flex;
            align-items: center;
            gap: 5px;
            color: #666;
            font-size: 0.9em;
        }}
        .stat-item .icon {{
            font-size: 1.1em;
        }}
        .tool-link {{
            display: inline-block;
            padding: 8px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 500;
            transition: all 0.3s;
        }}
        .tool-link:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }}
        .tool-source {{
            position: absolute;
            top: 15px;
            right: 15px;
            background: rgba(255,255,255,0.8);
            padding: 4px 10px;
            border-radius: 10px;
            font-size: 0.75em;
            color: #999;
        }}
        .rating {{
            color: #ffc107;
            font-size: 0.9em;
        }}
        .footer {{
            text-align: center;
            padding: 30px;
            color: white;
            font-size: 0.9em;
        }}
        @media (max-width: 768px) {{
            .tools-grid {{
                grid-template-columns: 1fr;
            }}
            .header h1 {{
                font-size: 2em;
            }}
            .section {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI & Crypto Tools Directory</h1>
            <p class="subtitle">I migliori strumenti per AI e Crypto, curati e aggiornati</p>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="number">{len(ai_tools)}</div>
                <div class="label">Tool AI</div>
            </div>
            <div class="stat-box">
                <div class="number">{len(crypto_tools)}</div>
                <div class="label">Tool Crypto</div>
            </div>
            <div class="stat-box">
                <div class="number">{len(ai_tools) + len(crypto_tools)}</div>
                <div class="label">Totale</div>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title ai">🤖 Intelligenza Artificiale</h2>
            <div class="tools-grid">
                {''.join(self._generate_tool_card(tool, 'ai') for tool in ai_tools)}
            </div>
        </div>

        <div class="section">
            <h2 class="section-title crypto">🪙 Criptovalute & DeFi</h2>
            <div class="tools-grid">
                {''.join(self._generate_tool_card(tool, 'crypto') for tool in crypto_tools)}
            </div>
        </div>

        <div class="footer">
            <p>Directory aggiornata il {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            <p>Dati raccolti da Product Hunt, GitHub, CoinGecko, DeFiLlama</p>
        </div>
    </div>
</body>
</html>"""

    def _generate_tool_card(self, tool: Dict, category: str) -> str:
        """Genera card HTML per un tool"""
        name = tool.get('name', 'Nome non disponibile')
        description = tool.get('description', '')[:100]
        url = tool.get('url', '#')
        votes = tool.get('votes', 0)
        rating = tool.get('rating', 0)
        source = tool.get('source', '')

        # Formatta i numeri
        if votes >= 1000000:
            votes_str = f"{votes/1000000:.1f}M"
        elif votes >= 1000:
            votes_str = f"{votes/1000:.0f}K"
        else:
            votes_str = str(votes)

        # Genera stelle rating
        stars = '★' * min(5, int(rating)) + '☆' * max(0, 5 - int(rating))

        return f"""
        <div class="tool-card">
            <div class="tool-source">{source}</div>
            <div class="tool-name">
                {name}
                <span class="tool-badge {category}">{category.upper()}</span>
            </div>
            <p class="tool-description">{description}</p>
            <div class="tool-meta">
                <div class="tool-stats">
                    <div class="stat-item">
                        <span class="icon">⭐</span>
                        <span class="rating" title="Rating">{rating:.1f} {stars}</span>
                    </div>
                    <div class="stat-item">
                        <span class="icon">📈</span>
                        <span>{votes_str}</span>
                    </div>
                </div>
                <a href="{url}" target="_blank" class="tool-link">Visita →</a>
            </div>
        </div>
        """

    def update_from_fetcher(self, fetcher):
        """Aggiorna directory usando un fetcher"""
        tools_data = fetcher.get_all_tools()
        return self.generate_tools_page(tools_data, {})
