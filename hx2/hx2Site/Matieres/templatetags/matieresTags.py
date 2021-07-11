from django import template
import re

### Natural sort ###

def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys(text):
    '''
    Coded found here : https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
    '''
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text.grouper) ]

####################



register = template.Library()


@register.filter
def sort_list(lst):
        try:
             return sorted(lst, key=natural_keys)

        except:
             print("An error occurred while sorting in matieresTags.py.")
             return sorted(lst)

