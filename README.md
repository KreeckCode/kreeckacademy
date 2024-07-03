
# Kreeck Academy

Kreeck Academy is an online learning management system built with Django, featuring an integrated online compiler that allows learners to create, save, and manage their own coding projects. The project is containerized using Docker for easy deployment and scalability.

## Features

- **Learning Management System**: Manage programs, courses, and content for online learning.
- **Online Compiler**: Integrated compiler supporting multiple programming languages with syntax highlighting and basic code suggestion functionality.
- **User Projects**: Allow users to create, save, and manage their own coding projects.
- **Admin Interface**: Enhanced Django admin interface for better usability and management of the new models.
- **Dockerized Deployment**: Easy setup and deployment using Docker and Docker Compose.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Docker Setup](#docker-setup)
- [Models](#models)
- [Admin Interface](#admin-interface)
- [License](#license)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/kreeckacademy.git
   cd kreeckacademy
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```sh
   python manage.py migrate
   ```

5. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```sh
   python manage.py runserver
   ```

## Usage

- Access the application at `http://localhost:8000`.
- Log in with your superuser account to access the admin interface at `http://localhost:8000/admin`.
- Create programs, courses, and upload course content using the admin interface.
- Use the integrated online compiler at `http://localhost:8000/compiler/` to create, save, and manage your coding projects.

## Docker Setup

1. Build the Docker images:
   ```sh
   docker-compose build
   ```

2. Run the Docker containers:
   ```sh
   docker-compose up
   ```

3. Access the application:
   - Main app: `http://localhost:8000`
   - Compiler service: `http://localhost:8001`

4. To stop the containers, press `Ctrl+C` in the terminal or run:
   ```sh
   docker-compose down
   ```

## Models

### Program
- Title
- Summary

### Course
- Slug
- Title
- Code
- Credit
- Summary
- Program
- Level
- Year
- Semester
- Is Elective
- Price

### CourseAllocation
- Lecturer
- Courses
- Session

### Upload
- Title
- Course
- File
- Updated Date
- Upload Time

### UploadVideo
- Title
- Slug
- Course
- Video
- Summary
- Duration
- Timestamp
- Practical Assessment
- Template Code
- Solution Code
- Instructions
- Timer

### UserCode
- User
- Lesson
- Code Main
- Code Test
- Notes
- Submitted

### UserProgress
- User
- Course
- Lesson
- Completed

### UserProject
- User
- Name
- Language
- Code Main
- Code Test
- Created At
- Updated At

## Admin Interface

The Django admin interface has been enhanced to provide better usability and management of the models. Custom admin classes have been added to display relevant fields, search capabilities, and filtering options.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
