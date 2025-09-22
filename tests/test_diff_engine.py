from unittest.mock import MagicMock

import pytest

from course_sync.data_types import CourseChangeData, EntityType, OperationType

from ..diff_engine import (
    CourseDiffHandler,
    DiffEngine,
    SubtopicDiffHandler,
    TopicDiffHandler,
)
from .factories import EdxCourseOutlineFactory, SubTopicFactory, TopicFactory


@pytest.fixture
def simple_course():
    """Create a simple course with 2 topics, each with 2 subtopics"""
    return EdxCourseOutlineFactory(
        topics=[
            TopicFactory(
                id="topic-1",
                name="Topic 1",
                sub_topics=[
                    SubTopicFactory(
                        id="subtopic-1-1", name="Subtopic 1.1", topic_id="topic-1"
                    ),
                    SubTopicFactory(
                        id="subtopic-1-2", name="Subtopic 1.2", topic_id="topic-1"
                    ),
                ],
            ),
            TopicFactory(
                id="topic-2",
                name="Topic 2",
                sub_topics=[
                    SubTopicFactory(
                        id="subtopic-2-1", name="Subtopic 2.1", topic_id="topic-2"
                    ),
                    SubTopicFactory(
                        id="subtopic-2-2", name="Subtopic 2.2", topic_id="topic-2"
                    ),
                ],
            ),
        ]
    )


@pytest.fixture
def modified_course(simple_course):
    """Create a modified version of the simple course with:
    - Changed course title
    - One topic deleted (topic-2)
    - One topic added (topic-3)
    - One topic renamed (topic-1 -> Updated Topic 1)
    - One subtopic deleted (subtopic-1-2)
    - One subtopic added (subtopic-1-3)
    - One subtopic renamed (subtopic-1-1 -> Updated Subtopic 1.1)
    """
    return EdxCourseOutlineFactory(
        course_id=simple_course.course_id,
        title="Updated Course Title",
        topics=[
            TopicFactory(
                id="topic-1",
                name="Updated Topic 1",
                sub_topics=[
                    SubTopicFactory(
                        id="subtopic-1-1",
                        name="Updated Subtopic 1.1",
                        topic_id="topic-1",
                    ),
                    SubTopicFactory(
                        id="subtopic-1-3", name="Subtopic 1.3", topic_id="topic-1"
                    ),
                ],
            ),
            TopicFactory(
                id="topic-3",
                name="Topic 3",
                sub_topics=[
                    SubTopicFactory(
                        id="subtopic-3-1", name="Subtopic 3.1", topic_id="topic-3"
                    ),
                ],
            ),
        ],
    )


class TestCourseDiffHandler:
    def test_new_course(self):
        """Test when a completely new course is provided"""
        # Arrange
        handler = CourseDiffHandler()
        new_course = EdxCourseOutlineFactory()

        # Act
        changes = handler.handle(None, new_course)

        # Assert
        assert len(changes) == 1
        assert changes[0].operation == OperationType.CREATE
        assert changes[0].entity_type == EntityType.COURSE
        assert changes[0].entity_id == new_course.course_id
        assert isinstance(changes[0].data, CourseChangeData)
        assert changes[0].data.name == new_course.title
        assert changes[0].data.course_outline == new_course

    def test_course_title_changed(self, simple_course):
        """Test when only the course title has changed"""
        # Arrange
        handler = CourseDiffHandler()
        mock_next_handler = MagicMock()
        handler.set_next(mock_next_handler)

        modified_course = EdxCourseOutlineFactory(
            course_id=simple_course.course_id,
            title="Updated Course Title",
            topics=simple_course.topics,
        )

        # Mock the next handler to return an empty list
        mock_next_handler.handle.return_value = []

        # Act
        changes = handler.handle(simple_course, modified_course)

        # Assert
        assert len(changes) == 1
        assert changes[0].operation == OperationType.UPDATE
        assert changes[0].entity_type == EntityType.COURSE
        assert changes[0].entity_id == modified_course.course_id
        assert changes[0].data.name == "Updated Course Title"

        # Verify next handler was called
        mock_next_handler.handle.assert_called_once_with(simple_course, modified_course)

    def test_no_course_changes(self, simple_course):
        """Test when the course has not changed"""
        # Arrange
        handler = CourseDiffHandler()
        mock_next_handler = MagicMock()
        handler.set_next(mock_next_handler)

        # Create a copy with the same properties
        same_course = EdxCourseOutlineFactory(
            course_id=simple_course.course_id,
            title=simple_course.title,
            topics=simple_course.topics,
        )

        # Mock the next handler to return an empty list
        mock_next_handler.handle.return_value = []

        # Act
        changes = handler.handle(simple_course, same_course)

        # Assert
        assert len(changes) == 0

        # Verify next handler was called
        mock_next_handler.handle.assert_called_once_with(simple_course, same_course)


