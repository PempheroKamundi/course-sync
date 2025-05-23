"""
course_sync.change_processor
~~~~~~~~~~~~

Contains code that processes change operations generated by the diff engine
using the Strategy pattern with Command elements.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Union

from django.db import OperationalError, transaction

from course_sync.data_types import (
    ChangeOperation,
    CourseChangeData,
    EntityType,
    OperationType,
    SubTopicChangeData,
)
from course_ware.models import AcademicClass, Course, ExaminationLevel, SubTopic, Topic
from exceptions import InvalidChangeDataTypeError

log = logging.getLogger(__name__)


class ChangeStrategy(ABC):
    """Base strategy for processing changes"""

    @abstractmethod
    def process(self, change: ChangeOperation) -> bool:
        """
        Process a change operation

        Args:
            change: The change operation to process

        Returns:
            bool: True if processing was successful, False otherwise
        """
        raise NotImplementedError("Abstract method not implemented")


class CreateStrategy(ChangeStrategy):
    """Strategy for processing CREATE operations"""

    def __init__(
        self,
        course: Course,
        examination_level: ExaminationLevel,
        academic_class: AcademicClass,
    ):
        self._course = course
        self._examination_level = examination_level
        self._academic_class = academic_class

    def process(self, change: ChangeOperation) -> bool:
        """Process a CREATE operation"""
        entity_type = change.entity_type
        entity_id = change.entity_id
        data = change.data

        log.info("Creating %s with ID %s ", entity_type.name, entity_id)

        if entity_type == EntityType.TOPIC:
            return self._create_topic(entity_id, data)
        if entity_type == EntityType.SUBTOPIC:
            return self._create_subtopic(entity_id, data)

        log.error("Unsupported entity type for CREATE: %s", entity_type)
        return False

    def _create_topic(
        self, block_id: str, topic_data: SubTopicChangeData | CourseChangeData
    ) -> bool:
        """Implement topic creation logic"""
        log.info("Creating topic: %s", block_id)
        Topic.objects.get_or_create(
            block_id=block_id,
            defaults={
                "name": topic_data.name,
                "examination_level": self._examination_level,
                "academic_class": self._academic_class,
                "course": self._course,
            },
        )
        return True

    def _create_subtopic(
        self, block_id: str, subtopic_data: Union[SubTopicChangeData, CourseChangeData]
    ) -> bool:
        """Implement subtopic creation logic"""
        log.info("Creating subtopic: %s", block_id)

        if not isinstance(subtopic_data, SubTopicChangeData):
            raise InvalidChangeDataTypeError(
                expected_type="SubTopicChangeData",
                actual_type=type(subtopic_data).__name__,
                operation="creating a subtopic",
            )

        topic = Topic.objects.get(block_id=subtopic_data.topic_id)

        SubTopic.objects.get_or_create(
            block_id=block_id,
            defaults={
                "name": subtopic_data.name,
                "topic": topic,
            },
        )
        return True


class UpdateStrategy(ChangeStrategy):
    """Strategy for processing UPDATE operations"""

    def process(self, change: ChangeOperation) -> bool:
        """Process an UPDATE operation"""
        entity_type = change.entity_type
        entity_id = change.entity_id
        data = change.data

        log.info(f"Updating {entity_type.name} with ID {entity_id}")

        if entity_type == EntityType.COURSE:
            return self._update_course(entity_id, data)
        elif entity_type == EntityType.TOPIC:
            return self._update_topic(entity_id, data)
        elif entity_type == EntityType.SUBTOPIC:
            return self._update_subtopic(entity_id, data)

        log.error(f"Unsupported entity type for UPDATE: {entity_type}")
        return False

    def _update_course(
        self, course_id: str, course_data: SubTopicChangeData | CourseChangeData
    ):
        """Updates course data"""
        log.info("Updating course: %s", course_id)

        if not isinstance(course_data, CourseChangeData):
            raise InvalidChangeDataTypeError(
                expected_type="CourseChangeData",
                actual_type=type(course_data).__name__,
                operation="updating a course",
            )

        course = Course.objects.get(id=course_id)
        course.name = course_data.name
        course.course_outline = course_data.course_outline
        course.save()
        return True

    def _update_topic(
        self, block_id: str, topic_data: SubTopicChangeData | CourseChangeData
    ):
        """Updates topic data"""
        log.info(f"Updating topic: {block_id}")

        topic = Topic.objects.get(block_id=block_id)
        topic.name = topic_data.name
        topic.save()
        return True

    def _update_subtopic(
        self, block_id: str, subtopic_data: SubTopicChangeData | CourseChangeData
    ):
        """Updates subtopic data"""
        log.info(f"Updating subtopic: {block_id}")

        subtopic = SubTopic.objects.get(block_id=block_id)
        subtopic.name = subtopic_data.name
        subtopic.save()

        return True


class DeleteStrategy(ChangeStrategy):
    """Strategy for processing DELETE operations"""

    def process(self, change: ChangeOperation) -> bool:
        """Process a DELETE operation"""
        entity_type = change.entity_type
        entity_id = change.entity_id

        log.info(f"Deleting {entity_type.name} with ID {entity_id}")

        if entity_type == EntityType.COURSE:
            return self._delete_course(entity_id)
        elif entity_type == EntityType.TOPIC:
            return self._delete_topic(entity_id)
        elif entity_type == EntityType.SUBTOPIC:
            return self._delete_subtopic(entity_id)
        else:
            log.error(f"Unsupported entity type for DELETE: {entity_type}")
            return False

    def _delete_course(self, course_id: str) -> bool:
        """Deletion of a course"""
        log.info(f"Deleting course: {course_id}")
        course = Course.objects.get(id=course_id)
        course.delete()
        return True

    def _delete_topic(self, block_id: str) -> bool:
        """deletion of a topic"""
        log.info(f"Deleting topic: {block_id}")
        topic = Topic.objects.get(block_id=block_id)
        topic.delete()

        return True

    def _delete_subtopic(self, block_id: str) -> bool:
        """Implement subtopic deletion logic"""
        log.info(f"Deleting subtopic: {block_id}")
        subtopic = SubTopic.objects.get(block_id=block_id)
        subtopic.delete()
        return True


class ChangeProcessor:
    """
    Processes change operations using appropriate strategies based on operation type.
    Acts as an adapter between the diff engine and the processing logic.
    """

    def __init__(
        self,
        course: Course,
        examination_level: ExaminationLevel,
        academic_class: AcademicClass,
    ):
        # Map operation types to their corresponding strategy
        self._strategies: Dict[OperationType, ChangeStrategy] = {
            OperationType.CREATE: CreateStrategy(
                course=course,
                examination_level=examination_level,
                academic_class=academic_class,
            ),
            OperationType.UPDATE: UpdateStrategy(),
            OperationType.DELETE: DeleteStrategy(),
        }

    @transaction.atomic
    def process_changes(self, changes: List[ChangeOperation]) -> List[ChangeOperation]:
        """
        Process a list of change operations

        Args:
            changes: List of change operations to process

        Returns:
            List of failed change operations
        """
        failed_changes = []

        for change in changes:
            log.info(
                f"Processing: Operation={change.operation.name}, Entity={change.entity_type.name}, ID={change.entity_id}"
            )

            strategy = self._strategies.get(change.operation)
            try:
                if strategy:
                    success = strategy.process(change)
                    if not success:
                        log.error(
                            f"Failed to process change: {change.operation.name} {change.entity_type.name} {change.entity_id}",
                            exc_info=True,
                        )
                        failed_changes.append(change)
                else:
                    log.error(
                        f"No strategy found for operation type: {change.operation}",
                        exc_info=True,
                    )
                    failed_changes.append(change)

            except (Topic.DoesNotExist, Course.DoesNotExist, SubTopic.DoesNotExist):
                log.error(
                    f"No strategy found for operation type: {change.operation}",
                    exc_info=True,
                )
                failed_changes.append(change)

            except OperationalError:
                log.warning(
                    "Database is probably locked. Need to fix this by hashing event types from webhooks"
                )

        return failed_changes
