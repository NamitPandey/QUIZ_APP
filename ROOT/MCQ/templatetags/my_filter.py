from django import template
from django.template.defaultfilters import stringfilter
import calendar
register = template.Library()

""" THE FILTER WILL ONLY ACCEPT STRING VALUE"""
@register.filter(name='replace')
@stringfilter
def replace_var(value):
    """REMOVE ALL UNDERSCORE WITH SPACE"""

    return value.replace("_", ' ')


""" FILETER WILL INCREMENT THE VALUE BY 1 TO ANY GIVEN VALUE """
@register.filter(name='addPage')
@stringfilter
def replace_var(value):

    return int(value)+1

""" FILETER WILL DECREMENT THE VALUE BY 1 TO ANY GIVEN VALUE """
@register.filter(name='subPage')
@stringfilter
def replace_var(value):
    """REMOVE ALL UNDERSCORE WITH SPACE"""

    return int(value)-1


""" FILTER WILL RETURN A LIST """
@register.filter(name='makelist')
@stringfilter
def list_gen(value):
    """REMOVE ALL UNDERSCORE WITH SPACE"""

    return value.split(" ")

""" multiply vaule by given number """
@register.filter(name='mul')
@stringfilter
def multiplication(value, second):
    """multiply vaule by given number"""

    return int(value)*int(second)

""" calculate percentage """
@register.filter(name='perc')
@stringfilter
def percentage_calc(value, denominator):
    """calculate percentage"""

    return round((int(value)/int(denominator))*100,1)

""" Will map program """
@register.filter(name='prgMap')
@stringfilter
def prg_map(prg):

    prgDict = {
    "Chemical_Engineering": "Chemical Engineering" ,
    "Mechanical_Engineering": "Mechanical Engineering" ,
    "Computer_Science_and_Engineering": "Computer Science & Engineering" ,
    "Fire_and_Safety_Engineering": "Fire & Environment, Health, Safety Engineering" ,
    "Chemistry_HONS": "Chemistry (Hons.)",
    "Biotechnology_HONS": "Biotechnology (Hons.)" ,
    "Industrial_Chemistry_HONS": "Industrial Chemistry (Hons.)" ,
    "Micro_Biology_HONS": "Micro Biology (Hons.)" ,
    "Chemistry_MSC": "Chemistry (M.Sc.)" ,
    "Biotechnology_MSC": "Biotechnology (M.Sc.)" ,
    "Industrial_Chemistry_MSC": "Industrial Chemistry (M.Sc.)" ,
    "Chemistry_PHD": "Chemistry (Ph. D)" ,
    "Biotechnology_PHD": "Biotechnology (Ph. D)" ,
    "General": "General" ,
    "Business_Analytics": "Business Analytics" ,
    }

    return prgDict[prg]


""" will underline value iterated from list """
@register.filter(name='underline')
@stringfilter
def underline(val, clr):


    return f"<u style='color:{clr};'>"+val+"</u>"

""" remaining percentage """
@register.filter(name='perRemain')
@stringfilter
def remain_perc(val):

    try:
        return 100-int(val)
    except:
        return val
""" actual attempts """
@register.filter(name='attempts')
@stringfilter
def get_attempts(loopData, actData):

    try:
        filterData = actData.query(f"CATEGORY == '{loopData}'").reset_index(drop=True)['TOTAL_ATTEMPT'][0]

        return filterData
    except:
        return 10
