# Course Sync Service

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Django](https://img.shields.io/badge/django-latest-green.svg)](https://www.djangoproject.com/)

A Django-based service that synchronizes course content between edX and Virtu Educate's learning management system.

## Overview

Course Sync detects and applies changes to course structures, ensuring that content updates in edX are automatically reflected in Virtu Educate's platform. The service efficiently handles:

- Creation of new courses, topics, and subtopics
- Updates to existing content
- Deletion of obsolete content

## Key Features

- **Efficient Change Detection**: Compares course structures and identifies specific changes
- **Atomic Operations**: Guarantees consistent course data through atomic database transactions
- **Robust Error Handling**: Tracks failed operations for system resilience
- **Comprehensive Testing**: Thoroughly tested with unit and integration tests

## Architecture

Course Sync is built with clean architecture principles and well-established design patterns:

### Core Components

- **CourseSyncService**: Orchestrates the sync process
- **DiffEngine**: Detects changes between course versions using Chain of Responsibility pattern
- **ChangeProcessor**: Applies detected changes using Strategy pattern
- **DataTransformer**: Converts edX data format to domain objects

```
┌─────────────────┐     ┌────────────┐     ┌────────────────┐
│ EdX Course Data │────▶│ DiffEngine │────▶│ ChangeProcessor│
└─────────────────┘     └────────────┘     └────────────────┘
                                                   │
                                                   ▼
                                           ┌────────────────┐
                                           │ Database       │
                                           └────────────────┘
```

## Installation

### Prerequisites

- Python 3.13
- Django
- Access to edX course data API

### Setup

1. Clone the repository
```bash
git clone https://github.com/virtu-educate/course-sync.git
cd course-sync
```

2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

## Usage

### Basic Implementation

```python
from course_sync.course_sync import CourseSyncService
from course_sync.data_transformer import EdxDataTransformer
from course_ware.models import Course, ExaminationLevel, AcademicClass

# Get edX course data
edx_course_data = get_edx_course_data()  # Implementation depends on your edX API

# Transform edX data
course_outline = EdxDataTransformer.transform_to_course_outline(
    structure=edx_course_data,
    course_id="course-123",
    title="Chemistry Basics"
)

# Initialize sync service
sync_service = CourseSyncService.create_service()

# Get necessary models
course = Course.objects.get(course_key="course-123")
exam_level = ExaminationLevel.objects.get(name="KCSE")
academic_class = AcademicClass.objects.get(name="Form 1")

# Perform synchronization
result = sync_service.sync_course(
    course_outline, course, exam_level, academic_class
)

print(f"Sync completed: {result.num_success} changes applied, {result.num_failed} changes failed")
```

## Testing

Run the test suite with:

```bash
pytest
```

## Design Patterns Used

For technical users, the project implements several design patterns:

1. **Strategy Pattern**: Different strategies for handling create, update, and delete operations
2. **Chain of Responsibility**: Sequential handling of course, topic, and subtopic changes
3. **Command Pattern**: Encapsulating change operations as objects

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

---

© 2025 Virtu Educate