"""
course_sync.diff_engine
~~~~~~~~~~~~

Contains code that is used to compare and detect course changes from
edx course outline, implemented using Chain of Responsibility pattern
"""

import logging
from functools import wraps
from typing import List, Optional

from course_sync.data_types import (
    ChangeOperation,
    CourseChangeData,
    EdxCourseOutline,
    EntityType,
    OperationType,
    SubTopicChangeData,
)

logger = logging.getLogger(__name__)



class DiffEngine:
    """
    Detect differences between course outline versions and generate change operations.
    Implements Chain of Responsibility pattern.
    """

    def __init__(self):
        logger.debug("DiffEngine: Initializing")
        # Initialize the chain
        self.chain = self._create_handler_chain()
        logger.debug("DiffEngine: Handler chain created")

    @validate_handlers
    def _create_handler_chain(
        self,
        course_handler=CourseDiffHandler,
        subtopic_handler=SubtopicDiffHandler,
        topic_handler=TopicDiffHandler,
    ) -> BaseDiffHandler:
        """Create and connect the chain of handlers"""
        logger.debug("DiffEngine: Creating handler chain")
        # Order: Course -> Topic -> Subtopic
        course_handler = course_handler()
        subtopic_handler = subtopic_handler()
        topic_handler = topic_handler()

        logger.debug("DiffEngine: Instantiated handlers")

        # Link the chain
        logger.debug("DiffEngine: Linking handler chain")
        course_handler.set_next(topic_handler)
        topic_handler.set_next(subtopic_handler)

        logger.debug("DiffEngine: Handler chain linked: Course -> Subtopic -> Topic")
        return course_handler

    def diff(
        self, old_course: Optional[EdxCourseOutline], new_course: EdxCourseOutline
    ) -> List[ChangeOperation]:
        """
        Compare old and new course versions and generate change operations.
        Starts the chain of responsibility.

        Args:
            old_course: Previous course outline version (None if this is a new course)
            new_course: Current course outline version

        Returns:
            List of change operations to transform old_course into new_course
        """
        logger.info("Starting diff process for course: %s", new_course.course_id)
        logger.debug("DiffEngine: Old course exists: %s", old_course is not None)
        if old_course:
            logger.debug("DiffEngine: Old course title: %s", old_course.title)
            logger.debug("DiffEngine: Old course topics count: %d", len(old_course.topics))
            logger.debug(
                "DiffEngine: Old course subtopics count: %d",
                old_course.structure.sub_topic_count,
            )

        logger.debug("DiffEngine: New course title: %s", new_course.title)
        logger.debug("DiffEngine: New course topics count: %d", len(new_course.topics))
        logger.debug(
            "DiffEngine: New course subtopics count: %d",
            new_course.structure.sub_topic_count,
        )

        changes = self.chain.handle(old_course, new_course)

        logger.info("Diff process completed with %d change operations", len(changes))
        for i, change in enumerate(changes):
            logger.debug(
                "DiffEngine: Change %d: %s %s %s",
                i + 1,
                change.operation.value,
                change.entity_type.value,
                change.entity_id,
            )

        return changes
