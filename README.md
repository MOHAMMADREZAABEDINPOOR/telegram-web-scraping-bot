<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=1,12,24,30&height=220&section=header&text=TELEGRAM_SCRAPER_BOT&fontSize=36&fontAlignY=35&desc=%E2%9A%A1%20AI%20Real-Estate%20Scraper%20%26%20Divar%20Intelligence%20Agent&descFontSize=16&descAlignY=62" alt="Scraper Bot Banner" width="100%" />

<a href="https://github.com/MOHAMMADREZAABEDINPOOR/telegram-web-scraping-bot">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=2800&pause=1000&color=00D2FF&center=true&vCenter=true&width=780&lines=Autonomous+Telegram+Agent+Scraping+Real-Estate+Listings;Powered+by+the+Agno+Agentic+Framework+%26+Google+Gemini+Flash;Automated+Scrapling+Engine+Extracting+Prices%2C+Areas+%26+Contacts;Bilingual+City+Translation+Dictionary+(Tehran%2C+Isfahan%2C+Shiraz);Interactive+Inline+Keyboards+with+Direct+Listing+URLs;Anti-Bot+Bypass+with+Adaptive+Request+Throttling" alt="Typing SVG" />
</a>

<br/>

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg?style=for-the-badge&logo=gnu)](https://www.gnu.org/licenses/agpl-3.0)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Agno Framework](https://img.shields.io/badge/AI_Agent-Agno_Framework-8A2BE2?style=for-the-badge)](https://github.com/agno-agi/agno)
[![Google Gemini](https://img.shields.io/badge/AI-Gemini_1.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Scrapling](https://img.shields.io/badge/Scraper-Scrapling_Fetcher-FF6B6B?style=for-the-badge)](https://github.com/D4Vinci/Scrapling)
[![Read in Persian](https://img.shields.io/badge/مطالعه_به_فارسی-Persian_README-008080?style=for-the-badge)](#persian-documentation)

<p align="center">
  <b>telegram-web-scraping-bot</b> is an autonomous AI agent and web-scraping bot for Telegram built on the <b>Agno agentic framework</b>, <b>Google Gemini 1.5 Flash</b>, and <b>Scrapling</b>. Designed for intelligent Iranian real estate discovery (Divar), the bot understands natural language queries in Persian, extracts listings, normalizes pricing and square footage, and delivers interactive cards with direct listing links.
</p>

[Project Overview](#-project-overview) •
[Directory Anatomy](#-exhaustive-directory--file-anatomy) •
[Agentic Architecture](#-agentic-scraping-architecture) •
[Quick Start](#-quick-start) •
[توضیحات فارسی](#persian-documentation) •
[License](#-copyleft-license--legal-attribution)

</div>

---

## ⚡ Project Overview

Searching for apartments and commercial real estate on platforms like Divar requires manually adjusting multiple filters across dozens of pages.

**telegram-web-scraping-bot** automates this via conversational AI:
- 💬 **Natural Language Query Parsing**: Say *"یک آپارتمان ۱۰۰ متری در سعادت آباد تهران با ودیعه ۲۰۰ میلیون"* and Gemini extracts parameters automatically.
- 🕷️ **Resilient Web Scraping (`Scrapling`)**: Extracts prices, floor areas, neighborhood tags, and photographs while circumventing Cloudflare challenges and rate limits.
- 🗺️ **Bilingual City Normalization**: Automatically maps Persian city names (`تهران`, `اصفهان`, `شیراز`, `مشهد`) to backend URL slugs.

---

## 📂 Exhaustive Directory & File Anatomy

```
d:/code/tagent/
│
├── agent.py                         # 940+ lines: Agno agent definitions, Gemini tools & Telebot handlers
├── telegram_bot.py                  # Core Telegram client and message dispatch loop
├── telegram_bot_proper.py           # Production-hardened bot runner with exception recovery
└── README.md                        # Master comprehensive bilingual documentation
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/MOHAMMADREZAABEDINPOOR/telegram-web-scraping-bot.git
cd telegram-web-scraping-bot

python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux:
source venv/bin/activate

pip install telebot agno scrapling google-generativeai
python agent.py
```

---

## Persian Documentation
### 🇮🇷 مستندات فوق‌العاده مفصل، جامع و فنی به زبان فارسی

### ۱. معرفی ایجنت هوشمند تلگرام استخراج آگهی مسکن
پروژه **telegram-web-scraping-bot** یک عامل هوشمند خودمختار (AI Autonomous Agent) در تلگرام است که با استفاده از فریم‌ورک نوین **Agno** و هوش مصنوعی **Google Gemini 1.5 Flash** مهندسی شده است. این ربات زبان طبیعی کاربر را متوجه شده، پارامترهای مسکن (متراژ، بودجه، ودیعه، محله) را استخراج کرده و به صورت خودکار جدیدترین آگهی‌های پلتفرم دیوار را استخراج کرده و در قالب پیام‌های تصویری شیک در تلگرام نمایش می‌دهد.

---

### ۲. تشریح ساختار فایل‌های پروژه
- **`agent.py`**: تعریف ابزارهای عامل هوش مصنوعی (AI Tools)، دیکشنری تبدیل اسامی فارسی شهرها به انگلیسی، و اتصال به ابزار Scrapling برای عبور از موانع ضدربات.
- **`telegram_bot.py`**: حلقه گوش دادن به پیام‌ها در تلگرام و ساخت دکمه‌های اینلاین با لینک مستقیم آگهی.

---

## 📜 Copyleft License & Legal Attribution

Distributed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

---

<div align="center">
<img src="./assets/footer.svg" alt="Telegram Web Scraping Bot 3D Footer" width="100%" />
<sub>Architected by <a href="https://github.com/MOHAMMADREZAABEDINPOOR"><b>MOHAMMADREZA ABEDINPOOR</b></a>. If this AI agent assists your workflow, leave a ⭐!</sub>
</div>