class TestSubtopicDiffHandler:
    def test_subtopic_deleted(self, simple_course):
        """Test when a subtopic is deleted"""
        # Arrange
        handler = SubtopicDiffHandler()
        mock_next_handler = MagicMock()
        handler.set_next(mock_next_handler)

        # Create modified course with subtopic-1-2 removed
        modified_course = EdxCourseOutlineFactory(
            course_id=simple_course.course_id,
            title=simple_course.title,
            topics=[
                TopicFactory(
                    id="topic-1",
                    name="Topic 1",
                    sub_topics=[
                        SubTopicFactory(
                            id="subtopic-1-1", name="Subtopic 1.1", topic_id="topic-1"
                        ),
                        # subtopic-1-2 removed
                    ],
                ),
                TopicFactory(
                    id="topic-2",
                    name="Topic 2",
                    sub_topics=[
                        SubTopicFactory(
                            id="subtopic-2-1", name="Subtopic 2.1", topic_id="topic-2"
                        ),
                        SubTopicFactory(
                            id="subtopic-2-2", name="Subtopic 2.2", topic_id="topic-2"
                        ),
                    ],
                ),
            ],
        )

        # Mock the next handler to return an empty list
        mock_next_handler.handle.return_value = []

        # Act
        changes = handler.handle(simple_course, modified_course)

        # Assert
        assert len(changes) == 1
        assert changes[0].operation == OperationType.DELETE
        assert changes[0].entity_type == EntityType.SUBTOPIC
        assert changes[0].entity_id == "subtopic-1-2"
        assert changes[0].data is None

        # Verify next handler was called
        mock_next_handler.handle.assert_called_once_with(simple_course, modified_course)

    def test_subtopic_created(self, simple_course):
        """Test when a subtopic is created"""
        # Arrange
        handler = SubtopicDiffHandler()
        mock_next_handler = MagicMock()
        handler.set_next(mock_next_handler)

        # Create modified course with new subtopic-1-3
        modified_course = EdxCourseOutlineFactory(
            course_id=simple_course.course_id,
            title=simple_course.title,
            topics=[
                TopicFactory(
                    id="topic-1",
                    name="Topic 1",
                    sub_topics=[
                        SubTopicFactory(
                            id="subtopic-1-1", name="Subtopic 1.1", topic_id="topic-1"
                        ),
                        SubTopicFactory(
                            id="subtopic-1-2", name="Subtopic 1.2", topic_id="topic-1"
                        ),
                        SubTopicFactory(
                            id="subtopic-1-3", name="Subtopic 1.3", topic_id="topic-1"
                        ),  # New subtopic
                    ],
                ),
                TopicFactory(
                    id="topic-2",
                    name="Topic 2",
                    sub_topics=[
                        SubTopicFactory(
                            id="subtopic-2-1", name="Subtopic 2.1", topic_id="topic-2"
                        ),
                        SubTopicFactory(
                            id="subtopic-2-2", name="Subtopic 2.2", topic_id="topic-2"
                        ),
                    ],
                ),
            ],
        )

        # Mock the next handler to return an empty list
        mock_next_handler.handle.return_value = []

        # Act
        changes = handler.handle(simple_course, modified_course)

        # Assert
        assert len(changes) == 1
        assert changes[0].operation == OperationType.CREATE
        assert changes[0].entity_type == EntityType.SUBTOPIC
        assert changes[0].entity_id == "subtopic-1-3"
        assert changes[0].data.name == "Subtopic 1.3"
        assert changes[0].data.topic_id == "topic-1"

        # Verify next handler was called
        mock_next_handler.handle.assert_called_once_with(simple_course, modified_course)

    def test_subtopic_updated(self, simple_course):
        """Test when a subtopic name is updated"""
        # Arrange
        handler = SubtopicDiffHandler()
        mock_next_handler = MagicMock()
        handler.set_next(mock_next_handler)

        # Create modified course with renamed subtopic-1-1
        modified_course = EdxCourseOutlineFactory(
            course_id=simple_course.course_id,
            title=simple_course.title,
            topics=[
                TopicFactory(
                    id="topic-1",
                    name="Topic 1",
                    sub_topics=[
                        SubTopicFactory(
                            id="subtopic-1-1",
                            name="Updated Subtopic 1.1",
                            topic_id="topic-1",
                        ),  # Renamed
                        SubTopicFactory(
                            id="subtopic-1-2", name="Subtopic 1.2", topic_id="topic-1"
                        ),
                    ],
                ),
                TopicFactory(
                    id="topic-2",
                    name="Topic 2",
                    sub_topics=[
                        SubTopicFactory(
                            id="subtopic-2-1", name="Subtopic 2.1", topic_id="topic-2"
                        ),
                        SubTopicFactory(
                            id="subtopic-2-2", name="Subtopic 2.2", topic_id="topic-2"
                        ),
                    ],
                ),
            ],
        )

        # Mock the next handler to return an empty list
        mock_next_handler.handle.return_value = []

        # Act
        changes = handler.handle(simple_course, modified_course)

        # Assert
        assert len(changes) == 1
        assert changes[0].operation == OperationType.UPDATE
        assert changes[0].entity_type == EntityType.SUBTOPIC
        assert changes[0].entity_id == "subtopic-1-1"
        assert changes[0].data.name == "Updated Subtopic 1.1"
        assert changes[0].data.topic_id == "topic-1"

        # Verify next handler was called
        mock_next_handler.handle.assert_called_once_with(simple_course, modified_course)

    def test_multiple_subtopic_changes(self, simple_course, modified_course):
        """Test when multiple subtopic changes occur simultaneously"""
        # Arrange
        handler = SubtopicDiffHandler()
        mock_next_handler = MagicMock()
        handler.set_next(mock_next_handler)

        # Mock the next handler to return an empty list
        mock_next_handler.handle.return_value = []

        # Act
        changes = handler.handle(simple_course, modified_course)

        # Assert
        # We expect:
        # - subtopic-1-2 is deleted
        # - subtopic-1-1 is updated
        # - subtopic-1-3 is created
        assert len(changes) == 3

        # Find each type of change
        deleted = [c for c in changes if c.operation == OperationType.DELETE]
        created = [c for c in changes if c.operation == OperationType.CREATE]
        updated = [c for c in changes if c.operation == OperationType.UPDATE]

        # Check deletion
        assert len(deleted) == 1
        assert deleted[0].entity_id == "subtopic-1-2"
        assert deleted[0].entity_type == EntityType.SUBTOPIC

        # Check creation
        assert len(created) == 1
        assert created[0].entity_id == "subtopic-1-3"
        assert created[0].entity_type == EntityType.SUBTOPIC

        # Check update
        assert len(updated) == 1
        assert updated[0].entity_id == "subtopic-1-1"
        assert updated[0].entity_type == EntityType.SUBTOPIC
        assert updated[0].data.name == "Updated Subtopic 1.1"

        # Verify next handler was called
        mock_next_handler.handle.assert_called_once_with(simple_course, modified_course)


