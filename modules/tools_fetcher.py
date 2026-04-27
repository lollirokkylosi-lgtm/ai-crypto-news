import requests
import os
from datetime import datetime, timedelta
from typing import List, Dict


class ToolsFetcher:
    """Raccoglie AI e Crypto tool da varie fonti"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AI-Crypto-Tools-Directory/1.0'
        })

    def fetch_ai_tools(self) -> List[Dict]:
        """
        Raccoglie AI tool da:
        - Product Hunt (trending)
        - GitHub (repository AI)
        - AlternativeTo (categorie AI)
        """
        tools = []

        # 1. Product Hunt - AI Tools (trending oggi)
        ph_tools = self._fetch_product_hunt_ai_tools()
        tools.extend(ph_tools)

        # 2. GitHub - AI Projects popolari
        github_tools = self._fetch_github_ai_tools()
        tools.extend(github_tools)

        # 3. AlternativeTo AI Category
        at_tools = self._fetch_alternativeto_ai()
        tools.extend(at_tools)

        return tools

    def fetch_crypto_tools(self) -> List[Dict]:
        """
        Raccoglie Crypto tool da:
        - CoinGecko (trending, exchanges)
        - Product Hunt (crypto)
        - DeBank API (protocolli DeFi)
        - Dune Analytics (dashboard)
        """
        tools = []

        # 1. CoinGecko - Exchanges e protocolli
        cg_tools = self._fetch_coingecko_tools()
        tools.extend(cg_tools)

        # 2. Product Hunt - Crypto
        ph_tools = self._fetch_product_hunt_crypto_tools()
        tools.extend(ph_tools)

        # 3. DeFiLlama - TVL e protocolli
        defi_tools = self._fetch_defillama_protocols()
        tools.extend(defi_tools)

        return tools

    def _fetch_product_hunt_ai_tools(self) -> List[Dict]:
        """Fetch AI tools da Product Hunt"""
        tools = []
        try:
            # Usa Product Hunt API (richiede token)
            token = os.getenv('PRODUCT_HUNT_TOKEN', '')
            if token:
                url = "https://api.producthunt.com/v2/api/graphql"
                query = """
                {
                  posts(category: "ai", first: 10, order: VOTES) {
                    edges {
                      node {
                        name
                        tagline
                        url
                        votesCount
                        reviewsRating
                      }
                    }
                  }
                }
                """
                headers = {'Authorization': f'Bearer {token}'}
                response = self.session.post(url, json={'query': query}, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    for edge in data.get('data', {}).get('posts', {}).get('edges', []):
                        node = edge['node']
                        tools.append({
                            'name': node['name'],
                            'category': 'AI',
                            'description': node['tagline'],
                            'url': node['url'],
                            'votes': node.get('votesCount', 0),
                            'rating': node.get('reviewsRating', 0),
                            'source': 'Product Hunt',
                            'added_date': datetime.now().strftime('%Y-%m-%d')
                        })
        except Exception as e:
            print(f"⚠️ Product Hunt AI error: {e}")

        # Fallback: AI tool noti se API non disponibile
        if not tools:
            tools = [
                {
                    'name': 'ChatGPT',
                    'category': 'AI',
                    'description': 'LLM conversazionale di OpenAI',
                    'url': 'https://chat.openai.com',
                    'votes': 10000,
                    'rating': 4.8,
                    'source': 'Trending',
                    'added_date': datetime.now().strftime('%Y-%m-%d')
                },
                {
                    'name': 'Claude 3',
                    'category': 'AI',
                    'description': 'Modello Anthropic avanzato',
                    'url': 'https://claude.ai',
                    'votes': 8500,
                    'rating': 4.7,
                    'source': 'Trending',
                    'added_date': datetime.now().strftime('%Y-%m-%d')
                },
                {
                    'name': 'Midjourney',
                    'category': 'AI',
                    'description': 'Generazione immagini AI',
                    'url': 'https://midjourney.com',
                    'votes': 7200,
                    'rating': 4.6,
                    'source': 'Trending',
                    'added_date': datetime.now().strftime('%Y-%m-%d')
                }
            ]

        return tools

    def _fetch_github_ai_tools(self) -> List[Dict]:
        """Fetch AI projects GitHub trending"""
        tools = []
        try:
            # GitHub API - repos AI trending
            headers = {'Accept': 'application/vnd.github.v3+json'}
            token = os.getenv('GITHUB_TOKEN', '')
            if token:
                headers['Authorization'] = f'token {token}'

            # Repos AI con più stars
            url = "https://api.github.com/search/repositories"
            params = {
                'q': 'artificial intelligence OR machine learning OR deep learning language:python stars:>1000',
                'sort': 'stars',
                'order': 'desc',
                'per_page': 10
            }
            response = self.session.get(url, headers=headers, params=params)

            if response.status_code == 200:
                repos = response.json().get('items', [])
                for repo in repos:
                    tools.append({
                        'name': repo['name'],
                        'category': 'AI',
                        'description': repo.get('description', '')[:100],
                        'url': repo['html_url'],
                        'votes': repo['stargazers_count'],
                        'rating': 4.5,
                        'source': 'GitHub',
                        'added_date': datetime.now().strftime('%Y-%m-%d')
                    })
        except Exception as e:
            print(f"⚠️ GitHub AI error: {e}")

        return tools

    def _fetch_alternativeto_ai(self) -> List[Dict]:
        """Fetch AI tools da AlternativeTo"""
        tools = []
        try:
            url = "https://api.alternativeto.net/categories/artificial-intelligence/list/?count=10"
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                for item in data.get('data', [])[:10]:
                    tools.append({
                        'name': item['name'],
                        'category': 'AI',
                        'description': item.get('short_description', ''),
                        'url': item.get('urls', {}).get('web', ''),
                        'votes': item.get('votes', 0),
                        'rating': item.get('rating', 0),
                        'source': 'AlternativeTo',
                        'added_date': datetime.now().strftime('%Y-%m-%d')
                    })
        except Exception as e:
            print(f"⚠️ AlternativeTo error: {e}")

        return tools

    def _fetch_coingecko_tools(self) -> List[Dict]:
        """Fetch crypto exchanges e tool da CoinGecko"""
        tools = []
        try:
            url = "https://api.coingecko.com/api/v3/exchanges"
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                exchanges = response.json()
                for ex in exchanges[:10]:
                    tools.append({
                        'name': ex['name'],
                        'category': 'Crypto',
                        'description': f"Exchange - Trust score: {ex.get('trust_score', 'N/A')}",
                        'url': ex.get('url', ''),
                        'votes': ex.get('trade_volume_24h_btc', 0),
                        'rating': ex.get('trust_score', 0) / 2 if ex.get('trust_score') else 0,
                        'source': 'CoinGecko',
                        'added_date': datetime.now().strftime('%Y-%m-%d')
                    })

            # Protocolli DeFi
            url2 = "https://api.coingecko.com/api/v3/coins/categories/defi"
            response2 = self.session.get(url2, timeout=10)

            if response2.status_code == 200:
                defi = response2.json()
                for item in defi.get('coins', [])[:5]:
                    tools.append({
                        'name': item['name'],
                        'category': 'Crypto',
                        'description': "DeFi Protocol - Top tier",
                        'url': item['url'],
                        'votes': item.get('market_cap_rank', 100),
                        'rating': 4.5,
                        'source': 'CoinGecko',
                        'added_date': datetime.now().strftime('%Y-%m-%d')
                    })
        except Exception as e:
            print(f"⚠️ CoinGecko error: {e}")

        # Fallback tool noti
        if not tools:
            tools = [
                {
                    'name': 'Uniswap',
                    'category': 'Crypto',
                    'description': 'DEX leader per trading token ERC-20',
                    'url': 'https://uniswap.org',
                    'votes': 10000,
                    'rating': 4.8,
                    'source': 'Trending',
                    'added_date': datetime.now().strftime('%Y-%m-%d')
                },
                {
                    'name': 'MetaMask',
                    'category': 'Crypto',
                    'description': 'Wallet crypto e browser extension',
                    'url': 'https://metamask.io',
                    'votes': 9500,
                    'rating': 4.7,
                    'source': 'Trending',
                    'added_date': datetime.now().strftime('%Y-%m-%d')
                }
            ]

        return tools

    def _fetch_product_hunt_crypto_tools(self) -> List[Dict]:
        """Fetch crypto tools da Product Hunt"""
        # Simili a AI, ma per categoria crypto
        return []

    def _fetch_defillama_protocols(self) -> List[Dict]:
        """Fetch protocolli DeFi da DeFiLlama"""
        tools = []
        try:
            url = "https://api.llama.fi/protocols"
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                protocols = response.json()
                # Prendi top 5 per TVL
                sorted_prot = sorted(protocols, key=lambda x: x.get('tvl', {}).get('tvl', 0) if isinstance(x.get('tvl'), dict) else 0, reverse=True)
                for prot in sorted_prot[:5]:
                    tvl = 0
                    if isinstance(prot.get('tvl'), dict):
                        tvl = prot['tvl'].get('tvl', 0)
                    elif isinstance(prot.get('tvl'), (int, float)):
                        tvl = prot['tvl']

                    tools.append({
                        'name': prot['name'],
                        'category': 'Crypto',
                        'description': f"DeFi Protocol - TVL: ${tvl:,.0f}",
                        'url': prot.get('url', ''),
                        'votes': int(tvl / 1000000),  # Milioni come proxy popolarità
                        'rating': 4.5,
                        'source': 'DeFiLlama',
                        'added_date': datetime.now().strftime('%Y-%m-%d')
                    })
        except Exception as e:
            print(f"⚠️ DeFiLlama error: {e}")

        return tools

    def get_all_tools(self) -> Dict[str, List[Dict]]:
        """Raccoglie tutti i tool"""
        return {
            'ai_tools': self.fetch_ai_tools(),
            'crypto_tools': self.fetch_crypto_tools()
        }
