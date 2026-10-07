<div align="center">

<img src="assets/readme/hero.gif" width="1200" alt="PROPERTY DISCOVERY BOT — rotating 3D geometry" />

**[English](README.md) · [فارسی](README.fa.md)**

<img src="assets/readme/identity.svg" width="1200" alt="ai / English and Persian documentation" />

</div>

# PROPERTY DISCOVERY BOT

A collection of Telegram and agent scripts for property-listing discovery, with Agno/Gemini integration and Scrapling extraction helpers.

[GitHub](https://github.com/MOHAMMADREZAABEDINPOOR/telegram-web-scraping-bot) · [PIMX / Profile](https://github.com/MOHAMMADREZAABEDINPOOR) · [Static artwork](assets/readme/hero.png)

## Features

- Property-listing queries and extraction helpers
- Telegram interfaces in separate script variants
- AI agent integration and structured result formatting
- City/query handling for listing searches

## Stack

| Tool | Version / source |
|---|---|
| Python | `standard library / source imports` |

## Getting started

Python 3; a desktop/Tk installation for Tkinter or turtle examples. Tkinter is provided by the Python installation, not pip. Legacy dependencies may need a compatible Python version.

```bash
git clone https://github.com/MOHAMMADREZAABEDINPOOR/telegram-web-scraping-bot.git
cd telegram-web-scraping-bot

python -m pip install agno google-genai scrapling "python-telegram-bot>=20,<23" requests
python telegram_bot_proper.py
```

## Configuration

No standard environment template is defined. Standalone exercises need no external configuration; inspect any service constants or paths in the source before running.

## Usage

Choose one script variant, review its provider/bot configuration and install its imports. Use a development bot to try a property query before scheduling repeated requests.

## Project structure

| Path | Role |
|---|---|
| [`assets/`](assets/) | Brand/media/README assets |
| [`agent.py`](agent.py) | Project entry/configuration file |
| [`telegram_bot.py`](telegram_bot.py) | Project entry/configuration file |
| [`telegram_bot_proper.py`](telegram_bot_proper.py) | Project entry/configuration file |

## Commands and checks

No automated test command is declared in a manifest. Verify behavior through a local example run.

## Deployment

Host a long-running bot process with environment secrets and private storage. Run a single polling instance. Check network access and dependency compatibility on the host.

## Limitations

No pinned requirements manifest is included. Website markup, access policy and provider APIs can change. Review configuration and avoid deploying development credentials.

## Troubleshooting

- Authentication/provider errors: verify credentials and selected model/provider.
- No Telegram updates: check polling/webhook mode and concurrent bot instances.
- Missing dependencies: use the declared manifest or inspect imports if no manifest is provided.

## Contributing

Create a focused branch, verify the affected behavior and explain the change clearly. Keep private data, build outputs and local databases out of commits.

## License

No repository-level license file is included in this snapshot. Public visibility alone does not grant reuse rights; contact the repository owner for terms.

---

Part of **PIMX** · Documentation in English and Persian.
