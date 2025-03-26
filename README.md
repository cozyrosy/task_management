# task-management
Task App - REST API with JWT Authentication
This Django app provides a RESTful API for managing tasks. Users can perform CRUD (Create, Read, Update, Delete) operations on tasks, and all endpoints are secured using JWT (JSON Web Token) authentication.

**Table of Contents**
----------------------
Features
-- Technologies 
-- Requirements
-- Installation
-- API Endpoints
-- Authentication
-- Task CRUD
-- JWT Authentication
-- Running the Project

----------------------------------------------------------------------------------------------------------

**Features**

-- User authentication using JWT.

-- CRUD operations for tasks.

-- Secured endpoints for task management.

----------------------------------------------------------------------------------------------------------

**Technologies**

-- Django

-- Django Rest Framework (DRF)

-- Simple JWT for authentication

-- SQLite (or any preferred database)

----------------------------------------------------------------------------------------------------------

**Requirements**

-- Python 3.x

-- Django 4.x

-- Django Rest Framework

-- Simple JWT package for JWT authentication

-----------------------------------------------------------------------------------------------------------


**Installation**

----------------------
**1. Installation**

git clone https://github.com/your-username/task-app.git

cd task-app

----------------------
**2. Create and activate a virtual environment:**

python -m venv venv

source venv/bin/activate  # For Windows: venv\Scripts\activate

----------------------
**3. Install the dependencies:**

pip install -r requirements.txt

----------------------
**4. Run migrations:**

python manage.py migrate

----------------------
**5. Create a superuser to access the admin panel:**

python manage.py createsuperuser

----------------------

**6. Run the development server:**

python manage.py runserver

----------------------------------------------------------------------------------------------------------

****API Endpoints****
**Authentication**
-----------------------

For all APIS need to pass Authorization in the headers:

**headers -   Authorization     Bearer <access_token>**


---------
**Register** (optional, if user registration is needed):

URL: [http://127.0.0.1:8001/user/register](url)

Method: POST

Description: Registers a new user.

Payload:

{

    "email":"rose@mailinator.com",
    
    "username":"rose",
    
    "password":"start@123",
    
    "confirm_password":"start@123"
    
}

Response:

{

    "statusCode": 400,
    
    "message": "Registered Successfully.",
    
    "data": null
    
}


-------------------------------------------------------------------------------------------------------------------------------
**Login:**


URL: [http://127.0.0.1:8001/user/login](url)

Method: POST

Description: Authenticates a user and returns a JWT token.

Payload:

{

    "email": "email@mailinator.com",
  
    "password": "password123"
  
}

Response:

{

    "statusCode": 200,
    
    
    "message": null,
    
    "data": 
    
    {
        
        "user_id": 8,
        
        "access_token": 
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI3NDEzMTE2LCJpYXQiOjE3MjY1NDkxMTYsImp0aSI6IjkxMWMyZTdhNmI2NTQxNWE4ODJiODhhODBmYTg4MWY0IiwidXNlcl9pZCI6OH0.wZ0No7lw__ikXBMY2j62U1bC9RtIrdJa82gY4x9xyus",

        "refresh_token": 
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNDMyNTExNiwiaWF0IjoxNzI2NTQ5MTE2LCJqdGkiOiIwNmMxY2I1ZTcxYTE0MTE2OThlMTVmNTk0MzdmMDEwMiIsInVzZXJfaWQiOjh9.OQw0-NRKJ2H0RDPUjDK6gmYwcBapqDfiZtj5VRF8gEs"
    
    }

}

-------------------------------------------------------------------------------------------------------------------------------

****Task CRUD****
-------------------------------------------------------------------------------------------------------------------------------

**Get All Tasks (List tasks):**

URL: [http://127.0.0.1:8001/apis/tasks](url)

Method: GET

Description: Retrieves a list of all tasks.

Headers:

{

      "Authorization": "Bearer <jwt_access_token>"
}

Params:

{

      "user_id ": 12,
      
      "status" : "pending",
      
      "next_page: 2,

      "per_page": 30

}

Response:
[
  {
  
    "id": 1,
    "title": "Sample Task",
    "description": "Task details",
    "status": "pending",
    "assigned_users": [1, 2]
  }
]

For the list API handled the pagination in order to go to next page, need pass next_page=2.
If you want particular number of data at first calling need to pass the parameter per_page=30

-------------------------------------------------------------------------------------------------------------------------------

**Create Task:**

URL: [http://127.0.0.1:8001/apis/create_task/](url)

Method: POST

Description: Creates a new task.

Headers:

{

    "Authorization": "Bearer <jwt_access_token>"

}

Payload:

{

      "title": "New Task",
      
      "description": "Task details",
      
      "status": "pending",
      
      "assigned_users": [1, 2]
}

Response:

{

    "message": "Task created successfully!",
      
    "task_id": 2
}

-------------------------------------------------------------------------------------------------------------------------------

**Get Task by ID (Retrieve a specific task):**

URL: [/api/tasks/<id>/](url)

Method: GET

Description: Retrieves a task by its ID.

Headers:

{
    
    "Authorization": "Bearer <jwt_access_token>"

}

Response:

{

      "id": 1,
      "title": "Sample Task",
      "description": "Task details",
      "status": "pending",
      "assigned_users": [1, 2]
}

-------------------------------------------------------------------------------------------------------------------------------

**Update Task:**

URL: [http://127.0.0.1:8001/apis/update_task/<id>/](url)

Method: PUT (or PATCH)

Description: Updates an existing task.

Headers:

{

    "Authorization": "Bearer <jwt_access_token>"

}

Payload:

{

      "title": "Updated Task",
      "status": "completed"
}

Response:

{

       "message": "Task updated successfully!",
       "data": { "id": 1, "title": "Updated Task", "status": "completed" }
}

-------------------------------------------------------------------------------------------------------------------------------

**Delete Task:**

URL: /api/tasks/<id>/

Method: DELETE

Description: Deletes a task by its ID.

Headers:

{
    
      "Authorization": "Bearer <jwt_access_token>"

}

Response:

{
 
      "message": "Task deleted successfully."
}

-------------------------------------------------------------------------------------------------------------------------------

**Error Handling**
Errors are returned in the following format:
{

      "message": "Error description"
}

Common error codes:

1. 400 Bad Request – Invalid input data

2. 401 Unauthorized – Authentication required

3. 403 Forbidden – Access denied

4. 404 Not Found – Resource not found

**Notes**

Ensure to replace your_access_token with a valid JWT token for authenticated endpoints.

Tasks can be assigned to multiple users using a list of user IDs.

The status field in tasks can have predefined values (e.g., pending, in_progress, completed).


**JWT Authentication**

JWT tokens are used to authenticate API requests. To access any task-related endpoints, you must provide a valid token in the Authorization header.

Get the JWT token by logging in via the login endpoint.

**Include the token in the Authorization header as follows:**

Authorization: Bearer <jwt_access_token>

Running the Project

To run the project locally, make sure you have followed the installation steps above. Once the server is running, you can interact with the API via a tool like Postman or cURL.

**Start the development server:**

python manage.py runserver

-------------------------------------------------------------------------------------------------------------------------------

