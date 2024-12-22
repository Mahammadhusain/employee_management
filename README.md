# Employee Management API - README

## Overview
This project provides a robust Employee Management API implemented using Django REST Framework (DRF). It supports role-based access control with Super Admin and Admin roles, ensuring secure and organized user management. The API includes CRUD operations, custom responses, filtering, pagination, and conditional permissions.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Mahammadhusain/employee_management.git
    ```

2. Navigate to the project directory:
    ```bash
    cd employee_management
    ```
3. Create Virtual environment and activate it:
  
    - Windows

        ```bash
        python -m venv venv -----> create virtual env
        
        venv\Scripts\Activate -----> activation (Cmd)
        
        .\venv\Scripts\Activate -----> activation (Powershell)

        ```
    - Linux

        ```bash
        python3 -m venv venv -----> create virtual env
        
        source venv/bin/activate -----> activation
        ```


4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Apply migrations:
    ```bash
    python manage.py migrate
    ```

6. Run the server:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Endpoints

| HTTP Method | Endpoint             | Description                                         |
|-------------|----------------------|------------------------------------------
| POST         | `api/token/`            | Generate JWT access token using username and password. 
| GET         | `api/users/`            | List all Employees.                |
| GET         | `api/users/{id}/`       | Retrieve a user's details.                         |
| GET         | `api/users/?q=xyz&q=xyz@email.com&role=employee`| Search and filter Employees.                |
| POST        | `api/users/`            | Create a new user.                                  |
| PATCH       | `api/users/{id}/`       | Update a user's details.                           |
| DELETE      | `api/users/{id}/`       | Delete a user.                                      |

## Role-Based Permissions

Permissions are defined in the `permissions.py` file.

- **Super Admin:**
  - Can **list** all employees.
  - Can **create** employee with any role.
  - Can **update** any employee.
  - Can **delete** any employee.
  
  
- **Admin:**
  - Can **list** employees under their supervision.
  - Can **create** new empolyee under their supervision.
  - Can **update** employees under their supervision. 
  - Can **delete** not allowd.
  
  

## Searching, Filtering
Defined in the `filters.py` file.
- **Searching:**
  - Searching implemented using `DjangoFilterBackend` and custom `UserFilter` class can filter by fields `name` and  `email`.
  - Example: Search by `?q=employee_name` or `?q=employee_email`.
- **Filtering:**
  - Filters implemented using `DjangoFilterBackend` and custom `UserFilter` class can filter by field `role`.
  - Example: Filter by `?role=employee`.


## Pagination
Defined in the `paginations.py` file.
- **Pagination:**
  - Custom pagination provided by `UserPagination` class.

## Send Welcome Email
Defined in the `signals.py` file.

`send_welcome_email()` signal send Welcome E-Mail if employee successfully created.

### Note - All Endpoints are tested with Postmen api client

# Thank you 
