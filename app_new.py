from flask import Flask, render_template, request, jsonify
import time
import random
from pycoingecko import CoinGeckoAPI
from datetime import datetime

app = Flask(__name__)
cg = CoinGeckoAPI()

class CryptoBuddy:
    def __init__(self):
        self.bot_name = "CryptoBuddy"
        self.coingecko = CoinGeckoAPI()
        self.crypto_db = {
            "bitcoin": {
                "price_trend": "rising",
                "market_cap": "high", 
                "energy_use": "high",
                "sustainability_score": 3,
                "symbol": "BTC",
                "description": "The original cryptocurrency and digital gold",
                "coingecko_id": "bitcoin"
            },
            "ethereum": {
                "price_trend": "stable",
                "market_cap": "high",
                "energy_use": "medium", 
                "sustainability_score": 6,
                "symbol": "ETH",
                "description": "Smart contract platform and DeFi backbone",
                "coingecko_id": "ethereum"
            },
            "cardano": {
                "price_trend": "rising",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 8,
                "symbol": "ADA", 
                "description": "Proof-of-stake blockchain focused on sustainability",
                "coingecko_id": "cardano"
            },
            "solana": {
                "price_trend": "rising",
                "market_cap": "high",
                "energy_use": "low",
                "sustainability_score": 7,
                "symbol": "SOL",
                "description": "High-performance blockchain for DeFi and NFTs",
                "coingecko_id": "solana"
            },
            "polkadot": {
                "price_trend": "stable", 
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 8,
                "symbol": "DOT",
                "description": "Multi-chain protocol enabling blockchain interoperability",
                "coingecko_id": "polkadot"
            },
            "chainlink": {
                "price_trend": "rising",
                "market_cap": "medium",
                "energy_use": "medium",
                "sustainability_score": 5,
                "symbol": "LINK",
                "description": "Decentralized oracle network connecting blockchains to real world",
                "coingecko_id": "chainlink"
            }
        }

    def get_real_time_data(self, coin_id):
        """Get real-time price and market data from CoinGecko"""
        try:
            # Get current price and 24h data
            coin_data = self.coingecko.get_coin_by_id(
                coin_id,
                localization=False,
                tickers=False,
                market_data=True,
                community_data=False,
                developer_data=False,
                sparkline=False
            )
            
            # Extract relevant data
            market_data = coin_data['market_data']
            return {
                'current_price': market_data['current_price']['usd'],
                'price_change_24h': market_data['price_change_percentage_24h'],
                'market_cap': market_data['market_cap']['usd'],
                'total_volume': market_data['total_volume']['usd'],
                'high_24h': market_data['high_24h']['usd'],
                'low_24h': market_data['low_24h']['usd'],
                'last_updated': market_data['last_updated'],
                'success': True
            }
        except Exception as e:
            print(f"Error fetching data from CoinGecko: {str(e)}")
            return {'success': False}

    def get_coin_info(self, coin_name):
        """Get information about a specific cryptocurrency"""
        target_coin = None
        for coin, data in self.crypto_db.items():
            if (coin.lower() == coin_name.lower() or 
                data['symbol'].lower() == coin_name.lower()):
                target_coin = coin
                break
        
        if target_coin:
            data = self.crypto_db[target_coin]
            # Get real-time data
            real_time_data = self.get_real_time_data(data['coingecko_id'])
            
            if real_time_data['success']:
                trend_emoji = '📈' if real_time_data['price_change_24h'] > 0 else '📉'
                price_formatted = "${:,.2f}".format(real_time_data['current_price'])
                market_cap_formatted = "${:,.0f}".format(real_time_data['market_cap'])
                
                return {
                    'type': 'coin_info',
                    'message': f"📊 <strong>{target_coin.title()} ({data['symbol']})</strong> Information:",
                    'coin_data': {
                        'name': target_coin.title(),
                        'symbol': data['symbol'],
                        'trend_emoji': trend_emoji,
                        'current_price': price_formatted,
                        'price_change_24h': f"{real_time_data['price_change_24h']:.2f}%",
                        'market_cap': market_cap_formatted,
                        'volume_24h': "${:,.0f}".format(real_time_data['total_volume']),
                        'high_24h': "${:,.2f}".format(real_time_data['high_24h']),
                        'low_24h': "${:,.2f}".format(real_time_data['low_24h']),
                        'last_updated': datetime.fromisoformat(real_time_data['last_updated'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S UTC'),
                        'energy_use': data['energy_use'].capitalize(),
                        'sustainability_score': data['sustainability_score'],
                        'description': data['description']
                    }
                }
            else:
                # Fallback to static data if real-time data fetch fails
                trend_emoji = '📈' if data['price_trend'] == 'rising' else '📊'
                return {
                    'type': 'coin_info',
                    'message': f"📊 <strong>{target_coin.title()} ({data['symbol']})</strong> Information (Static Data):",
                    'coin_data': {
                        'name': target_coin.title(),
                        'symbol': data['symbol'],
                        'trend_emoji': trend_emoji,
                        'price_trend': data['price_trend'].capitalize(),
                        'market_cap': data['market_cap'].capitalize(),
                        'energy_use': data['energy_use'].capitalize(),
                        'sustainability_score': data['sustainability_score'],
                        'description': data['description']
                    }
                }
        else:
            available = ', '.join([f"{coin.title()} ({data['symbol']})" 
                                 for coin, data in self.crypto_db.items()])
            return {
                'type': 'error',
                'message': f"❌ Sorry, I don't have information about '{coin_name}'.<br>Available coins: {available}"
            }

    def get_sustainable_recommendation(self):
        """Get the most sustainable cryptocurrency recommendation"""
        best_coin = max(self.crypto_db.keys(), 
                       key=lambda x: self.crypto_db[x]['sustainability_score'])
        data = self.crypto_db[best_coin]
        real_time_data = self.get_real_time_data(data['coingecko_id'])
        
        coin_data = {
            'name': best_coin,
            'symbol': data['symbol'],
            'sustainability_score': data['sustainability_score'],
            'energy_use': data['energy_use'],
            'description': data['description']
        }
        
        if real_time_data['success']:
            coin_data.update({
                'current_price': "${:,.2f}".format(real_time_data['current_price']),
                'price_change_24h': f"{real_time_data['price_change_24h']:.2f}%",
                'market_cap': "${:,.0f}".format(real_time_data['market_cap'])
            })
        
        return {
            'type': 'sustainable',
            'message': f"🌱 For sustainable investing, I recommend <strong>{best_coin} ({data['symbol']})</strong>!",
            'coin_data': coin_data
        }

    def get_profitable_recommendation(self):
        """Get profitable cryptocurrency recommendations"""
        profitable_coins = []
        
        for coin, data in self.crypto_db.items():
            real_time_data = self.get_real_time_data(data['coingecko_id'])
            if real_time_data['success'] and real_time_data['price_change_24h'] > 5:  # 5% growth
                profitable_coins.append({
                    'name': coin,
                    'symbol': data['symbol'],
                    'description': data['description'],
                    'price_change_24h': f"{real_time_data['price_change_24h']:.2f}%",
                    'current_price': "${:,.2f}".format(real_time_data['current_price'])
                })
        
        if profitable_coins:
            return {
                'type': 'profitable',
                'message': "🚀 Top profitable cryptos with strong growth:",
                'coins': profitable_coins
            }
        else:
            return {
                'type': 'none',
                'message': "🤔 No cryptocurrencies showing significant growth at the moment."
            }

    def get_longterm_recommendation(self):
        """Get long-term growth recommendations"""
        longterm_coins = []
        
        for coin, data in self.crypto_db.items():
            if data['sustainability_score'] > 7:
                real_time_data = self.get_real_time_data(data['coingecko_id'])
                if real_time_data['success']:
                    longterm_coins.append({
                        'name': coin,
                        'symbol': data['symbol'],
                        'sustainability_score': data['sustainability_score'],
                        'description': data['description'],
                        'current_price': "${:,.2f}".format(real_time_data['current_price']),
                        'market_cap': "${:,.0f}".format(real_time_data['market_cap'])
                    })
        
        if longterm_coins:
            return {
                'type': 'longterm',
                'message': "🌿📈 Great long-term opportunities (sustainable + strong market presence):",
                'coins': longterm_coins
            }
        else:
            return {
                'type': 'none',
                'message': "📊 Currently no coins meet our long-term investment criteria."
            }

    def show_all_coins(self):
        """Show all available cryptocurrencies"""
        coins_data = []
        for coin, data in self.crypto_db.items():
            real_time_data = self.get_real_time_data(data['coingecko_id'])
            coin_info = {
                'name': coin,
                'symbol': data['symbol'],
                'sustainability_score': data['sustainability_score']
            }
            
            if real_time_data['success']:
                trend_emoji = '📈' if real_time_data['price_change_24h'] > 0 else '📉'
                coin_info.update({
                    'trend_emoji': trend_emoji,
                    'current_price': "${:,.2f}".format(real_time_data['current_price']),
                    'price_change_24h': f"{real_time_data['price_change_24h']:.2f}%"
                })
            else:
                coin_info['trend_emoji'] = '📊'
            
            coins_data.append(coin_info)
        
        return {
            'type': 'all_coins',
            'message': "📋 <strong>All Available Cryptocurrencies:</strong>",
            'coins': coins_data
        }

    def show_help(self):
        """Show help information"""
        return {
            'type': 'help',
            'message': """🔍 <strong>Available Commands & Examples:</strong><br><br>
            <strong>Investment Advice:</strong><br>
            • "sustainable" or "eco-friendly" → Get eco-conscious recommendations<br>
            • "profitable" or "trending" → Find coins with rising trends<br>
            • "long-term" or "growth" → Best for long-term investment<br><br>
            <strong>Information:</strong><br>
            • "bitcoin info" or "btc" → Get real-time details about specific coins<br>
            • "all coins" → See all available cryptocurrencies with live prices<br>
            • "compare bitcoin ethereum" → Compare multiple coins<br><br>
            Try the quick action buttons below for easy access!"""
        }

    def process_query(self, user_input):
        """Process user query and return appropriate response"""
        query = user_input.lower().strip()
        
        if query in ['help', '?']:
            return self.show_help()
        
        if query in ['all coins', 'list', 'show all']:
            return self.show_all_coins()
        
        sustainable_keywords = ['sustainable', 'eco', 'green', 'environment', 'energy efficient']
        if any(word in query for word in sustainable_keywords):
            return self.get_sustainable_recommendation()
        
        profitable_keywords = ['profitable', 'trending', 'rising', 'hot', 'bull', 'pump']
        if any(word in query for word in profitable_keywords):
            return self.get_profitable_recommendation()
        
        longterm_keywords = ['long-term', 'long term', 'growth', 'future', 'hold', 'hodl']
        if any(word in query for word in longterm_keywords):
            return self.get_longterm_recommendation()
        
        if 'info' in query:
            words = query.replace('info', '').strip().split()
            if words and words[0]:
                return self.get_coin_info(words[0])
        
        # Check for individual coin queries
        for coin, data in self.crypto_db.items():
            if coin.lower() in query or data['symbol'].lower() in query:
                return self.get_coin_info(coin)
        
        return {
            'type': 'default',
            'message': """🤔 I didn't quite understand that. Try asking about:<br>
            • 'sustainable coins' for eco-friendly options<br>
            • 'profitable coins' for trending investments<br>
            • 'bitcoin info' for real-time coin details<br>
            • 'help' for more commands<br><br>
            Or use the quick action buttons below!"""
        }

# Initialize the bot
bot = CryptoBuddy()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    user_message = request.json.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Process the query
    response = bot.process_query(user_message)
    
    return jsonify(response)

if __name__ == '__main__':
    print("🚀 Starting CryptoBuddy Python Application with CoinGecko Integration...")
    print("🌐 Access the application at: http://localhost:5000")
    print("⚠️  Remember: This is for educational purposes only!")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 