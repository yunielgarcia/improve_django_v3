from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Menu, Item, Ingredient


# MODELS

class MenuModelTests(TestCase):

    def setUp(self):
        self.chef = User.objects.create(username='ygarcia', email='ygarcia@email.com')
        self.items_test = Item.objects.create(
            name='item_test_name',
            description='item_test_description',
            chef=self.chef
        )

    def test_menu_creation(self):
        menu = Menu.objects.create(
            season='Seasont',
        )
        menu.items.add(self.items_test)
        now = timezone.now()
        self.assertLess(menu.created_date, now)


class ItemModelTests(TestCase):

    def setUp(self):
        self.chef = User.objects.create(username='ygarcia', email='ygarcia@email.com')
        self.ingredients_test = Ingredient.objects.create(
            name='ingredient'
        )
        self.before_count = Item.objects.count()

    def test_item_creation(self):
        item = Item.objects.create(
            name='item_test_name',
            description='item_test_description',
            chef=self.chef
        )
        item.ingredients.add(self.ingredients_test)
        count = Item.objects.count()
        self.assertNotEqual(self.before_count, count)


class IngredientModelTests(TestCase):
    before_count = Item.objects.count()

    def test_ingredient_creation(self):
        Ingredient.objects.create(
            name='ingredient_test_name'
        )
        count = Item.objects.count()
        self.assertNotEqual(self.before_count, count)


# VIEWS
class MenuViewsTests(TestCase):
    def setUp(self):
        self.chef = User.objects.create(username='ygarcia', email='ygarcia@email.com')

        self.item1 = Item.objects.create(
            name='item_test_name',
            description='item_test_description',
            chef=self.chef
        )
        self.item2 = Item.objects.create(
            name='item_test_name2',
            description='item_test_description2',
            chef=self.chef
        )

        self.menu1 = Menu.objects.create(
            season='Seasont',
        )
        self.menu1.items.add(self.item1, self.item2)

        self.menu2 = Menu.objects.create(
            season='Seasont2',
        )
        self.menu2.items.add(self.item2)

    def test_menu_list_view(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu1, resp.context['menu'])
        self.assertIn(self.menu2, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, self.menu1.season)



