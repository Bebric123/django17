from django import template
import re


register = template.Library()

CENSORED_WORDS = [
    'редиска',
    'дурак',
    'идиот',
    'придурок',
    'мудак',
    'херня',
]

@register.filter(name='censor')
def censor(value):
    """
    Фильтр для цензурирования текста
    Заменяет буквы нежелательных слов на '*', кроме первой
    """
    if not isinstance(value, str):
        raise ValueError(f'Фильтр censor можно применять только к строкам, получен: {type(value)}')
    result = value
    
    for word in CENSORED_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        matches = pattern.finditer(result)
        for match in matches:
            matched_word = match.group()
            censored_word = matched_word[0] + '*' * (len(matched_word) - 1)
            result = result.replace(matched_word, censored_word)
    
    return result