from django import template

register = template.Library()


def get_stars_format(number) -> str:
    return f'{number}★'


register.filter('get_stars_format', get_stars_format)
