from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, Rights


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass')

    def test_redirect_if_not_authenticated(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('login'))

    def test_index_renders_for_authenticated_user(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')


class EditTaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(username='owner', password='pass')
        self.other_user = User.objects.create_user(username='other', password='pass')
        self.task = Task.objects.create(user=self.owner, title='Original', description='desc')
    
    def test_edit_own_task(self):
        self.client.login(username='owner', password='pass')
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {
            'title': 'Updated Title',
            'completed': 'True'
        })
        self.assertRedirects(response, reverse('index'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Title')
        self.assertTrue(self.task.completed)

    def test_delete_task(self):
        self.client.login(username='owner', password='pass')
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {'delete': '1'})
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_edit_not_owner_without_rights(self):
        self.client.login(username='other', password='pass')
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {
            'title': 'Hack'
        })
        self.assertRedirects(response, reverse('index'))
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.title, 'Hack')

    def test_edit_not_owner_with_edit_right(self):
        Rights.objects.create(user=self.other_user, task=self.task, can_edit=True)
        self.client.login(username='other', password='pass')
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {
            'title': 'Changed by Other',
            'completed': 'False'
        })
        self.assertRedirects(response, reverse('index'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Changed by Other')
