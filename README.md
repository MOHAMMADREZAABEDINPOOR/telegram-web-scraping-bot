# 🏠 Telegram Web Scraping Bot

A Telegram bot for searching and browsing real estate listings from Divar.ir. This bot provides an interactive interface for users to search properties across Iranian cities with real-time web scraping.

## 🌟 Features

- **Real-time Web Scraping**: Fetches fresh property listings directly from Divar.ir
- **Multiple Property Types**: Supports residential, commercial, sale, and rental properties
- **City Search**: Search across 20+ major Iranian cities
- **Detailed Information**: Shows property images, prices, location, specifications, and amenities
- **Interactive Interface**: User-friendly inline keyboard menus
- **Pagination Support**: Browse through multiple listings efficiently

## 🛠️ Technologies Used

- **Python 3.x**
- **pyTelegramBotAPI (telebot)**: Telegram Bot API wrapper
- **Scrapling**: Web scraping library
- **Agno**: AI agent framework with Google Gemini integration
- **Logging**: Comprehensive error tracking and monitoring

## 📋 Prerequisites

- Python 3.7 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Google Gemini API Key (optional, for AI features)

## ⚙️ Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/telegram-web-scraping-bot.git
cd telegram-web-scraping-bot
```

2. Install required packages:
```bash
pip install pyTelegramBotAPI scrapling agno
```

3. Update the bot configuration in the main file:
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"  # Optional
```

4. (Optional) Update Gemini API key if using AI features:
```python
api_key = "YOUR_GEMINI_API_KEY"
```

## 🚀 Usage

Run the bot:
```bash
python agent.py
```

Or use the alternative version:
```bash
python telegram_bot_proper.py
```

## 🎯 Bot Commands

- `/start` or `/help`: Show welcome message and main menu

## 📱 Supported Property Types

### Residential
- Apartments (Sale/Rent)
- Villas (Sale/Rent)
- Land and Old Houses (Sale)

### Commercial
- Offices (Sale/Rent)
- Stores (Sale/Rent)
- Industrial Properties (Sale/Rent)

## 🏙️ Supported Cities

تهران، اصفهان، مشهد، شیراز، تبریز، کرج، اهواز، قم، رشت، کرمان، همدان، یزد، اردبیل، بندرعباس، کرمانشاه، زاهدان، ساری، قزوین، خرم‌آباد، گرگان

## 📸 Features

- **Image Support**: Shows up to 3 property images per listing
- **Price Details**: Displays both main price and detailed pricing
- **Location Info**: Shows neighborhood and city information
- **Property Specs**: Includes square footage, room count, construction year
- **Amenities**: Lists available facilities and features

## 🔧 Project Structure

```
.
├── agent.py                    # Main bot file (with detailed scraping)
├── telegram_bot_proper.py      # Alternative bot version
├── telegram_bot.py             # Legacy version
├── .gitignore
└── README.md
```

## ⚠️ Important Notes

- **API Keys**: Make sure to replace placeholder API keys with your own
- **Rate Limiting**: Be mindful of Divar.ir's rate limits when scraping
- **Legal Compliance**: Ensure web scraping complies with website's terms of service

## 👨‍💻 Developer

Developed by **Mohammadreza Abedinpour** for PIMX

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📞 Support

For support and questions, please open an issue in the GitHub repository.

---

**Note**: This bot is for educational and research purposes. Please respect the website's robots.txt and terms of service when using web scraping functionality.

