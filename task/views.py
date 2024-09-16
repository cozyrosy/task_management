from django.shortcuts import render
from .models import Tasks
from .serializers import TasksListSerializer
from user.utils import sanitized_bool_query_params, generic_response

# Create your views here.

class TaskListView(APIView):
    """
        API to list all the tasks of a logged in user.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            if not user:
                return generic_response(status.HTTP_401_UNAUTHORIZED, 'Access token is invalid!')

            if not user.is_authenticated:
                return generic_response(status.HTTP_401_UNAUTHORIZED, "User is not logged in!")

            try:
                tasks = Tasks.objects.filter(user=user)
            except Tasks.DoesNotExist:
                return generic_response(status.HTTP_400_BAD_REQUEST, 'No tasks found for the user!')

            is_completed = sanitized_bool_query_params(request.GET.get('is_completed', 0))
            
            serialized_data = TasksListSerializer(tasks, many=True).data
            return get_pure_paginated_response(serialized_data, request)

        except Exception as ex:
            print(ex)
            return generic_response(status.HTTP_400_BAD_REQUEST,
                                    'Error while fetching your tasks!')

