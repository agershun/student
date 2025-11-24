#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для автоматического улучшения всех 300 промптов в index.html
"""

import re

# Читаем файл
with open('/Users/agershun/repo/ag/student/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Словарь с улучшенными промптами
# Ключ - название карточки (h3), значение - {'level': 'basic'/'medium'/'advanced', 'prompt': 'текст промпта', 'description': 'краткое описание'}

improved_prompts = {
    # СТУДЕНТЫ - УЧЕБА (study) - 50 промптов