class TestTopicDiffHandler:
    def test_topic_deleted(self, simple_course):
        """Test when a topic is deleted"""
        # Arrange
        handler = TopicDiffHandler()
        mock_next_handler = MagicMock()
        handler.set_next(mock_next_handler)

        # Create modified course with topic-2 removed
        modified_course = EdxCourseOutlineFactory(
            course_id=simple_course.course_id,
            title=simple_course.title,
            topics=[
                TopicFactory(
                    id="topic-1",
                    name="Topic 1",
                    sub_topics=[
                        SubTopicFactory(
                            id="subtopic-1-1", name="Subtopic 1.1", topic_id="topic-1"
                        ),
                        SubTopicFactory(
                            id="subtopic-1-2", name="Subtopic 1.2", topic_id="topic-1"
                        ),
                    ],
                ),
                # topic-2 removed
            ],
        )

        # Mock the next handler to return an empty list
        mock_next_handler.handle.return_value = []

        # Act
        changes = handler.handle(simple_course, modified_course)

        # Assert
        assert len(changes) == 1
        assert changes[0].operation == OperationType.DELETE
        assert changes[0].entity_type == EntityType.TOPIC
        assert changes[0].entity_id == "topic-2"
        assert changes[0].data is None

        # Verify next handler was called
        mock_next_handler.handle.assert_called_once_with(simple_course, modified_course)

    def test_topic_created(self, simple_course):
        """Test when a topic is created"""
        # Arrange
        handler = TopicDiffHandler()
        mock_next_handler = MagicMock()
        handler.set_next(mock_next_handler)

        # Create modified course with new topic-3
        modified_course = EdxCourseOutlineFactory(
            course_id=simple_course.course_id,
            title=simple_course.title,
            topics=[
                TopicFactory(
                    id="topic-1",
                    name="Topic 1",
                    sub_topics=[
                        SubTopicFactory(
                            id="subtopic-1-1", name="Subtopic 1.1", topic_id="topic-1"
                        ),
                        SubTopicFactory(
                            id="subtopic-1-2", name="Subtopic 1.2", topic_id="topic-1"
                        ),
                    ],
                ),
                TopicFactory(
                    id="topic-2",
                    name="Topic 2",
                    sub_topics=[
                        SubTopicFactory(
                            id="subtopic-2-1", name="Subtopic 2.1", topic_id="topic-2"
                        ),
                        SubTopicFactory(
                            id="subtopic-2-2", name="Subtopic 2.2", topic_id="topic-2"
                        ),
                    ],
                ),
                TopicFactory(  # New topic
                    id="topic-3",
                    name="Topic 3",
                    sub_topics=[
                        SubTopicFactory(
                            id="subtopic-3-1", name="Subtopic 3.1", topic_id="topic-3"
                        ),
                    ],
                ),
            ],
        )

        # Mock the next handler to return an empty list
        mock_next_handler.handle.return_value = []

        # Act
        changes = handler.handle(simple_course, modified_course)

        # Assert
        assert len(changes) == 1
        assert changes[0].operation == OperationType.CREATE
        assert changes[0].entity_type == EntityType.TOPIC
        assert changes[0].entity_id == "topic-3"
        assert changes[0].data.name == "Topic 3"

        # Verify next handler was called
        mock_next_handler.handle.assert_called_once_with(simple_course, modified_course)

    def test_topic_updated(self, simple_course):
        """Test when a topic name is updated"""
        # Arrange
        handler = TopicDiffHandler()
        mock_next_handler = MagicMock()
        handler.set_next(mock_next_handler)

        # Create modified course with renamed topic-1
        modified_course = EdxCourseOutlineFactory(
            course_id=simple_course.course_id,
            title=simple_course.title,
            topics=[
                TopicFactory(
                    id="topic-1",
                    name="Updated Topic 1",  # Renamed
                    sub_topics=[
                        SubTopicFactory(
                            id="subtopic-1-1", name="Subtopic 1.1", topic_id="topic-1"
                        ),
                        SubTopicFactory(
                            id="subtopic-1-2", name="Subtopic 1.2", topic_id="topic-1"
                        ),
                    ],
                ),
                TopicFactory(
                    id="topic-2",
                    name="Topic 2",
                    sub_topics=[
                        SubTopicFactory(
                            id="subtopic-2-1", name="Subtopic 2.1", topic_id="topic-2"
                        ),
                        SubTopicFactory(
                            id="subtopic-2-2", name="Subtopic 2.2", topic_id="topic-2"
                        ),
                    ],
                ),
            ],
        )

        # Mock the next handler to return an empty list
        mock_next_handler.handle.return_value = []

        # Act
        changes = handler.handle(simple_course, modified_course)

        # Assert
        assert len(changes) == 1
        assert changes[0].operation == OperationType.UPDATE
        assert changes[0].entity_type == EntityType.TOPIC
        assert changes[0].entity_id == "topic-1"
        assert changes[0].data.name == "Updated Topic 1"

        # Verify next handler was called
        mock_next_handler.handle.assert_called_once_with(simple_course, modified_course)

    def test_multiple_topic_changes(self, simple_course, modified_course):
        """Test when multiple topic changes occur simultaneously"""
        # Arrange
        handler = TopicDiffHandler()
        mock_next_handler = MagicMock()
        handler.set_next(mock_next_handler)

        # Mock the next handler to return an empty list
        mock_next_handler.handle.return_value = []

        # Act
        changes = handler.handle(simple_course, modified_course)

        # Assert
        # We expect:
        # - topic-2 is deleted
        # - topic-1 is updated
        # - topic-3 is created
        assert len(changes) == 3

        # Find each type of change
        deleted = [c for c in changes if c.operation == OperationType.DELETE]
        created = [c for c in changes if c.operation == OperationType.CREATE]
        updated = [c for c in changes if c.operation == OperationType.UPDATE]

        # Check deletion
        assert len(deleted) == 1
        assert deleted[0].entity_id == "topic-2"
        assert deleted[0].entity_type == EntityType.TOPIC

        # Check creation
        assert len(created) == 1
        assert created[0].entity_id == "topic-3"
        assert created[0].entity_type == EntityType.TOPIC

        # Check update
        assert len(updated) == 1
        assert updated[0].entity_id == "topic-1"
        assert updated[0].entity_type == EntityType.TOPIC
        assert updated[0].data.name == "Updated Topic 1"

        # Verify next handler was called
        mock_next_handler.handle.assert_called_once_with(simple_course, modified_course)


