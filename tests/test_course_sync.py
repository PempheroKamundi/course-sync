from unittest.mock import MagicMock, patch

import pytest

from course_sync.course_sync import ChangeResult, CourseSyncService
from course_sync.data_types import (
    ChangeOperation,
    CourseChangeData,
    CourseStructure,
    EdxCourseOutline,
    EntityType,
    OperationType,
)
from course_sync.diff_engine import DiffEngine
from course_ware.tests.course_ware_factory import (
    AcademicClassFactory,
    CourseFactory,
    ExaminationLevelFactory,
)


@pytest.fixture
def mock_diff_engine():
    """Create a mock DiffEngine."""
    return MagicMock(spec=DiffEngine)


@pytest.fixture
def course_sync_service(mock_diff_engine):
    """Create a CourseSyncService with a mock DiffEngine."""
    return CourseSyncService(diff_engine=mock_diff_engine)


@pytest.fixture
def course():
    """Create a test course."""
    return CourseFactory()


@pytest.fixture
def examination_level():
    """Create a test examination level."""
    return ExaminationLevelFactory()


@pytest.fixture
def academic_class():
    """Create a test academic class."""
    return AcademicClassFactory()


@pytest.fixture
def mock_course_outline():
    """Create a mock course outline."""
    outline = MagicMock(spec=EdxCourseOutline)
    outline.course_id = "test-course-id"
    outline.title = "Test Course"
    outline.structure = MagicMock(spec=CourseStructure)
    outline.structure.topics = {"topic-1", "topic-2"}
    outline.topics = []
    return outline


