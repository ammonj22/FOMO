from django.test import TestCase
from account import models as amod

class UserClassTest(TestCase):

    def setUp(self):
        """Test creating, saving, and reloading a user"""
        self.u1 = amod.User()
        self.u1.first_name = 'Lisa'
        self.u1.last_name = 'Simpson'
        self.u1.email = 'lisa@simpsons.com'
        self.u1.set_password('password')
        self.u1.address = '123 Fake Street'
        self.u1.city = 'Salt Lake City'
        self.u1.state = 'Utah'
        self.u1.zipcode = '12345'
        self.u1.is_active = True
        self.u1.is_superuser = True
        self.u1.is_staff = True
        self.u1.save()

    def test_load_save(self):
        u2 = amod.User.objects.get(email='lisa@simpsons.com')
        self.assertEqual(self.u1.first_name, u2.first_name)
        self.assertEqual(self.u1.last_name, u2.last_name)
        self.assertEqual(self.u1.email, u2.email)
        self.assertEqual(self.u1.password, u2.password)
        self.assertEqual(self.u1.address, u2.address)
        self.assertEqual(self.u1.city, u2.city)
        self.assertEqual(self.u1.state, u2.state)
        self.assertEqual(self.u1.zipcode, u2.zipcode)


    def test_adding_groups(self):
        """Test adding a few groups"""


    def test_permissions(self):
        """Test adding permissions and using them"""
        u2 = amod.User.objects.get(email='lisa@simpsons.com')
        self.assertTrue(u2.is_active)
        self.assertTrue(u2.is_superuser)
        self.assertTrue(u2.is_staff)

    def test_authenticate_login(self):
        """Test authenticate/login with is_ananymous"""

    def test_logout(self):
        """Test logout with is_anonymous"""

    def test_passwords(self):
        """Test set_password and check_password"""
        u2 = amod.User.objects.get(email='lisa@simpsons.com')
        u2.set_password('newPassword')
        self.assertTrue(u2.check_password('newPassword'))

    def test_field_changes(self):
        """Test changing fields such as first name, email, etc"""
