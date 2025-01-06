<<<<<<< HEAD
# kreeckacademylms
Here is our Design Structure:
    https://app.eraser.io/workspace/tsh5KWN40mMELhoRS9i4

# Django CI Workflow

This repository contains the Continuous Integration (CI) workflow for a Django project. The CI workflow is designed to automate testing, code quality checks, security scanning, and deployment to staging.

## Components

### 1. Linting and Code Formatting

Linting and code formatting are performed using Flake8 and Black.

- **Flake8**: Checks Python code against PEP 8 coding standards and detects violations.
- **Black**: Automatically formats Python code according to PEP 8 standards.

### 2. Code Coverage

Code coverage testing is done using Coverage.py.

- **Coverage.py**: Measures code coverage during Python test execution to identify areas not covered by tests.

### 3. Security Scanning

Security scanning is conducted using Bandit and Safety.

- **Bandit**: Identifies common security issues in Python code.
- **Safety**: Checks installed dependencies for known security vulnerabilities.

### 4. Static Analysis

Static analysis is performed using PyLint and MyPy.

- **PyLint**: Checks Python code for errors, convention violations, and code smells.
- **MyPy**: Static type checker for Python that detects type-related errors.

### 5. Deployment to Staging

After successful testing, the application is deployed to a staging environment.

*Placeholder commands are provided. Replace them with actual deployment commands.*

### 6. Notification and Reporting

Notifications or reports are sent when a build fails.

*Placeholder commands are provided. Replace them with actual notification or reporting mechanisms.*

## Usage

To use this CI workflow, simply include the provided workflow file (`django_ci.yml`) in your GitHub repository under the `.github/workflows/` directory.

## Contributing

Contributions to improve this CI workflow are welcome! Please feel free to submit pull requests or open issues if you encounter any problems or have suggestions for enhancements.
=======
# Kreeck Academy

Kreeck Academy is an online learning management system built with Django, featuring an integrated online compiler that allows learners to create, save, and manage their own coding projects. The project is containerized using Docker for easy deployment and scalability.

## Features

- **Learning Management System**: Manage programs, courses, and content for online learning.
- **Online Compiler**: Integrated compiler supporting multiple programming languages with syntax highlighting and basic code suggestion functionality.
- **User Projects**: Allow users to create, save, and manage their own coding projects.
- **Admin Interface**: Enhanced Django admin interface for better usability and management of the new models.
- **Dockerized Deployment**: Easy setup and deployment using Docker and Docker Compose.
- **Support Ticket System**: Automatic error reporting and support ticket creation for technical issues.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Docker Setup](#docker-setup)
- [Models](#models)
- [Admin Interface](#admin-interface)
- [Contributions](#contributions)
- [Support System](#support-system)
- [Pending Issues](#pending-issues)
- [License](#license)

## Installation

1. Clone the repository:
   \`\`\`sh
   git clone https://github.com/kreeckcode/kreeckacademy.git
   cd kreeckacademy
   \`\`\`

2. Create a virtual environment and activate it:
   \`\`\`sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   \`\`\`

3. Install dependencies:
   \`\`\`sh
   pip install -r requirements.txt
   \`\`\`

4. Run migrations:
   \`\`\`sh
   python manage.py migrate
   \`\`\`

5. Create a superuser:
   \`\`\`sh
   python manage.py createsuperuser
   \`\`\`

6. Run the development server:
   \`\`\`sh
   python manage.py runserver
   \`\`\`

## Usage

- Access the application at \`http://localhost:8000\`.
- Log in with your superuser account to access the admin interface at \`http://localhost:8000/admin\`.
- Create programs, courses, and upload course content using the admin interface.
- Use the integrated online compiler at \`http://localhost:8000/compiler/\` to create, save, and manage your coding projects.

## Docker Setup

1. Build the Docker images:
   \`\`\`sh
   docker-compose build
   \`\`\`

2. Run the Docker containers:
   \`\`\`sh
   docker-compose up
   \`\`\`

3. Access the application:
   - Main app: \`http://localhost:8000\`
   - Compiler service: \`http://localhost:8001\`

4. To stop the containers, press \`Ctrl+C\` in the terminal or run:
   \`\`\`sh
   docker-compose down
   \`\`\`

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

### Ticket
- User
- Error Code
- Error Message
- Status
- Created At
- Last Updated At
- Last Updated By

### SupportTicket
- Ticket
- Assigned To
- Resolved At
- Resolution Notes
- Active
- Last Active
- Tickets Resolved

## Admin Interface

The Django admin interface has been enhanced to provide better usability and management of the models. Custom admin classes have been added to display relevant fields, search capabilities, and filtering options.

## Contributions

### Updated JavaScript for the Compiler
- Added support for multiple inputs in sequential order.
- Managed state using \`executionId\` to handle code execution in parts.

### Backend Changes
- Modified the backend to handle multiple inputs sequentially.
- Added state management to maintain the current execution state using an \`execution_id\`.
- Handled execution and input prompts dynamically.

### Docker
- Updated Docker setup to include the compiler service.
- Ensured communication between the Django app and the compiler service.

### Support System
- Implemented automatic error reporting and support ticket creation for technical issues.
- Added middleware for logging errors and creating tickets automatically.
- Created custom views and templates for managing support tickets.
- Enhanced admin interface to manage support team and tickets.

## Recent Changes

### Course and Module Integration
- Integrated module creation and assignment within course video upload functionality.
- Updated views and forms to handle module creation dynamically during video upload.
- Fixed attribute error related to accessing course modules.

### Error Handling and Debugging
- Resolved internal server error related to module attribute access in course views.
- Updated URL routing to correctly handle module assignments during video uploads.
- Addressed attribute and method inconsistencies in Django models and forms.


## Pending Issues

- [ ] Input handling for multiple inputs in the compiler.
- [ ] Error handling and logging improvements.
- [ ] Execution ID management for stateful execution of code.
- [ ] Compiler service returning EOFError when reading input lines.
- [ ] Implementing continuous code execution line by line.
- [ ] Ensuring the code executes correctly for different languages.
- [ ] Adding more comprehensive tests for the compiler integration.
- [ ] Improving user interface for input prompts and code execution feedback.
- [ ] Fixing issues related to the compiler service endpoint returning 400 Bad Request.
- [ ] General code review and optimization.

## Fixed Issues
- Automatic error reporting now creates support tickets.
- Dynamic handling of input prompts and removal from the output.

---

**Note**: This README includes recent changes and updates to the application based on ongoing development and improvements. For any issues or further contributions, please refer to the issues section on the GitHub repository.
>>>>>>> development
