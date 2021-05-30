# #NoQueueLife-Bot
You can test bot on [@nql1bot](http://t.me/nql1bot)
### Requirements

```bash
pip install -r requirements.txt
```

In the environment variables, you need to put the bot's API token:

`TELEGRAM_API_TOKEN` — API bot token

```python
# run.py
# simple usage
from nql_bot.bot import Bot

bot = Bot()
bot.run()
```
```bash
python run.py
```
