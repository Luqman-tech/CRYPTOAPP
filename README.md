# CryptoBuddy - Cryptocurrency Analysis Tool

CryptoBuddy is a Python-based cryptocurrency analysis tool that provides real-time market data and investment recommendations based on sustainability, profitability, and long-term growth potential. It uses the CoinGecko API to fetch current market data and combines it with sustainability metrics to help users make informed investment decisions.

## Features

- **Real-time Market Data**: Get current prices, 24-hour changes, market caps, and trading volumes
- **Sustainability Focus**: Each cryptocurrency is rated on its energy usage and sustainability
- **Multiple Analysis Types**:
  - Sustainable cryptocurrency recommendations
  - Profitable investment opportunities (>5% growth)
  - Long-term investment suggestions based on sustainability and market presence
  - Comprehensive coin information including price trends and market metrics

## Supported Cryptocurrencies

- Bitcoin (BTC)
- Ethereum (ETH)
- Cardano (ADA)
- Solana (SOL)
- Polkadot (DOT)
- Chainlink (LINK)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CryptoApplication.git
cd CryptoApplication
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from app import CryptoBuddy

# Initialize CryptoBuddy
buddy = CryptoBuddy()

# Get information about a specific cryptocurrency
bitcoin_info = buddy.get_coin_info("bitcoin")
print(bitcoin_info)

# Get sustainable cryptocurrency recommendations
sustainable = buddy.get_sustainable_recommendation()
print(sustainable)

# Get profitable recommendations
profitable = buddy.get_profitable_recommendation()
print(profitable)

# Show all available cryptocurrencies
all_coins = buddy.show_all_coins()
print(all_coins)
```

### Example Output

```python
# Bitcoin Information
{
    'name': 'Bitcoin',
    'symbol': 'BTC',
    'current_price': '$104,724.00',
    'price_change_24h': '0.14%',
    'market_cap': '$2,080,921,405,315',
    'volume_24h': '$22,215,497,641',
    'high_24h': '$104,849.00',
    'low_24h': '$103,296.00',
    'last_updated': '2025-05-31 20:45:20 UTC',
    'energy_use': 'High',
    'sustainability_score': 3,
    'description': 'The original cryptocurrency and digital gold'
}
```

## Features in Detail

### 1. Get Coin Information
```python
buddy.get_coin_info("bitcoin")  # Get info by name
buddy.get_coin_info("ETH")      # Get info by symbol
```

### 2. Sustainable Recommendations
```python
buddy.get_sustainable_recommendation()  # Returns the most eco-friendly crypto
```

### 3. Profitable Recommendations
```python
buddy.get_profitable_recommendation()  # Returns coins with >5% growth
```

### 4. Long-term Recommendations
```python
buddy.get_longterm_recommendation()  # Returns sustainable coins with strong market presence
```

## Sustainability Scoring

Cryptocurrencies are scored on a scale of 1-10 based on:
- Energy consumption
- Network efficiency
- Consensus mechanism
- Environmental impact

## Dependencies

- Python 3.6+
- pycoingecko
- requests

## API Usage

This application uses the CoinGecko API for real-time market data. No API key is required for basic usage, but there are rate limits.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

⚠️ Cryptocurrency investments are highly risky. This tool is for educational purposes only. Always do your own research before investing. The recommendations provided are based on predefined criteria and should not be considered as financial advice.

## Author

[Your Name]
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## Acknowledgments

- CoinGecko API for providing real-time cryptocurrency data
- The cryptocurrency community for sustainability metrics and insights 