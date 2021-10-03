from django.contrib.auth import get_user_model
from django.test import TestCase
import datetime
from .models import Contact

User = get_user_model()
class UserTestCase(TestCase):

    def setUp(self):
        user_a = User(username='abcd', email='abc@abc.abc')
        user_a.set_password('1234')
        user_a.save()
        con = Contact.objects.create(name='qwaszx', email='qaz@qa.qaz')
        con.save()

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)

    def test_create_contact(self):
        con = Contact.objects.all().first()
        self.assertEqual(con.name, 'qwaszx')
        self.assertEqual(con.email, 'qaz@qa.qaz')

    def test_search_contact(self):
        con = Contact.objects.filter(name__icontains="qwaszx").count()
        con2 = Contact.objects.filter(email__icontains="qaz@qa.qaz").count()
        self.assertEqual(con, 1)
        self.assertEqual(con2, 1)

    def test_edit_contact(self):
        con = Contact.objects.all().first()
        con.name = 'person'
        con.email = 'person@gmail.com'
        con.save()
        self.assertEqual(con.name, 'person')
        self.assertEqual(con.email, 'person@gmail.com')

    def test_delete_contact(self):
        con = Contact.objects.all().first()
        con.delete()
        self.assertEqual(Contact.objects.all().count(), 0)