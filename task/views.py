from django.shortcuts import render
from .models import Tasks
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import TasksListSerializer, TaskDetailSerializer
from user.utils import sanitized_bool_query_params, generic_response, validate_logged_in_user, get_pure_paginated_response, validate_field_not_request_body

# Create your views here.

class TaskListView(APIView):
    """
        API to list all the tasks of a logged in user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = validate_logged_in_user(request)
            if not user:
                return generic_response(status.HTTP_401_UNAUTHORIZED, 'Access token is invalid!')

            tasks = Tasks.objects.filter(user=user)
            if not tasks:
                return generic_response(status.HTTP_404_NOT_FOUND, "No data found!")

            is_completed = sanitized_bool_query_params(request.GET.get('is_completed', 0))
            if is_completed is not None:
                tasks = tasks.filter(is_completed=is_completed)
            
            serialized_data = TasksListSerializer(tasks, many=True).data
            return get_pure_paginated_response(serialized_data, request)

        except Exception as ex:
            print(ex)
            return generic_response(status.HTTP_400_BAD_REQUEST,
                                    'Error while fetching your tasks!')


class TaskDetailView(APIView):
    """
        GET --: API to fetch the details of a particular tasks.
        POST --: API to create a new task.
        PATCH --: API to update the resource partially.
        DELETE --: API to delete a resource for the given id.
    """
    def get(self, request, task_id):
        try:
            user = validate_logged_in_user(request)
            if not user:
                return generic_response(status.HTTP_401_UNAUTHORIZED, 'Access token is invalid!')

            task = Tasks.objects.filter(id=task_id).first()
            if not task:
                return generic_response(status.HTTP_404_NOT_FOUND, "No data found!")
            
            serialized_data = TaskDetailSerializer(task).data
            return generic_response(status.HTTP_200_OK, data=serialized_data)

        except Exception as ex:
            print(ex)
            return generic_response(status.HTTP_400_BAD_REQUEST,
                                    'Error while fetching your tasks!')

    def post(self, request):
        try:
            user = validate_logged_in_user(request)
            if not user:
                return generic_response(status.HTTP_401_UNAUTHORIZED, 'Access token is invalid!')

            data = request.data
            validated_data = {
                'title': data.get('title'),
                'description': data.get('description')
            }

            is_error, response = validate_field_not_request_body(validated_data)
            if is_error:
                return response
            
            validated_data['is_completed'] = data.get('is_completed')
            validated_data['user'] = user.id
            print(user)
            
            serializer = TaskDetailSerializer(data=validated_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return generic_response(status.HTTP_400_BAD_REQUEST, f'Error:{serializer.errors}')

            return generic_response(status.HTTP_200_OK,message="Task created successfully.", data=serializer.data)

        except Exception as ex:
            return generic_response(status.HTTP_400_BAD_REQUEST,
                                    'Error while updatin your tasks!')

    def patch(self, request, task_id):
        try:
            user = validate_logged_in_user(request)
            if not user:
                return generic_response(status.HTTP_401_UNAUTHORIZED, 'Access token is invalid!')

            data = request.data
            data['user'] = user.id
            
            try:
                task = Tasks.objects.get(id=task_id)
            except Tasks.DoesNotExist:
                return generic_response(status.HTTP_400_BAD_REQUEST, 'No such task exists in your list!')

            serializer = TaskDetailSerializer(task, data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return generic_response(status.HTTP_400_BAD_REQUEST, f'Error:{serializer.errors}')

            return generic_response(status.HTTP_200_OK, data=serializer.data)

        except Exception as ex:
            return generic_response(status.HTTP_400_BAD_REQUEST,
                                    'Error while updating your tasks!')

    def delete(self, request, task_id):
        try:
            user = validate_logged_in_user(request)
            if not user:
                return generic_response(status.HTTP_401_UNAUTHORIZED, 'Access token is invalid!')

            try:
                task = Tasks.objects.get(id=task_id)
            except Tasks.DoesNotExist:
                return generic_response(status.HTTP_400_BAD_REQUEST, 'No such task exists in your list!')
            
            task.delete()
            return generic_response(status.HTTP_200_OK, 'Task deleted successfully.')

        except Exception as ex:
            return generic_response(status.HTTP_400_BAD_REQUEST,
                                    'Error while fetching your tasks!')
