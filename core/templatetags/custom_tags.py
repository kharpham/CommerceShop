from django import template

register = template.Library()

@register.filter(name='times')
def times(number):
    return range(number)

@register.simple_tag
def multiply(value1, value2):
    try: 
        return float(value1) * float(value2)
    except (ValueError, TypeError):
        return None
    
@register.filter(name='is_in_list')
def is_in_list(value, arg_list):
    return value in arg_list