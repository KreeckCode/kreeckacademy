from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class AppTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            is_student=True,
        )

    def test_landing_view(self):
        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on your expected output

    def test_compiler_view(self):
        response = self.client.get(reverse('compiler'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on your expected output


    # Add more test cases for other views

    def tearDown(self):
        # Clean up any created test data if needed
        pass

    """
    def test_post_add_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_item'), data={'title': 'Test Post', 'content': 'Test Content'})
        print(response.content.decode())  # Print the response content for debugging
        self.assertEqual(response.status_code, 302)  # Ensure there is a redirect
        self.assertRedirects(response, reverse('home'))  # Update to match the actual redirect destination
        # Add more assertions based on your expected output
"""