@pytest.mark.django_db
class TestCourseSyncService:
    """Tests for the CourseSyncService."""

    def test_sync_course_no_changes(
        self,
        course_sync_service,
        mock_diff_engine,
        course,
        examination_level,
        academic_class,
        mock_course_outline,
    ):
        """Test sync_course when there are no changes detected."""
        mock_diff_engine.diff.return_value = []

        result = course_sync_service.sync_course(
            mock_course_outline, course, examination_level, academic_class
        )

        assert isinstance(result, ChangeResult)
        assert result.num_success == 0
        assert result.num_failed == 0
        mock_diff_engine.diff.assert_called_once_with(
            course.course_outline, mock_course_outline
        )

    def test_sync_course_with_successful_changes(
        self,
        course_sync_service,
        mock_diff_engine,
        course,
        examination_level,
        academic_class,
        mock_course_outline,
    ):
        """Test sync_course when there are changes that are successfully processed."""
        changes = [
            ChangeOperation(
                operation=OperationType.UPDATE,
                entity_type=EntityType.COURSE,
                entity_id="test-course-id",
                data=CourseChangeData(
                    name="Updated Course", course_outline=mock_course_outline
                ),
            )
        ]

        mock_diff_engine.diff.return_value = changes

        with patch("course_sync.course_sync.ChangeProcessor") as mock_processor_class:
            mock_processor = mock_processor_class.return_value
            mock_processor.process_changes.return_value = []

            result = course_sync_service.sync_course(
                mock_course_outline, course, examination_level, academic_class
            )

            assert isinstance(result, ChangeResult)
            assert result.num_success == 1
            assert result.num_failed == 0
            mock_diff_engine.diff.assert_called_once_with(
                course.course_outline, mock_course_outline
            )
            mock_processor_class.assert_called_once_with(
                course=course,
                examination_level=examination_level,
                academic_class=academic_class,
            )
            mock_processor.process_changes.assert_called_once_with(changes)

    def test_sync_course_with_failed_changes(
        self,
        course_sync_service,
        mock_diff_engine,
        course,
        examination_level,
        academic_class,
        mock_course_outline,
    ):
        """Test sync_course when there are changes that fail to process."""
        changes = [
            ChangeOperation(
                operation=OperationType.UPDATE,
                entity_type=EntityType.COURSE,
                entity_id="test-course-id",
                data=CourseChangeData(
                    name="Updated Course", course_outline=mock_course_outline
                ),
            ),
            ChangeOperation(
                operation=OperationType.CREATE,
                entity_type=EntityType.TOPIC,
                entity_id="topic-1",
                data=MagicMock(),
            ),
        ]

        mock_diff_engine.diff.return_value = changes

        with patch("course_sync.course_sync.ChangeProcessor") as mock_processor_class:
            mock_processor = mock_processor_class.return_value
            mock_processor.process_changes.return_value = [
                changes[1]
            ]  # The second change failed

            result = course_sync_service.sync_course(
                mock_course_outline, course, examination_level, academic_class
            )

            assert isinstance(result, ChangeResult)
            assert result.num_success == 1
            assert result.num_failed == 1
            mock_diff_engine.diff.assert_called_once_with(
                course.course_outline, mock_course_outline
            )
            mock_processor_class.assert_called_once_with(
                course=course,
                examination_level=examination_level,
                academic_class=academic_class,
            )
            mock_processor.process_changes.assert_called_once_with(changes)

    def test_sync_course_with_partially_successful_changes(
        self,
        course_sync_service,
        mock_diff_engine,
        course,
        examination_level,
        academic_class,
        mock_course_outline,
    ):
        """Test sync_course when there are multiple changes with mixed success."""
        changes = [
            ChangeOperation(
                operation=OperationType.UPDATE,
                entity_type=EntityType.COURSE,
                entity_id="test-course-id",
                data=CourseChangeData(
                    name="Updated Course", course_outline=mock_course_outline
                ),
            ),
            ChangeOperation(
                operation=OperationType.CREATE,
                entity_type=EntityType.TOPIC,
                entity_id="topic-1",
                data=MagicMock(),
            ),
            ChangeOperation(
                operation=OperationType.DELETE,
                entity_type=EntityType.SUBTOPIC,
                entity_id="subtopic-1",
                data=None,
            ),
        ]

        mock_diff_engine.diff.return_value = changes

        with patch("course_sync.course_sync.ChangeProcessor") as mock_processor_class:
            mock_processor = mock_processor_class.return_value
            mock_processor.process_changes.return_value = [
                changes[1],
                changes[2],
            ]  # Two changes failed

            result = course_sync_service.sync_course(
                mock_course_outline, course, examination_level, academic_class
            )

            assert isinstance(result, ChangeResult)
            assert result.num_success == 1
            assert result.num_failed == 2
            mock_diff_engine.diff.assert_called_once_with(
                course.course_outline, mock_course_outline
            )
            mock_processor_class.assert_called_once_with(
                course=course,
                examination_level=examination_level,
                academic_class=academic_class,
            )
            mock_processor.process_changes.assert_called_once_with(changes)

    def test_detect_changes_method(
        self, course_sync_service, mock_diff_engine, mock_course_outline
    ):
        """Test the _detect_changes method directly."""
        old_outline = MagicMock(spec=EdxCourseOutline)
        mock_diff_engine.diff.return_value = []

        result = course_sync_service._detect_changes(old_outline, mock_course_outline)

        assert result == []
        mock_diff_engine.diff.assert_called_once_with(old_outline, mock_course_outline)

    def test_process_changes_method(
        self, course_sync_service, course, examination_level, academic_class
    ):
        """Test the _process_changes method directly."""
        changes = [MagicMock(spec=ChangeOperation)]

        with patch("course_sync.course_sync.ChangeProcessor") as mock_processor_class:
            mock_processor = mock_processor_class.return_value
            mock_processor.process_changes.return_value = []

            result = course_sync_service._process_changes(
                changes, course, examination_level, academic_class
            )

            assert result == []
            mock_processor_class.assert_called_once_with(
                course=course,
                examination_level=examination_level,
                academic_class=academic_class,
            )
            mock_processor.process_changes.assert_called_once_with(changes)
