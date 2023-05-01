'''
Implements a custom template for output tree menus.
'''
from collections import deque
from typing import Optional

from django import template
from django.urls import reverse
from django.core.exceptions import ValidationError

from ..models import MenuItem
from ..validators import validate_path


register = template.Library()

def list_to_tree(
        items: deque[MenuItem],
        parent: Optional[MenuItem] = None
    ) -> Optional[MenuItem]:
    '''
    Converts list of sorted items "items" to tree structure, adding child
    items into "childs" attribute of "parent".
    Returns the root of the resulting tree.
    '''
    while items:
        # Get item and add it in parent's child list
        item = items.popleft()
        if parent:
            parent.childs.append(item)

        # Go down if the next item is a child of the current one
        if items and items[0].parent_id == item.id:
            item.childs = []
            list_to_tree(items, item)

        # Go up if the next item isn't a child of parent
        if not items or not parent or items[0].parent_id != parent.id:
            return item

@register.inclusion_tag('menuapp/tags/menu.html', takes_context=True)
def draw_menu(
        context: template.context.RequestContext,
        menu_name: str
    ) -> None:
    '''
    Template tag function for drawing a menu with name "menu_name" on web
    pages.
    '''
    # Get current path and current path name
    current_path = context['request'].path_info
    current_path_name = context['request'].resolver_match.url_name

    # Retrieve all items by given menu name
    menu_items = MenuItem.get_menu_items(menu_name)

    # Get current (selected) menu item
    current_menu_item = next(
        (menu_item for menu_item in menu_items
         if menu_item.path in [current_path, current_path_name]),
        None
    )

    # Mark current menu item
    if current_menu_item:
        current_menu_item.current = True

    # Mark openned menu items
    if current_menu_item:
        # Get openned menu item ids
        openned_ids = [int(id) for id in current_menu_item.hierarchy.split('_')]

        # Mark openned menu items
        [setattr(
            menu_item,
            'open',
            menu_item.id in openned_ids
         ) for menu_item in menu_items]

    # Check path and convert named url to absolute url
    for menu_item in menu_items:
        try:
            validate_path(menu_item.path)
        except ValidationError:
            menu_item.path = None
        if menu_item.path and not menu_item.path.startswith('/'):
            menu_item.path = reverse(menu_item.path)

    # Convert items list to tree structure
    menu = list_to_tree(menu_items)

    return {'menu': menu}
