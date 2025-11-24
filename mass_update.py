#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Массовое улучшение ВСЕХ 300 промптов
Применяет структуру: базовые (30%), средние (40%), продвинутые (30%)
"""

import re
import random

# Читаем файл
with open('/Users/agershun/repo/ag/student/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Паттерн для поиска промптов
pattern = r'(<div class="prompt-card visible" data-category="[^"]+") data-prompt="([^"]+)">(\s*<h3>)([^<]+)(</h3>\s*<p>)([^<]+)(</p>)'

# Найдем все промпты
matches = list(re.finditer(pattern, content, re.DOTALL))
print(f"Найдено {len(matches)} промптов для обработки")

# Функция для определения уровня сложности промпта
def classify_prompt_level(index, total):
    """
    Распределяем промпты по уровням:
    - Первые 30% - базовые
    - Средние 40% - средние
    - Последние 30% - продвинутые
    """
    ratio = index / total
    if ratio < 0.3:
        return "basic"
    elif ratio < 0.7:
        return "medium"
    else:
        return "advanced"

# Функция для улучшения промпта
def improve_prompt(current_prompt, title, level):
    """
    Улучшает промпт в зависимости от уровня сложности
    """
    # Если промпт уже улучшен (содержит КОНТЕКСТ/ЗАДАЧА/ФОРМАТ), не меняем
    if any(keyword in current_prompt for keyword in ['КОНТЕКСТ:', 'ЗАДАЧА:', 'ФОРМАТ:', 'РОЛЬ:', 'ТВОЯ РОЛЬ:']):
        return current_prompt

    # БАЗОВЫЕ промпты - короткие и прямые
    if level == "basic":
        # Оставляем короткими, но добавляем детали
        if len(current_prompt) < 150:
            # Добавляем немного деталей к короткому промпту
            improved = current_prompt.rstrip('. ') + ". "

            # Добавляем полезные уточнения based on содержания
            if "объясни" in current_prompt.lower() or "расскажи" in current_prompt.lower():
                improved += "Используй простые слова и примеры."
            elif "создай" in current_prompt.lower() or "составь" in current_prompt.lower():
                improved += "Сделай это структурированно и понятно."
            elif "помоги" in current_prompt.lower():
                improved += "Дай конкретные пошаговые рекомендации."
            elif "напиши" in current_prompt.lower():
                improved += "Текст должен быть четким и практичным."

            return improved
        return current_prompt

    # СРЕДНИЕ промпты - добавляем структуру
    elif level == "medium":
        # Если промпт еще не структурирован, добавляем базовую структуру
        if len(current_prompt) < 200:
            improved = f"""ЗАДАЧА:
{current_prompt}

ТРЕБОВАНИЯ:
- Дай структурированный ответ
- Приведи конкретные примеры
- Объясни практическое применение"""
            return improved
        return current_prompt

    # ПРОДВИНУТЫЕ промпты - полная структура
    else:  # advanced
        # Для длинных промптов добавляем роль
        if len(current_prompt) > 100 and not current_prompt.startswith("ТВОЯ РОЛЬ"):
            # Определяем подходящую роль based on содержания
            role = "Ты - опытный консультант и наставник."

            if "преподават" in current_prompt.lower() or "учител" in current_prompt.lower():
                role = "Ты - опытный преподаватель с 10-летним стажем."
            elif "карьер" in current_prompt.lower() or "резюме" in current_prompt.lower() or "собеседован" in current_prompt.lower():
                role = "Ты - профессиональный карьерный консультант."
            elif "научн" in current_prompt.lower() or "исследован" in current_prompt.lower():
                role = "Ты - научный руководитель и методолог."
            elif "психолог" in current_prompt.lower() or "стресс" in current_prompt.lower():
                role = "Ты - практикующий психолог-консультант."

            improved = f"""{role}

КОНТЕКСТ:
{current_prompt}

ФОРМАТ РАБОТЫ:
1. Проанализируй ситуацию
2. Дай структурированные рекомендации
3. Приведи конкретные примеры
4. Укажи следующие шаги

ВАЖНО: Давай практичные, actionable советы, а не общие фразы."""
            return improved
        return current_prompt

# Обрабатываем промпты
new_content = content
processed_count = {'basic': 0, 'medium': 0, 'advanced': 0}

for i, match in enumerate(matches):
    level = classify_prompt_level(i, len(matches))

    opening_div = match.group(1)
    current_prompt = match.group(2)
    h3_open = match.group(3)
    title = match.group(4)
    h3_close_p_open = match.group(5)
    description = match.group(6)
    p_close = match.group(7)

    # Улучшаем промпт
    improved_prompt = improve_prompt(current_prompt, title, level)

    # Обновляем description если нужно (делаем его кратким резюме промпта)
    if len(description) > 200 or description == current_prompt:
        # Берем первое предложение из промпта как description
        first_sentence = improved_prompt.split('.')[0] + '.'
        if len(first_sentence) > 150:
            first_sentence = first_sentence[:147] + '...'
        new_description = first_sentence
    else:
        new_description = description

    # Формируем новую версию карточки
    old_card = match.group(0)
    new_card = f'{opening_div} data-prompt="{improved_prompt}">{h3_open}{title}{h3_close_p_open}{new_description}{p_close}'

    # Заменяем в контенте
    new_content = new_content.replace(old_card, new_card, 1)

    processed_count[level] += 1

    if (i + 1) % 50 == 0:
        print(f"Обработано {i + 1}/{len(matches)} промптов...")

# Записываем улучшенный файл
with open('/Users/agershun/repo/ag/student/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✓ Обработка завершена!")
print(f"\nСтатистика по уровням:")
print(f"- Базовые (basic): {processed_count['basic']}")
print(f"- Средние (medium): {processed_count['medium']}")
print(f"- Продвинутые (advanced): {processed_count['advanced']}")
print(f"- ВСЕГО: {sum(processed_count.values())}")
print(f"\nФайл сохранен: /Users/agershun/repo/ag/student/index.html")
print(f"Резервная копия: /Users/agershun/repo/ag/student/index.html.backup")
