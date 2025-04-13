# 🗞️ ETF News Bot

A Python Telegram bot that fetches daily, relevant news about your ETF portfolio from the web and sends it directly to your Telegram chat.

## 🚀 Features

- 📰 **Daily News Delivery**: Retrieves top news related to your selected ETFs.
- 🤖 **Telegram Integration**: Sends messages using Telegram Bot API.
- 🔍 **Keyword Matching**: Uses tailored queries per ETF to find the most relevant headlines.
- 🧠 **Duplicate Filtering**: Keeps track of already-sent articles to avoid repetition.
- 🔒 **Environment Variables**: API keys are handled securely.

---

## 🧰 ETFs Tracked

The bot currently tracks news related to the following ETFs:

| Ticker | Focus Area |
|--------|------------|
| `VTI`  | US Stock Market |
| `VWO`  | Emerging Markets |
| `TIP`  | TIPS & Inflation |
| `GLD`  | Gold & Precious Metals |
| `VNQ`  | Real Estate (REITs) |
| `VGIT` | Treasury Bonds & Interest Rates |

---

## 📦 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/etf-news-bot.git
cd etf-news-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** Make sure to have Python 3.7+ installed.

### 3. Set Environment Variables

Create a `.env` file or export variables directly in your terminal/session:

```bash
export TELEGRAM_BOT_API_KEY="your_telegram_bot_api_key"
export NEWS_API_KEY="your_newsapi_key"
export CHAT_ID='your_telegram_chat_id"
```

### 4. Run the Bot

```bash
python3 etf_news_bot.py
```

---

## 💬 Telegram Commands

- `/start` - Displays a welcome message and usage instructions.
- `/getNews` - Fetches the latest news articles and sends them to your Telegram.

---

## 🗂️ File Structure

- `etf_news_bot.py` - Main bot logic.
- `seen_articles.txt` - Tracks already-sent article URLs.

---

## 🙌 Acknowledgments

- [NewsAPI.org](https://newsapi.org/) for providing the news articles.
- [python-telegram-bot](https://github.com/eternnoir/pyTelegramBotAPI) for Telegram integration.
