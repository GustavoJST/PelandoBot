<img src="./assets/logo.png" width="100%"/>

<div align="center">

[![Tests](https://github.com/GustavoJST/PelandoBot/actions/workflows/tests.yaml/badge.svg)](https://github.com/GustavoJST/PelandoBot/actions/workflows/tests.yaml)

<h3 align="center">Pelando Bot</h3>

A simple Telegram bot that delivers notifications on discounts, promo codes, etc, that appears in the [Pelando website](https://www.pelando.com.br).

Click [here](https://t.me/pelandopromobot) or search **@pelandopromobot** on Telegram to use this bot.
  
**Pelando Bot is in active development.**

Made using [PyTelegramBotApi](https://github.com/eternnoir/pyTelegramBotAPI).

<a href="https://github.com/GustavoJST/CLID/labels/bug">Report Bug</a>
<br><br>
</div>

# About the project
Pelando bot is a simple Telegram bot that delivers notifications on discounts, promo codes, etc.

This bot uses a similar tags system used in the Pelando website, in which the tags filters new discounts based on the discount's post title.

**Example:** if you set your tags to "amd" and "intel", you'll only receive notification on discounts that have one (or both) of these words in the discount's post title.

## Limitations

Unfortunately, due to scalability issues derived from limiting requests to Telegram's servers, the maximum number of simultaneous chats that the bot supports is 1000. If this number were higher, there would be a noticeable delay between fetching the information from the website and sending it to you as a Telegram message. 

To compensate for that, it's advised to use this bot in groups/supergroups, although it can be used in private chats. **The bot will only respond to commands from admins.**

Also, keep in mind that the bot **will not work (read commands) on channels or if you're an anonnymous admin in a group**.

## Disclaimer
This project and it's creator are not affiliated with the Pelando website/company. This is just an open source project that aims to help people get better notifications on discounts that appear on the Pelando website.
