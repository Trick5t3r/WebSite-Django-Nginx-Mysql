from django import template
import re

### Natural sort ###

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    Coded found here : https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text.grouper) ]

####################



register = template.Library()


@register.filter
def sort_list(lst):
        try:
             return sorted(lst, key=natural_keys)

        except:
             print("An error occurred while sorting in matieresTags.py.")
             return sorted(lst)

