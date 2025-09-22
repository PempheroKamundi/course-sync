from unittest.mock import MagicMock, patch

from course_sync.data_types import (
    ChangeOperation,
    CourseChangeData,
    DefaultChangeData,
    EntityType,
    OperationType,
    SubTopicChangeData,
)
from course_ware.models import Course, SubTopic, Topic
from course_ware.tests.course_ware_factory import TopicFactory


class TestCreateStrategy:
    def test_create_topic(self, create_strategy):
        topic_id = "topic-123"
        topic_data = MagicMock()
        topic_data.name = "Test Topic"
        change = ChangeOperation(
            operation=OperationType.CREATE,
            entity_type=EntityType.TOPIC,
            entity_id=topic_id,
            data=topic_data,
        )

        topics_count_before = Topic.objects.count()

        result = create_strategy.process(change)

        assert result is True
        assert Topic.objects.count() == topics_count_before + 1

        created_topic = Topic.objects.get(block_id=topic_id)
        assert created_topic.name == topic_data.name
        assert created_topic.examination_level == create_strategy._examination_level
        assert created_topic.academic_class == create_strategy._academic_class
        assert created_topic.course == create_strategy._course

    def test_create_subtopic(self, create_strategy, subtopic):
        topic = TopicFactory()
        subtopic_data = SubTopicChangeData(topic_id="Test Name", name="Test Name")
        subtopic_data.name = subtopic.name
        subtopic_data.topic_id = topic.id
        change = ChangeOperation(
            operation=OperationType.CREATE,
            entity_type=EntityType.SUBTOPIC,
            entity_id="sample_block_id",
            data=subtopic_data,
        )

        subtopics_count_before = SubTopic.objects.count()

        result = create_strategy.process(change)

        assert result is True
        assert SubTopic.objects.count() == subtopics_count_before + 1

        created_subtopic = SubTopic.objects.get(block_id="sample_block_id")
        assert created_subtopic.name == subtopic_data.name
        assert created_subtopic.topic_id == subtopic_data.topic_id

    def test_create_unsupported_entity(self, create_strategy):
        change = ChangeOperation(
            operation=OperationType.CREATE,
            entity_type=EntityType.COURSE,  # Unsupported for creation in the provided code
            entity_id="course-789",
            data=MagicMock(),
        )

        result = create_strategy.process(change)

        assert result is False


class TestUpdateStrategy:
    def test_update_course(self, update_strategy, course):
        course_data = CourseChangeData(name=course.name, course_outline={})
        course_data.name = "Updated Course"
        course_data.course_outline = {"hello": "world"}
        change = ChangeOperation(
            operation=OperationType.UPDATE,
            entity_type=EntityType.COURSE,
            entity_id=course.id,
            data=course_data,
        )

        result = update_strategy.process(change)

        updated_course = Course.objects.get(id=course.id)

        assert result is True
        assert updated_course.name == course_data.name
        assert updated_course.course_outline == course_data.course_outline

    def test_update_topic(self, update_strategy, topic):
        topic_data = DefaultChangeData(name=topic.name)
        topic_data.name = "Updated Topic"
        change = ChangeOperation(
            operation=OperationType.UPDATE,
            entity_type=EntityType.TOPIC,
            entity_id=topic.block_id,
            data=topic_data,
        )

        result = update_strategy.process(change)

        updated_topic = Topic.objects.get(block_id=topic.block_id)

        assert result is True
        assert updated_topic.name == "Updated Topic"

    def test_update_subtopic(self, update_strategy, subtopic):
        subtopic_data = SubTopicChangeData(name=subtopic.name, topic_id=subtopic.id)
        subtopic_data.name = "Updated Subtopic"
        change = ChangeOperation(
            operation=OperationType.UPDATE,
            entity_type=EntityType.SUBTOPIC,
            entity_id=subtopic.block_id,
            data=subtopic_data,
        )

        result = update_strategy.process(change)

        updated_subtopic = SubTopic.objects.get(block_id=subtopic.block_id)

        assert result is True
        assert updated_subtopic.name == "Updated Subtopic"