class TestValidateHandlers:
    def test_invalid_handler_type(self):
        """Test that an error is raised when using an invalid handler type"""
        # Arrange
        diff_engine = DiffEngine()

        # Define a class that is not a subclass of BaseDiffHandler
        class InvalidHandler:
            pass

        # Act/Assert
        with pytest.raises(TypeError) as exc_info:
            diff_engine._create_handler_chain(
                course_handler=InvalidHandler,
                subtopic_handler=SubtopicDiffHandler,
                topic_handler=TopicDiffHandler,
            )

        # Check error message
        assert "Course handler is invalid" in str(exc_info.value)
        assert "Must be a subclass of BaseDiffHandler" in str(exc_info.value)


class TestDiffEngine:

    def test_diff_engine_integration(self, simple_course, modified_course):
        """Integration test for the diff engine with all handlers"""
        # Arrange
        diff_engine = DiffEngine()

        # Act
        changes = diff_engine.diff(simple_course, modified_course)

        # Assert
        # We expect the following changes:
        # - Course title update
        # - Topic 2 deletion
        # - Topic 1 name update
        # - Topic 3 creation
        # - Subtopic 1-2 deletion
        # - Subtopic 1-1 name update
        # - Subtopic 1-3 creation
        assert len(changes) == 7

        # Group by entity type and operation
        course_changes = [c for c in changes if c.entity_type == EntityType.COURSE]
        topic_changes = [c for c in changes if c.entity_type == EntityType.TOPIC]
        subtopic_changes = [c for c in changes if c.entity_type == EntityType.SUBTOPIC]

        # Course changes
        assert len(course_changes) == 1
        assert course_changes[0].operation == OperationType.UPDATE
        assert course_changes[0].data.name == "Updated Course Title"

        # Topic changes
        assert len(topic_changes) == 3
        topic_deletions = [
            c for c in topic_changes if c.operation == OperationType.DELETE
        ]
        topic_updates = [
            c for c in topic_changes if c.operation == OperationType.UPDATE
        ]
        topic_creations = [
            c for c in topic_changes if c.operation == OperationType.CREATE
        ]

        assert len(topic_deletions) == 1
        assert topic_deletions[0].entity_id == "topic-2"

        assert len(topic_updates) == 1
        assert topic_updates[0].entity_id == "topic-1"
        assert topic_updates[0].data.name == "Updated Topic 1"

        assert len(topic_creations) == 1
        assert topic_creations[0].entity_id == "topic-3"

        # Subtopic changes
        assert len(subtopic_changes) == 3
        subtopic_deletions = [
            c for c in subtopic_changes if c.operation == OperationType.DELETE
        ]
        subtopic_updates = [
            c for c in subtopic_changes if c.operation == OperationType.UPDATE
        ]
        subtopic_creations = [
            c for c in subtopic_changes if c.operation == OperationType.CREATE
        ]

        assert len(subtopic_deletions) == 1
        assert subtopic_deletions[0].entity_id == "subtopic-1-2"

        assert len(subtopic_updates) == 1
        assert subtopic_updates[0].entity_id == "subtopic-1-1"
        assert subtopic_updates[0].data.name == "Updated Subtopic 1.1"

        assert len(subtopic_creations) == 1
        assert subtopic_creations[0].entity_id == "subtopic-1-3"

    def test_new_course_integration(self):
        """Integration test for the diff engine with a new course"""
        # Arrange
        diff_engine = DiffEngine()
        new_course = EdxCourseOutlineFactory(topics=2)

        # Act
        changes = diff_engine.diff(None, new_course)

        # Assert
        # For a new course, we should only have one CREATE operation for the course
        assert len(changes) == 1
        assert changes[0].operation == OperationType.CREATE
        assert changes[0].entity_type == EntityType.COURSE
        assert changes[0].entity_id == new_course.course_id
