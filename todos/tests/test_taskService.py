from rest_framework import status
from rest_framework.test import APITestCase


class TestTaskService(APITestCase): # pragma: no cover
    """
    Testcases and helper function to test static\js\services\taskService.js
    """

    def test_get_task(self):
        """
        Ensure we can get tasks.
        """
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f"Got {response.status_code} instead of {status.HTTP_200_OK} on /api/tasks/ ")

    def test_create_task(self):
        """
        Ensure we can create task.
        """

        # Test with valid payload
        response = self.create_category()
        data = {"title": "TitleOfNewTask", "category": response.json()['id'],
                "description": "DescriptionOfNewTask", "deadline": "2022-10-31"}
        response = self.client.post('/api/tasks/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         f"Got {response.status_code} instead of {status.HTTP_201_CREATED} on /api/tasks/create/ with valid payload")
        self.assertEqual(response.json(), data,
                         f"Got {response.json()} instead of {data} ")

        # Test with invalid payload
        response = self.create_category()
        data = {}
        response = self.client.post('/api/tasks/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f"Got {response.status_code} instead of {status.HTTP_400_BAD_REQUEST} on /api/tasks/create/ with invalid payload")

    def test_edit_task(self):
        """
        Ensure we can edit task.
        """

        # Test with valid payload
        response = self.create_task()
        last_task = self.get_last_task()
        altered_task_data = {"id": last_task["id"], "title": "alteredTitle",
                             "description": "alteredDesc", "category": last_task["category"]["id"], "deadline": last_task["deadline"]}
        response = self.client.put(
            f'/api/tasks/edit/{last_task["id"]}', data=altered_task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f"Got {response.status_code} instead of {status.HTTP_200_OK} on /api/tasks/edit/{last_task['id']} with valid payload")
        del altered_task_data["id"]
        self.assertEqual(response.json(), altered_task_data,
                         f"Got {response.json()} instead of {altered_task_data}")

        # Test with invalid payload
        response = self.create_task()
        last_task = self.get_last_task()
        altered_task_data = {}
        response = self.client.put(
            f'/api/tasks/edit/{last_task["id"]}', data=altered_task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f"Got {response.status_code} instead of {status.HTTP_400_BAD_REQUEST} on /api/tasks/edit/{last_task['id']} with invalid payload")

    def test_edit_non_existing_task(self):
        """
        Ensure we get error code when we are trying to edit a task which not exist.
        """
        altered_task_data = {"id": -1, "title": "alteredTitle",
                             "description": "alteredDesc", "category": -1, "deadline": "2022-10-31"}
        response = self.client.put(
            '/api/tasks/edit/-1', data=altered_task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         f"Got {response.status_code} instead of {status.HTTP_404_NOT_FOUND} on /api/tasks/edit/-1")

    def test_delete_task(self):
        """
        Ensure we can delete task.
        """
        response = self.create_task()
        last_task = self.get_last_task()
        response = self.client.delete(
            f'/api/tasks/delete/{last_task["id"]}', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         f"Got {response.status_code} instead of {status.HTTP_204_NO_CONTENT} on /api/tasks/delete/{last_task['id']}")

    def test_delete_non_existing_task(self):
        """
        Ensure we get error code when we are trying to delete a task which not exist.
        """
        response = self.client.delete('/api/tasks/delete/-1', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         f"Got {response.status_code} instead of {status.HTTP_404_NOT_FOUND} on /api/tasks/delete/-1")

    def create_category(self, data=None):
        """
        This creates a new category as precondition for further tests
        """
        if not data:
            data = {'name': 'newTestCategory'}
        response = self.client.post(
            '/api/categories/create/', data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            self.assert_(
                False, f"Testcase cannot be tested because create_category precondition response code was: {response.status_code}")
            exit()
        return response

    def create_task(self, data=None):
        """
        This creates a task as precondition for further tests
        """
        response = self.create_category()
        data = {"title": "TitleOfNewTask", "category": response.json()['id'],
                "description": "DescriptionOfNewTask", "deadline": "2022-10-31"}
        response = self.client.post('/api/tasks/create/', data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            self.assert_(
                False, f"Testcase cannot be tested because create_task precondition response code was: {response.status_code}")
            exit()
        return response

    def get_last_task(self):
        """
        This will give you back the last task from /api/tasks/
        """
        response = self.client.get('/api/tasks/')
        return response.json()[-1]
