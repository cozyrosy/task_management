from rest_framework import status
from rest_framework.response import Response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


def generic_response(status_code=status.HTTP_200_OK, message=None, data=None, common_data={}):
    response_data = {'statusCode': status_code, 'message': message, 'data': data}
    if common_data:
        for key, value in common_data.items():
            response_data[key] = value

    response = Response(response_data, status=status_code)
    return response


def validate_field_not_request_body(request_body_fields={}):
    for field, value in request_body_fields.items():
        if value is None or not value:
            # logger.debug('Missing {} in body parameter which is required field!'.format(field))
            return (True, generic_response(status.HTTP_400_BAD_REQUEST,
                                           'Missing {} in body parameter which is required field!'.format(field)))
    return False, None


# def validate_logged_in_user(request):
#     token = request.GET.get('access_token')
#     data = {'token': token}
#     try:
#         valid_data = VerifyJSONWebTokenSerializer().validate(data)
#         if valid_data['user']:
#             messages.success(request, 'User logged in. Please try again.')
#         else:
#             messages.error(request, 'User not logged in. Please try again.')
#         return valid_data['user']
#     except Exception as ex:
#         print('Error while verifying access token %s', ex)
#         return None


def sanitized_bool_query_params(query_param) ->bool:
    """
    Sanitizes a query parameter and returns a boolean value based on its validity.

    Args:
        query_param (str or int or bool): The query parameter to be sanitized.

    Returns:
        bool: The sanitized boolean value of the query parameter.

    Examples:
        >>> sanitized_bool_query_params("true")
        True
        >>> sanitized_bool_query_params("false")
        False
        >>> sanitized_bool_query_params(1)
        True
        >>> sanitized_bool_query_params(0)
        False
        >>> sanitized_bool_query_params("invalid")
        False
    """

    # Check if query_param is a string.
    if isinstance(query_param, str):
        # Convert string to lowercase for case-insensitive comparison.
        lowercase_query_param = query_param.lower()  

        # Check if the lowercase string matches any of the valid representations of True.
        if lowercase_query_param in {"true", "yes", "t", "y", "1"}:
            return True
        # Check if the lowercase string matches any of the valid representations of False.
        elif lowercase_query_param in {"false", "no", "f", "n", "0"}:
            return False
    # Check if query_param is an integer and its value is either 0 or 1.
    elif isinstance(query_param, int) and query_param in {0, 1}:
        # Convert the integer 1 to True and 0 to False.
        return bool(query_param)
    # Check if query_param is and bool and true, then return true
    elif isinstance(query_param, bool) and query_param:
        return True
    
    # Return False for any other cases (invalid inputs).
    return False


def get_pure_paginated_response(serialized_data, request, common_data={}):
    """
        This function is used to create a pagination for the API responses, need to pass list of dict data
    """
    per_page = int(request.GET.get('per_page', 10))
    page = int(request.GET.get('page', 1))

    if int(per_page) == -1:
        return generic_response(data=serialized_data)

    paginator = Paginator(serialized_data, per_page)

    try:
        paginated_data = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        paginated_data = paginator.page(1)

    serialized_paginated_data = serialized_data[paginated_data.start_index() - 1:paginated_data.end_index()]

    has_next_page = paginated_data.has_next()
    base_url = request.build_absolute_uri().split('?')[0]
    
    next_params = f'per_page={per_page}&page={paginated_data.next_page_number()}'
    next_link = f'{base_url}?{next_params}' if paginated_data.has_next() else None
    
    prev_params = f'per_page={per_page}&page={paginated_data.previous_page_number()}'
    previous_link = f'{base_url}?{prev_params}' if paginated_data.has_previous() else None

    response_data = {
        'statusCode': status.HTTP_200_OK,
        'hasNextPage': has_next_page,
        'next': next_link,
        'previous': previous_link,
        'count': paginator.count,
        'message': None,
        'data': serialized_paginated_data,
    }

    if common_data:
        for key, value in common_data.items():
            response_data[key] = value

    return Response(response_data, status=status.HTTP_200_OK)
