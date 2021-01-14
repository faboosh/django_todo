from todo.tests.TodoClient import TodoClient
from django.test import TestCase
from rest_framework import status
from core.helpers.random_string import random_string

class TodoListHelper:
    TODO_CLIENT = None
    FOREGIN_TODO_CLIENT = None
    LAST_CREATED_TODO_LIST = None
    LAST_CREATED_TODO = None
    TODO_LIST_DATA = { 'title': 'Test123' }

    def setUp(self):
        self.TODO_CLIENT = TodoClient()
        self.FOREGIN_TODO_CLIENT = TodoClient()

    # Todo list CRUD
    def get_todo_list(self, list_id=None):
        return self.TODO_CLIENT.do_get(self.get_todo_list_URI(list_id))

    def create_todo_list(self):
        self.LAST_CREATED_TODO_LIST = self.TODO_CLIENT.do_post(
            self.TODO_CLIENT.TODO_LIST_URI, 
            self.TODO_LIST_DATA
        )

        return self.LAST_CREATED_TODO_LIST

    def delete_todo_list(self, list_id=None):     
        return self.TODO_CLIENT.do_delete(self.get_todo_list_URI(list_id))

    def update_todo_list(self, payload={}, list_id=None):
        return self.TODO_CLIENT.do_patch(self.get_todo_list_URI(list_id), payload)

    def update_other_users_todo_list(self, payload={}, list_id=None):
        return self.FOREGIN_TODO_CLIENT.do_put(self.get_todo_list_URI(list_id), payload)

    # Todo CRUD
    def create_todo(self, payload={}, list_id=None):
        return self.TODO_CLIENT.do_post(self.get_todo_URI(list_id), payload) 

    def get_todo(self, list_id=None, todo_id=None):
        return self.TODO_CLIENT.do_get(self.get_todo_URI(list_id=list_id, todo_id=todo_id)) 

    def update_todo(self, payload={}, list_id=None, todo_id=None):
        return self.TODO_CLIENT.do_patch(self.get_todo_URI(list_id=list_id, todo_id=todo_id), payload) 

    def delete_todo(self, payload={}, list_id=None, todo_id=None):
        return self.TODO_CLIENT.do_delete(self.get_todo_URI(list_id=list_id, todo_id=todo_id)) 

    def delete_other_users_todo(self, payload={}, list_id=None, todo_id=None):
        return self.FOREGIN_TODO_CLIENT.do_delete(self.get_todo_URI(list_id=list_id, todo_id=todo_id)) 

    # Util functions
    def get_last_list_id_if_none(self, list_id=None):
        if not list_id:
            list_id = self.LAST_CREATED_TODO_LIST.data['id']

        return list_id

    def get_todo_list_URI(self, list_id=None):
        list_id = self.get_last_list_id_if_none(list_id)
        return self.TODO_CLIENT.TODO_LIST_URI + str(list_id) + '/'

    def get_todo_URI(self, list_id=None, todo_id=None):
        uri = self.get_todo_list_URI(list_id) + 'todos/'
        if todo_id:
            uri += str(todo_id) + '/' 
        return uri


###################################################
## TESTS
###################################################


class TestCRUDTodoList(TodoListHelper, TestCase):
    def setUp(self):
        TodoListHelper.setUp(self)
        self.create_todo_list()

    def test_create_todo_list(self):
        response = self.LAST_CREATED_TODO_LIST
        self.assertTrue(status.is_success(response.status_code))

    def test_get_todo_list(self):
        list_id = self.LAST_CREATED_TODO_LIST.data['id']
        get_response = self.get_todo_list(list_id=list_id)
        self.assertTrue(status.is_success(get_response.status_code))

    def test_delete_todo_list(self):
        delete_response = self.delete_todo_list()
        self.assertTrue(status.is_success(delete_response.status_code))

    def test_update_todo_list(self):
        new_title = 'Test1234'
        update_response = self.update_todo_list(payload={
            'title': new_title
        })

        updated_todo_list = update_response.data

        self.assertTrue(status.is_success(update_response.status_code))
        self.assertEquals(updated_todo_list['title'], new_title)

    def test_update_other_users_todo_list(self):
        new_title = 'Test1234'

        update_response = self.update_other_users_todo_list(payload={
            'title': new_title
        })

        self.assertTrue(status.is_client_error(update_response.status_code))

class TestCRUDTodo(TodoListHelper, TestCase):
    TODO_DATA = None

    def setUp(self):
        TodoListHelper.setUp(self)
        self.TODO_LIST = self.create_todo_list()
        self.TODO_DATA = {
            'title': 'test',
            'is_completed': True
        }

    def test_create_todo(self):
        response = self.create_todo(payload=self.TODO_DATA)
        todo = response.data

        self.assertTrue(status.is_success(response.status_code))
        self.assertEquals(todo['title'], self.TODO_DATA['title'])
        self.assertEquals(todo['is_completed'], self.TODO_DATA['is_completed'])

    def test_get_todo(self):
        response = self.create_todo(payload=self.TODO_DATA)
        todo = response.data

        get_response = self.get_todo(todo_id=todo['id'])

        todo_from_api = get_response.data

        self.assertTrue(status.is_success(get_response.status_code))
        self.assertEquals(todo_from_api['title'], self.TODO_DATA['title'])
        self.assertEquals(todo_from_api['is_completed'], self.TODO_DATA['is_completed'])

    def test_update_todo(self):        
        response = self.create_todo(payload=self.TODO_DATA)
        todo = response.data
        update_response = self.update_todo(todo_id=todo['id'], payload={'is_completed': False})

        self.assertTrue(status.is_success(update_response.status_code))
        self.assertEquals(update_response.data['is_completed'], False)

    def test_delete_todo(self):        
        response = self.create_todo(payload=self.TODO_DATA)
        todo = response.data
        delete_response = self.delete_todo(todo_id=todo['id'])

        self.assertTrue(status.is_success(delete_response.status_code))

    def test_delete_other_users_todo(self):        
        response = self.create_todo(payload=self.TODO_DATA)
        todo = response.data
        delete_response = self.delete_other_users_todo(todo_id=todo['id'])

        self.assertTrue(status.is_client_error(delete_response.status_code))