class TestDeleteStrategy:
    def test_delete_course(self, delete_strategy, course):
        change = ChangeOperation(
            operation=OperationType.DELETE,
            entity_type=EntityType.COURSE,
            entity_id=course.id,
            data=None,
        )

        result = delete_strategy.process(change)

        assert result is True
        assert not Course.objects.filter(id=course.id).exists()

    def test_delete_topic(self, delete_strategy, topic):
        change = ChangeOperation(
            operation=OperationType.DELETE,
            entity_type=EntityType.TOPIC,
            entity_id=topic.block_id,
            data=None,
        )

        result = delete_strategy.process(change)

        assert result is True
        assert not Topic.objects.filter(id=topic.id).exists()

    def test_delete_subtopic(self, delete_strategy, subtopic):
        change = ChangeOperation(
            operation=OperationType.DELETE,
            entity_type=EntityType.SUBTOPIC,
            entity_id=subtopic.block_id,
            data=None,
        )

        result = delete_strategy.process(change)

        assert result is True
        assert not SubTopic.objects.filter(id=subtopic.id).exists()


class TestChangeProcessor:
    def test_init(self, change_processor):
        """Test that the processor initializes with the correct strategies"""

        # Check that all three strategies are initialized
        assert len(change_processor._strategies) == 3
        assert OperationType.CREATE in change_processor._strategies
        assert OperationType.UPDATE in change_processor._strategies
        assert OperationType.DELETE in change_processor._strategies

    def test_process_changes_successful(self, change_processor):
        """Test that changes are processed successfully"""

        # Create mock strategies
        create_strategy_mock = MagicMock()
        create_strategy_mock.process.return_value = True
        update_strategy_mock = MagicMock()
        update_strategy_mock.process.return_value = True
        delete_strategy_mock = MagicMock()
        delete_strategy_mock.process.return_value = True

        # Replace real strategies with mocks
        change_processor._strategies = {
            OperationType.CREATE: create_strategy_mock,
            OperationType.UPDATE: update_strategy_mock,
            OperationType.DELETE: delete_strategy_mock,
        }

        # Create test changes
        create_change = ChangeOperation(
            operation=OperationType.CREATE,
            entity_type=EntityType.TOPIC,
            entity_id="topic-123",
            data=MagicMock(),
        )

        update_change = ChangeOperation(
            operation=OperationType.UPDATE,
            entity_type=EntityType.SUBTOPIC,
            entity_id="subtopic-456",
            data=MagicMock(),
        )

        delete_change = ChangeOperation(
            operation=OperationType.DELETE,
            entity_type=EntityType.COURSE,
            entity_id="course-789",
            data=None,
        )

        changes = [create_change, update_change, delete_change]

        # Process changes
        failed_changes = change_processor.process_changes(changes)

        # Assertions
        assert len(failed_changes) == 0
        create_strategy_mock.process.assert_called_once_with(create_change)
        update_strategy_mock.process.assert_called_once_with(update_change)
        delete_strategy_mock.process.assert_called_once_with(delete_change)

    def test_process_changes_with_failures(self, change_processor):
        """Test that failed changes are properly reported"""

        # Create mock strategies with some failures
        create_strategy_mock = MagicMock()
        create_strategy_mock.process.return_value = False  # This one fails
        update_strategy_mock = MagicMock()
        update_strategy_mock.process.return_value = True
        delete_strategy_mock = MagicMock()
        delete_strategy_mock.process.return_value = True

        # Replace real strategies with mocks
        change_processor._strategies = {
            OperationType.CREATE: create_strategy_mock,
            OperationType.UPDATE: update_strategy_mock,
            OperationType.DELETE: delete_strategy_mock,
        }

        # Create test changes
        create_change = ChangeOperation(
            operation=OperationType.CREATE,
            entity_type=EntityType.TOPIC,
            entity_id="topic-123",
            data=MagicMock(),
        )

        update_change = ChangeOperation(
            operation=OperationType.UPDATE,
            entity_type=EntityType.SUBTOPIC,
            entity_id="subtopic-456",
            data=MagicMock(),
        )

        changes = [create_change, update_change]

        # Process changes
        failed_changes = change_processor.process_changes(changes)

        # Assertions
        assert len(failed_changes) == 1
        assert failed_changes[0] == create_change
        create_strategy_mock.process.assert_called_once_with(create_change)
        update_strategy_mock.process.assert_called_once_with(update_change)

    def test_process_changes_with_exceptions(self, change_processor):
        """Test that exceptions during processing are caught and logged properly"""

        # Create mock strategy that raises an exception
        create_strategy_mock = MagicMock()
        create_strategy_mock.process.side_effect = Topic.DoesNotExist(
            "Topic does not exist"
        )

        # Replace real strategies with mocks
        change_processor._strategies = {
            OperationType.CREATE: create_strategy_mock,
            OperationType.UPDATE: MagicMock(),
            OperationType.DELETE: MagicMock(),
        }

        # Create test change
        create_change = ChangeOperation(
            operation=OperationType.CREATE,
            entity_type=EntityType.TOPIC,
            entity_id="topic-123",
            data=MagicMock(),
        )

        changes = [create_change]

        # Process changes
        failed_changes = change_processor.process_changes(changes)

        # Assertions
        assert len(failed_changes) == 1
        assert failed_changes[0] == create_change
        create_strategy_mock.process.assert_called_once_with(create_change)

    def test_process_changes_mixed_results(self, change_processor):
        """Test with a mix of successful and failed changes"""

        # Create mock strategies with mixed results
        create_strategy_mock = MagicMock()
        create_strategy_mock.process.return_value = True
        update_strategy_mock = MagicMock()
        update_strategy_mock.process.return_value = False  # This one fails
        delete_strategy_mock = MagicMock()
        delete_strategy_mock.process.side_effect = SubTopic.DoesNotExist(
            "SubTopic does not exist"
        )  # This raises an exception

        # Replace real strategies with mocks
        change_processor._strategies = {
            OperationType.CREATE: create_strategy_mock,
            OperationType.UPDATE: update_strategy_mock,
            OperationType.DELETE: delete_strategy_mock,
        }

        # Create test changes
        create_change = ChangeOperation(
            operation=OperationType.CREATE,
            entity_type=EntityType.TOPIC,
            entity_id="topic-123",
            data=MagicMock(),
        )

        update_change = ChangeOperation(
            operation=OperationType.UPDATE,
            entity_type=EntityType.SUBTOPIC,
            entity_id="subtopic-456",
            data=MagicMock(),
        )

        delete_change = ChangeOperation(
            operation=OperationType.DELETE,
            entity_type=EntityType.SUBTOPIC,
            entity_id="nonexistent-subtopic",
            data=None,
        )

        changes = [create_change, update_change, delete_change]

        # Process changes
        failed_changes = change_processor.process_changes(changes)

        # Assertions
        assert len(failed_changes) == 2
        assert update_change in failed_changes
        assert delete_change in failed_changes
        create_strategy_mock.process.assert_called_once_with(create_change)
        update_strategy_mock.process.assert_called_once_with(update_change)
        delete_strategy_mock.process.assert_called_once_with(delete_change)

    @patch("course_sync.change_processor.log")
    def test_logging(self, mock_log, change_processor):
        """Test that processing logs appropriate information"""

        # Create mock strategy
        create_strategy_mock = MagicMock()
        create_strategy_mock.process.return_value = True

        # Replace real strategies with mocks
        change_processor._strategies = {
            OperationType.CREATE: create_strategy_mock,
        }

        # Create test change
        create_change = ChangeOperation(
            operation=OperationType.CREATE,
            entity_type=EntityType.TOPIC,
            entity_id="topic-123",
            data=MagicMock(),
        )

        changes = [create_change]

        # Process changes
        change_processor.process_changes(changes)

        # Assertions for logging
        mock_log.info.assert_any_call(
            "Processing: Operation=CREATE, Entity=TOPIC, ID=topic-123"
        )
