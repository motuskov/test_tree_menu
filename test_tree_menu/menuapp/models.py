from collections import deque

from django.db import models
from django.core.exceptions import ValidationError

from .validators import validate_path


class MenuItem(models.Model):
    '''
    Represents a menu item.
    '''
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
        help_text=(
            'Parent menu item. Leave empty to create a top level element.'
        )
    )
    name = models.CharField(
        max_length=50,
        help_text=(
            'Menu item name. Must be unique for a top level element.'
        )
    )
    path = models.CharField(
        max_length=100,
        validators=[
            validate_path,
        ],
        blank=True,
        help_text=(
            'Existing Django path or path name. A path has to start with "/" '
            'symbol. Can be empty for top level elements.'
        )
    )
    position = models.PositiveIntegerField(
        default=0,
        help_text='Determine item position on curremt level.'
    )

    def __str__(self):
        return self.name

    def clean(self):
        # Check uniqueness of menu item name
        if (
            not self.pk
            and self.parent == None
            and self.__class__.objects.filter(
                parent__isnull=True,
                name=self.name
            ).exists()
        ):
            raise ValidationError(
                'A top level menu item with the given name already exists.'
            )

        return super().clean()

    @classmethod
    def get_menu_items(cls, menu_name: str) -> deque:
        '''
        Returns a list of items of the menu with name "menu_name".
        '''
        return deque(cls.objects.raw(
            'WITH RECURSIVE menu_item AS ('
                'SELECT id, '
                       'name, '
                       'path, '
                       'parent_id, '
                       'position, '
                       '0 AS level, '
                       'CAST(id AS TEXT) AS hierarchy '
                    'FROM menuapp_menuitem '
                    'WHERE parent_id IS NULL '
                         f'AND name = "{menu_name}" '
                'UNION ALL '
                'SELECT child_item.id, '
                       'child_item.name, '
                       'child_item.path, '
                       'child_item.parent_id, '
                       'child_item.position, '
                       'menu_item.level + 1 AS level, '
                       'CAST('
                            'menu_item.hierarchy || "_" || '
                            'CAST(child_item.id AS TEXT) AS TEXT'
                        ') AS hierarchy '
                    'FROM menuapp_menuitem child_item '
                    'JOIN menu_item '
                    'ON menu_item.id = child_item.parent_id '
                    'ORDER BY level DESC, position'
            ') '
            'SELECT id, '
                   'name, '
                   'path, '
                   'parent_id, '
                   'hierarchy '
                'FROM menu_item;'
        ))
