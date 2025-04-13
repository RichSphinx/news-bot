#!/usr/bin/env python3
"""
ETF News Bot

This script fetches daily financial news for selected ETFs and sends it to a Telegram chat.
It uses NewsAPI to gather news articles and Telebot (pyTelegramBotAPI) for Telegram integration.
"""

import os
import re
import time
from datetime import datetime
import requests
import telebot

news_cache = {}
SEEN_FILE = "seen_articles.txt"

def load_seen_articles():
    """
    Load previously seen article URLs from a local file.

    Returns:
        set: A set of URLs that have already been sent.
    """
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_seen_articles(seen_set):
    """
    Save the set of seen article URLs to a local file.

    Args:
        seen_set (set): The set of URLs to write to the file.
    """
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        for url in seen_set:
            f.write(url + "\n")

seen_articles = load_seen_articles()

# Define keyword queries associated with each ETF
keywords = {
    'VTI':  'US stock market OR SP500 OR US economy OR Federal Reserve',
    'VWO':  'emerging markets OR China economy OR India economy OR developing countries',
    'TIP':  'inflation OR CPI OR TIPS bonds OR US Treasury',
    'GLD':  'gold prices OR precious metals OR gold ETF',
    'VNQ':  'real estate market OR REITs OR commercial real estate OR housing market',
    'VGIT': 'interest rates OR treasury yields OR Federal Reserve OR bond market'
}

TelegramAPIToken = os.getenv('TELEGRAM_BOT_API_KEY')
bot = telebot.TeleBot(TelegramAPIToken)
CHAT_ID = os.getenv('CHAT_ID')

def escape_markdown_v2(text):
    """
    Escape Telegram MarkdownV2 reserved characters for safe message formatting.

    Args:
        text (str): The text to escape.

    Returns:
        str: Escaped MarkdownV2-safe text.
    """
    if not text:
        return ''
    escape_chars = r'_*\[\]()~`>#+\-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

def strip_html_tags(text):
    """
    Remove basic HTML tags from a string.

    Args:
        text (str): The text that may contain HTML tags.

    Returns:
        str: Cleaned text without HTML.
    """
    return re.sub('<[^<]+?>', '', text or '')

def escape_url(url):
    """
    Escape problematic characters in a URL (e.g., parentheses).

    Args:
        url (str): The URL to escape.

    Returns:
        str: A URL safe for MarkdownV2 formatting.
    """
    return url.replace(")", "%29")

def get_news(news_query):
    """
    Fetch news articles from NewsAPI for a given query.
    Uses a local cache to avoid repeated API calls for the same keyword.

    Args:
        news_query (str): The query string to search for.

    Returns:
        list: A list of news articles (dicts).
    """
    if news_query in news_cache:
        return news_cache[news_query]

    news_api = 'https://newsapi.org/v2/everything'
    news_api_key = os.getenv('NEWS_API_KEY')
    params = {
        'q': news_query,
        'from': datetime.now().strftime('%d-%m-%Y'),
        'sortBy': 'relevancy',
        'language': 'en',
        'apiKey': news_api_key,
        'pageSize': 2
    }

    response = requests.get(news_api, params=params, timeout=5)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        news_cache[news_query] = articles
        time.sleep(1)  # Sleep to respect API rate limits
        return articles

    print(f"Error {response.status_code} for query {news_query}")
    return []

@bot.message_handler(commands=['start'])
def send_welcome(_):
    """
    Handle the /start command by sending a welcome message to the user.
    """
    bot.send_message(
        CHAT_ID,
        "To interact with this bot use command: */getNews*",
        parse_mode="MarkdownV2",
        disable_web_page_preview=True
    )

@bot.message_handler(commands=['getNews'])
def send_news(_):
    """
    Handle the /getNews command by fetching and sending ETF news to Telegram.
    """
    date_str = escape_markdown_v2(datetime.now().strftime('%d-%m-%Y'))
    bot.send_message(
        CHAT_ID,
        f"*TODAY'S NEWS: {date_str}*",
        parse_mode="MarkdownV2"
    )

    for etf, query in keywords.items():
        etf_message = f"*{escape_markdown_v2(etf)}*\n"
        seen_for_etf = set()
        has_articles = False

        articles = get_news(query)
        for a in articles:
            title = escape_markdown_v2(a.get('title', ''))
            desc = escape_markdown_v2(strip_html_tags(a.get('description', '')))
            url = a.get('url', '')

            if url in seen_articles or url in seen_for_etf:
                continue

            seen_for_etf.add(url)
            seen_articles.add(url)
            has_articles = True

            etf_message += f"\n• *{title}*\n  {desc}\n  [Read more]({escape_url(url)})\n"

        if has_articles:
            # Telegram limits messages to 4096 characters
            while len(etf_message) > 4000:
                split_at = etf_message.rfind('\n', 0, 4000)
                part = etf_message[:split_at]
                bot.send_message(
                    CHAT_ID,
                    part.strip(),
                    parse_mode="MarkdownV2",
                    disable_web_page_preview=True
                )
                etf_message = etf_message[split_at:]

            if etf_message.strip():
                bot.send_message(
                    CHAT_ID,
                    etf_message.strip(),
                    parse_mode="MarkdownV2",
                    disable_web_page_preview=True
                )

    save_seen_articles(seen_articles)

bot.infinity_polling()
