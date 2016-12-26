#From Python
import collections

from django import template

"""Instantiate this module as a valid tag library.
'register' is an instance of template.Library"""
register = template.Library()


"""Make available to Django's template language by
registering with .filter() method(decorator)"""


@register.filter(name='getsubdivisions')
def getsubdivisions(value, subdivisions):
    """
    Given a list, returns a new two-dimensional list with each internal list containing
    'subdivisions' number of elements. If len(value) % 3 != 0 then the last list will contain
    len(value) % 3 number of elements.
    Example: getsubdivisions([1,2,3,4,5,6,7], 3)
             -> [[1,2,3],[4,5,6],[7]]
    """
    if not value:  # NoneType
        return []

    if not isinstance(value, collections.Iterable):
        raise ValueError("Expected value type: " + str(collections.Iterable) + ", got: " + str(type(value)))

    try:
        subdivisions = int(subdivisions)
    except ValueError:
        subdivisions = 3

    subdivided_list = []
    subdivision = []
    index = 0
    while index < len(value):
        subdivision.append(value[index])
        if len(subdivision) == subdivisions:
            subdivided_list.append(subdivision)
            subdivision = []
        index += 1
    if subdivision:
        subdivided_list.append(subdivision)
    return subdivided_list

