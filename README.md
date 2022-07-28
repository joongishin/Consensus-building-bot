# Chatbots Facilitating Consensus-Building in Asynchronous Co-Design

This repository provides the chatbot created for the UIST'22 publication of [Chatbots Facilitating Consensus-Building in Asynchronous Co-Design]().

## Abstract

Consensus-building is an essential process for the success of co-design projects. To build consensus, stakeholders need to discuss conflicting needs and viewpoints, converge their ideas toward shared interests, and grow their willingness to commit to group decisions. However, managing group discussions is challenging in large co-design projects with multiple stakeholders. In this paper, we investigate the interaction design of a chatbot that can mediate consensus-building conversationally. By interacting with individual stakeholders, the chatbot collects ideas to satisfy conflicting needs and engages stakeholders to consider others' viewpoints, without having stakeholders directly interact with each other. Results from an empirical study in an educational setting (N = 12) suggest that the approach can increase stakeholders' commitment to group decisions and maintain the effect even on the group decisions that conflict with personal interests. We conclude that chatbots can facilitate consensus-building in small-to-medium-sized projects, but more work is needed to scale up to larger projects.

## Setup

1. Install the following libraries:
      - [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (13.12)
      - [Inflect](https://pypi.org/project/inflect/) (5.6.2)

2. Follow the link to create a token for your Telegram bot:
      - https://github.com/python-telegram-bot/python-telegram-bot

3. Update the token in the consensus-building-bot.py with your Telegram bot's token.
"""
      updater = Updater("token")
"""

## Use

- Run consensus-building-bot.py to try the conversation flow. 
- The sample sentences can be found in dialogue.py.
