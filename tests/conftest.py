import pytest

from course_sync.change_processor import (
    ChangeProcessor,
    CreateStrategy,
    DeleteStrategy,
    UpdateStrategy,
)
from course_ware.tests.course_ware_factory import (
    AcademicClassFactory,
    CourseFactory,
    ExaminationLevelFactory,
    SubTopicFactory,
    TopicFactory,
)


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Automatically enable database access for all tests."""
    pass


@pytest.fixture
def course():
    return CourseFactory()


@pytest.fixture
def topic():
    return TopicFactory()


@pytest.fixture
def subtopic():
    return SubTopicFactory()


@pytest.fixture
def examination_level():
    return ExaminationLevelFactory()


@pytest.fixture
def academic_class():
    return AcademicClassFactory()


@pytest.fixture
def update_strategy():
    return UpdateStrategy()


@pytest.fixture
def delete_strategy():
    return DeleteStrategy()


@pytest.fixture
def create_strategy(course, examination_level, academic_class):
    return CreateStrategy(
        course=course,
        examination_level=examination_level,
        academic_class=academic_class,
    )


@pytest.fixture
def change_processor(course, examination_level, academic_class):
    return ChangeProcessor(
        course=course,
        examination_level=examination_level,
        academic_class=academic_class,
    )
