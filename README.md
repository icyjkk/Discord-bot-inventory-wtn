# Discord-bot-inventory-wtn

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-v1.7.3-blue.svg)](https://discordpy.readthedocs.io/)

## Description

`Discord-bot-inventory-wtn` is a Discord bot that helps manage an inventory of sneakers. The bot allows users to add and remove sneakers, search for models by name or SKU, and get notified when specific sizes or models become available. This bot is specifically designed for sneaker enthusiasts who want to keep track of their collections and be notified of updates.

The bot was integrated with a monitor for WTN (WeTheNew), a popular sneaker marketplace. WTN frequently posted buy requests for specific sneakers that they wanted to purchase. Users could list their sneakers in the bot’s inventory, including the sizes they had for sale. Whenever WTN posted a buy request that matched a sneaker and size from a user's inventory, the bot would instantly notify the user, allowing them to quickly respond to the opportunity and sell their sneakers to WTN. This functionality helped users capitalize on potential sales and react swiftly to buy requests, ensuring they didn't miss any selling opportunities.

## Features

- Add and remove sneakers from your personal inventory.
- Search and add sneakers by name or SKU.
- View your inventory in an easy-to-read format.
- Notifications for sneaker availability based on user subscriptions.
- Role-based command restrictions.

## Commands

The following commands are supported by the bot:

| Command               | Description                                                                          |
|-----------------------|--------------------------------------------------------------------------------------|
| `!ping`               | Responds with "PONG".                                                                |
| `!addName "name" size`| Adds a sneaker by name and size to the user's inventory.                             |
| `!addSKU sku size`    | Adds a sneaker by SKU and size to the user's inventory.                              |
| `!inventory`          | Shows the current inventory of the user.                                             |
| `!remove "name" size` | Removes a specific size of a sneaker from the user's inventory.                      |
| `!removeSKU sku size` | Removes a specific size of a sneaker by SKU from the user's inventory.               |
| `!add "name" sku`     | Adds a new sneaker to the bot's database with the given name and SKU.                |

![image](https://github.com/user-attachments/assets/eebe9d63-3d83-4e0e-a1c8-82a64beb2715)

