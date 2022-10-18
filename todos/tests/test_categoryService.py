from rest_framework import status
from rest_framework.test import APITestCase


class TestCategoryService(APITestCase): # pragma: no cover
    """
    Testcases and helper function to test static\js\services\categoryService.js
    """

    def test_get_category(self):
        """
        Ensure we can get categories.
        """
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f"Got {response.status_code} instead of {status.HTTP_200_OK} on /api/categories/ ")

    def test_create_category(self):
        """
        Ensure we can create a new category.
        """

        # Test with valid payload
        data = {'name': 'newTestCategory'}
        response = self.client.post(
            '/api/categories/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         f"Got {response.status_code} instead of {status.HTTP_201_CREATED} on /api/categories/create/ with valid payload ")
        self.assertEqual(response.json()[
                         'name'], data['name'], f"Got {response.json()['name']} instead of { data['name']} ")

        # Test with invalid payload
        data = {}
        response = self.client.post(
            '/api/categories/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f"Got {response.status_code} instead of {status.HTTP_400_BAD_REQUEST} on /api/categories/create/ with invalid payload ")

    def test_get_categorys_task(self):
        """
        Ensure we can get task's of a new category.
        """
        data = {'name': 'newTestCategory'}
        response = self.create_category(data)
        tempId = response.json()['id']
        response = self.client.get(
            f'/api/category_tasks/{tempId}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f"Got {response.status_code} instead of {status.HTTP_200_OK} on /api/category_tasks/{tempId}")
        self.assertEqual(response.json(), [
        ], f"Got {response.json()} instead of empty list on /api/category_tasks/{tempId}")

    def test_edit_existing_category(self):
        """
        Ensure we can edit an existing category.
        """

        # Test with valid payload
        data = {'name': 'newTestCategoryForEdit'}
        response = self.create_category(data)
        tempId = response.json()['id']
        data = {'name': 'newTestCategoryForEdit_altered'}
        response = self.client.put(
            f'/api/categories/edit/{tempId}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f"Got {response.status_code} instead of {status.HTTP_200_OK} on /api/categories/edit/{tempId} with valid payload ")
        self.assertEqual(response.json()[
                         'name'], data['name'], f"Got {response.json()['name']} instead of {data['name']} on /api/categories/edit/{tempId}")

        # Test with invalid payload
        data = {'name': 'newTestCategoryForEdit'}
        response = self.create_category(data)
        tempId = response.json()['id']
        data = {}
        response = self.client.put(
            f'/api/categories/edit/{tempId}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         f"Got {response.status_code} instead of {status.HTTP_400_BAD_REQUEST} on /api/categories/edit/{tempId} with invalid payload ")

    def test_edit_not_existing_category(self):
        """
        Ensure we get error code when we try to edit a category which not exists.
        """
        data = {'name': 'newTestCategory'}
        invalidId = -1
        response = self.client.put(
            f'/api/categories/edit/{invalidId}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         f"Got {response.status_code} instead of {status.HTTP_404_NOT_FOUND} on '/api/categories/edit/{invalidId}")

    def test_delete_existing_category(self):
        """
        Ensure we can delete an existing category.
        """

        data = {'name': 'newTestCategoryForDelete'}
        response = self.create_category(data)
        tempId = response.json()['id']
        response = self.client.delete(
            f'/api/categories/delete/{tempId}', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         f"Got {response.status_code} instead of {status.HTTP_204_NO_CONTENT} on '/api/categories/delete/{tempId}")

    def test_delete_not_existing_category(self):
        """
        Ensure we get error code when we try to delete a category which not exists.
        """
        invalidId = -1
        response = self.client.delete(
            f'/api/categories/delete/{invalidId}', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         f"Got {response.status_code} instead of {status.HTTP_404_NOT_FOUND} on '/api/categories/delete/{invalidId}")

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
