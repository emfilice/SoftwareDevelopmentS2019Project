from django.test import TestCase, Client
from fuelest.models import UserInfo, Address
from django.contrib.auth.models import User

# Create your tests here.

class AccountTestCase(TestCase):
    def setUp(self):
        user=User.objects.create_user('samy', password='Abde144!!')
        address=Address.objects.create(address1='123 Charming St.', address2='Ste. 223',
                                        city='Houston', state='TX', zip='77002')
        user_full=UserInfo.objects.create(username=user, name="Samy Gee", address=address)

    def test_database_validity(self):
        user_full=UserInfo.objects.get(name="Samy Gee")
        address=Address.objects.get(address2="Ste. 223")
        user=User.objects.get(username="samy")
        self.assertEqual(address, user_full.address)
        self.assertEqual(user, user_full.username)
        self.assertEqual(address.address1, '123 Charming St.')
        self.assertEqual(address.address2, 'Ste. 223')
        self.assertEqual(address.city, 'Houston')
        self.assertEqual(address.state, 'TX')
        self.assertEqual(address.zip, 77002)

class ViewsTestCase(TestCase):
    def setUp(self):
        user=User.objects.create_user('user', password='test')
        address=Address.objects.create(address1='123 Charming St.', address2='Ste. 223',
                                        city='Houston', state='TX', zip='77002')
        user_full=UserInfo.objects.create(username=user, name="Whatever", address=address)
        self.client = Client()
    def test_call_view_loads(self):
        self.client.login(username='user', password='test')  # defined in fixture or with factory in setUp()
        response = self.client.get('/profile/')
        self.assertTrue(response.context['profile_made'])
        response2 = self.client.get('/index/')
        self.assertTrue(response2.context['profile_made'])
