from django.test import TestCase
from account import models as amod
from django.contrib.auth.models import Group, Permission, ContentType
from django.contrib.auth import authenticate, login

class UserClassTest(TestCase):

    fixtures = ['data.yaml']

    def setUp(self):
        """Test creating, saving, and reloading a user"""
        self.u1 = amod.User.objects.get(email='homer@simpsons.com')
        # self.u1.first_name = 'Lisa'
        # self.u1.last_name = 'Simpson'
        # self.u1.email = 'lisa@simpsons.com'
        # self.u1.set_password('password')
        # self.u1.address = '123 Fake Street'
        # self.u1.city = 'Salt Lake City'
        # self.u1.state = 'Utah'
        # self.u1.zipcode = '12345'
        # self.u1.is_active = True
        # self.u1.is_superuser = True
        # self.u1.is_staff = True
        self.u1.save()

    def test_load_save(self):
        u2 = amod.User.objects.get(email='homer@simpsons.com')
        self.assertEqual(self.u1.first_name, u2.first_name)
        self.assertEqual(self.u1.last_name, u2.last_name)
        self.assertEqual(self.u1.email, u2.email)
        self.assertEqual(self.u1.password, u2.password)
        self.assertEqual(self.u1.address, u2.address)
        self.assertEqual(self.u1.city, u2.city)
        self.assertEqual(self.u1.state, u2.state)
        self.assertEqual(self.u1.zipcode, u2.zipcode)
        self.assertTrue(u2.is_active)
        self.assertTrue(u2.is_superuser)
        self.assertTrue(u2.is_staff)


    def test_adding_groups(self):
        """Test adding a few groups with permissions to users and then test those permissions"""
        g1 = Group()
        g1.name = 'Salespeople'
        g1.save()
        self.u1.groups.add(g1)
        self.u1.save()

        p1 = Permission()
        p1.codename = 'change_product_price'
        p1.name = 'Change the price of a product'
        p1.content_type = ContentType.objects.get(id=1)
        p1.save()

        g1.permissions.add(p1)
        g1.save()

        self.assertTrue(self.u1.groups.filter(name='Salespeople').count() > 1)
        self.assertTrue(self.u1.has_perm('change_product_price'))

    def test_permissions(self):
        """Test adding permissions to users and then test those permissions"""
        #self.u1.user_permissions.add()
        #self.assertTrue(self.u1.has_perm())

    def test_authenticate_login(self):
        """Test authenticate/login with is_anonymous"""
        u2 = authenticate(email='homer@simpsons.com', password=self.u1.check_password('doh!'))

        if u2 is not None:
            login(request, u2)
            self.assertTrue(u2.is_authenticated)

    def test_logout(self):
        """Test logout with is_anonymous"""

    def test_passwords(self):
        """Test set_password and check_password"""
        u2 = amod.User.objects.get(email='lisa@simpsons.com')
        u2.set_password('newPassword')
        self.assertTrue(u2.check_password('newPassword'))

    def test_field_changes(self):
        """Test changing fields such as first name, email, etc"""
        u2 = amod.User.objects.get(email='lisa@simpsons.com')
        u2.first_name = 'Marg'
        u2.city = 'Des Moines'
        u2.state = 'Iowa'
        u2.email = 'marg@simpsons.com'
        u2.save()
        u3 = amod.User.objects.get(email = 'marg@simpsons.com')
        self.assertEqual(u2.first_name, u3.first_name)
        self.assertEqual(u2.city, u3.city)
        self.assertEqual(u2.state, u3.state)

