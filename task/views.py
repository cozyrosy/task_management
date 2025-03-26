from django.shortcuts import render
from .models import Tasks
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import TasksListSerializer, TaskDetailSerializer
from user.utils import sanitized_bool_query_params, generic_response, validate_logged_in_user, get_pure_paginated_response, validate_field_not_request_body
from user.models import UserProfile
# Create your views here.

class TaskListView(APIView):
    """
        API to list all the tasks of a logged in user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            logged_in_user = validate_logged_in_user(request)
            if not logged_in_user:
                return generic_response(status.HTTP_401_UNAUTHORIZED, 'Access token is invalid!')


            tasks = Tasks.objects.all()
            if not tasks:
                return generic_response(status.HTTP_404_NOT_FOUND, "No data found!")
            
            user_id = request.GET.get('user_id')
            user = UserProfile.objects.filter(id=user_id).first() if user_id else logged_in_user

            if not user:
                return generic_response(status.HTTP_404_NOT_FOUND, 'User not found!')

            if user_id:
                tasks = tasks.filter(assigned_users=user)

            status = request.GET.get('status')
            if status is not None:
                tasks = tasks.filter(status=status)
            
            serialized_data = TasksListSerializer(tasks, many=True).data
            return get_pure_paginated_response(serialized_data, request)

        except Exception as ex:
            return generic_response(status.HTTP_400_BAD_REQUEST,
                                    'Error while fetching your tasks!')


class TaskDetailView(APIView):
    """
        GET --: API to fetch the details of a particular tasks.
        POST --: API to create a new task. Can assign to multiple user while creating.
        PATCH --: API to update the resource partially. Can assign to multiple user while updating.
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
                'description': data.get('description'),
                'status': data.get('status'),
                'assigned_users': data.get('assigned_users', [])  # ✅ Ensure it gets a list from request
            }

            is_error, response = validate_field_not_request_body(validated_data)
            if is_error:
                return response

            # Ensuring if assigned_users is a valid list of user IDs
            if not isinstance(validated_data['assigned_users'], list):
                return generic_response(status.HTTP_400_BAD_REQUEST, "assigned_users must be a list of user IDs.")

            # Creating the task object first (without assigned users)
            task = Tasks.objects.create(
                title=validated_data['title'],
                description=validated_data['description'],
                status=validated_data['status']
            )

            # Assigning users to ManyToMany field
            task.assigned_users.set(validated_data['assigned_users'])

            return generic_response(status.HTTP_201_CREATED, 'Task created successfully!', {'task_id': task.id})

        except Exception as ex:
            print(f'Error while creating task: {ex}')
            return generic_response(status.HTTP_400_BAD_REQUEST, 'Error while creating task')


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
                return generic_response(status.HTTP_400_BAD_REQUEST, 'No such task exists!')

            assigned_users = data.get('assigned_users', None)

            if assigned_users is not None and not isinstance(assigned_users, list):
                return generic_response(status.HTTP_400_BAD_REQUEST, "assigned_users must be a list of user IDs.")

            serializer = TaskDetailSerializer(task, data=data, partial=True) 
            if serializer.is_valid():
                serializer.save()

                # Updating ManyToMany field separately if 'assigned_users' is provided
                if assigned_users is not None:
                    task.assigned_users.set(assigned_users)

                return generic_response(status.HTTP_200_OK, 'Task updated successfully!', serializer.data)
            else:
                return generic_response(status.HTTP_400_BAD_REQUEST, f'Error: {serializer.errors}')

        except Exception as ex:
            return generic_response(status.HTTP_400_BAD_REQUEST, 'Error while updating your task!')

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
