#!/usr/bin/env python3

import logging
from views.PlayerInterface import PlayerInterface

logging.basicConfig(level=logging.INFO)
logging.info("Running project 🚀")

PlayerInterface().start()
