from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    """Вычитание arg из value"""
    return value - arg

@register.filter
def win_rate(wins, losses):
    """Расчет винрейта в процентах"""
    total = wins + losses
    return round((wins / total) * 100, 1) if total > 0 else 0