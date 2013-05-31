"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import factory
from django.contrib.auth import get_user_model
User = get_user_model()


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    email = 'admin@admin.com'
    username = 'admin'
    password = 'adm1n'

    is_superuser = True
    is_staff = True
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user

class PollsTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.user = UserFactory.create()


    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_poll_via_admin_site(self):
        self.browser.get(self.live_server_url+'/admin/')

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('adm1n')
        password_field.send_keys(Keys.ENTER)

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        polls_links = self.browser.find_elements_by_link_text('Polls')
        self.assertEqual(len(polls_links), 2)


        self.fail('Finish the test!')
