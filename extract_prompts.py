#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Извлекает все промпты из index.html для анализа
"""

import re

# Читаем файл
with open('/Users/agershun/repo/ag/student/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Ищем все карточки с промптами
pattern = r'<div class="prompt-card visible" data-category="([^"]+)" data-prompt="([^"]+)">\s*<h3>([^<]+)</h3>'

matches = re.findall(pattern, content, re.DOTALL)

print(f"Найдено {len(matches)} промптов\n")
print("="*80)

for i, (category, prompt, title) in enumerate(matches, 1):
    # Обрезаем промпт если он слишком длинный
    short_prompt = prompt[:100] + "..." if len(prompt) > 100 else prompt
    print(f"{i}. [{category}] {title}")
    print(f"   Текущий промпт: {short_prompt}")
    print()

    if i == 20:  # Показываем первые 20 для примера
        print(f"\n... и ещё {len(matches) - 20} промптов")
        break
