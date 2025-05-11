"""
course_sync.diff_engine
~~~~~~~~~~~~

Contains code that is used to compare and detect course changes from
edx course outline, implemented using Chain of Responsibility pattern
"""

import logging
from abc import ABC, abstractmethod
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

log = logging.getLogger(__name__)


class BaseDiffHandler(ABC):
    """Base handler for the diff chain of responsibility"""

    def __init__(self):
        self._next_handler = None
        log.debug("%s: Initialized", self.__class__.__name__)

    def set_next(self, handler):
        """Set the next handler in the chain"""
        log.debug(
            "%s: Setting next handler to %s",
            self.__class__.__name__,
            handler.__class__.__name__,
        )
        self._next_handler = handler
        return handler

    def process_next(
        self, old_course: Optional[EdxCourseOutline], new_course: EdxCourseOutline
    ) -> List[ChangeOperation]:
        """Process the next handler in the chain if it exists"""
        if self._next_handler:
            log.debug(
                "%s: Passing to next handler %s",
                self.__class__.__name__,
                self._next_handler.__class__.__name__,
            )
            return self._next_handler.handle(old_course, new_course)
        log.debug("%s: No next handler, ending chain", self.__class__.__name__)
        return []

    @abstractmethod
    def handle(
        self, old_course: Optional[EdxCourseOutline], new_course: EdxCourseOutline
    ) -> List[ChangeOperation]:
        """Handle the diff operation and decide whether to continue the chain"""
        pass


class CourseDiffHandler(BaseDiffHandler):
    """Course diff handler - handles course-level changes"""

    def handle(
        self, old_course: Optional[EdxCourseOutline], new_course: EdxCourseOutline
    ) -> List[ChangeOperation]:
        """
        Compare old and new course versions and generate change operations.
        If this is a completely new course, stops the chain.

        Args:
            old_course: Previous course outline version (None if this is a new course)
            new_course: Current course outline version

        Returns:
            List of change operations
        """
        log.debug(
            "CourseDiffHandler: Starting to handle course diff for course %s",
            new_course.course_id,
        )
        changes: List[ChangeOperation] = []

        # Handle case of a completely new course
        if old_course is None:
            log.info("New course detected: %s", new_course.course_id)
            log.debug(
                "CourseDiffHandler: No old course exists, creating new course operation"
            )
            return [
                ChangeOperation(
                    operation=OperationType.CREATE,
                    entity_type=EntityType.COURSE,
                    entity_id=new_course.course_id,
                    data=CourseChangeData(
                        name=new_course.title, course_outline=new_course
                    ),
                )
            ]

        # Check course-level changes
        log.debug("CourseDiffHandler: Comparing course properties")
        changes.extend(self._diff_course_properties(old_course, new_course))

        # Continue the chain
        log.debug("CourseDiffHandler: Finished course-level checks, continuing chain")
        changes.extend(self.process_next(old_course, new_course))

        log.debug("CourseDiffHandler: Completed handling with %d changes", len(changes))
        return changes

    def _diff_course_properties(
        self, old_course: EdxCourseOutline, new_course: EdxCourseOutline
    ) -> List[ChangeOperation]:
        """
        Compare course-level properties and generate change operations.

        Args:
            old_course: Previous course outline
            new_course: Current course outline

        Returns:
            List of change operations for course-level properties
        """
        changes = []

        # Currently only checking title changes
        log.debug(
            "CourseDiffHandler: Checking title change: old='%s', new='%s'",
            old_course.title,
            new_course.title,
        )
        title_changed = old_course.title != new_course.title

        if title_changed:
            log.info("Course title changed: %s", new_course.course_id)
            log.debug(
                "CourseDiffHandler: Adding UPDATE operation for course title change"
            )
            changes.append(
                ChangeOperation(
                    operation=OperationType.UPDATE,
                    entity_type=EntityType.COURSE,
                    entity_id=new_course.course_id,
                    data=CourseChangeData(
                        name=new_course.title, course_outline=new_course
                    ),
                )
            )

        return changes


class SubtopicDiffHandler(BaseDiffHandler):
    """
    Subtopic diff handler - runs before topic handler since we need to capture
    subtopic changes before potential topic deletions
    """

    def handle(
        self, old_course: Optional[EdxCourseOutline], new_course: EdxCourseOutline
    ) -> List[ChangeOperation]:
        """
        Compare subtopics between old and new course versions and generate change operations.

        Args:
            old_course: Previous course outline version (None if this is a new course)
            new_course: Current course outline version

        Returns:
            List of change operations
        """
        log.debug(
            "SubtopicDiffHandler: Starting to handle subtopic diff for course %s",
            new_course.course_id,
        )
        changes: List[ChangeOperation] = []
        if not old_course:
            log.debug(
                "SubtopicDiffHandler: No old course exists, skipping subtopic diff"
            )
            return self.process_next(old_course, new_course)

        # Diff subtopics
        log.debug("SubtopicDiffHandler: Comparing subtopics")
        changes.extend(self._diff_subtopics(old_course, new_course))

        # Continue the chain
        log.debug("SubtopicDiffHandler: Finished subtopic checks, continuing chain")
        changes.extend(self.process_next(old_course, new_course))

        log.debug(
            "SubtopicDiffHandler: Completed handling with %d changes", len(changes)
        )
        return changes

    def _diff_subtopics(
        self, old_course: EdxCourseOutline, new_course: EdxCourseOutline
    ) -> List[ChangeOperation]:
        """
        Compare subtopics across all topics and generate change operations.

        Args:
            old_course: Previous course outline
            new_course: Current course outline

        Returns:
            List of change operations for subtopics
        """
        changes = []

        # Get subtopic ID sets directly from the course structure
        old_subtopic_ids = old_course.structure.sub_topics
        new_subtopic_ids = new_course.structure.sub_topics

        log.debug(
            "SubtopicDiffHandler: Old subtopic IDs count: %d", len(old_subtopic_ids)
        )
        log.debug(
            "SubtopicDiffHandler: New subtopic IDs count: %d", len(new_subtopic_ids)
        )
        log.debug("SubtopicDiffHandler: Old subtopic IDs: %s", old_subtopic_ids)
        log.debug("SubtopicDiffHandler: New subtopic IDs: %s", new_subtopic_ids)

        # Handle deleted subtopics
        deleted_subtopics = old_subtopic_ids - new_subtopic_ids
        log.debug(
            "SubtopicDiffHandler: Found %d deleted subtopics", len(deleted_subtopics)
        )

        for subtopic_id in deleted_subtopics:
            log.info("Subtopic deleted: %s", subtopic_id)
            log.debug(
                "SubtopicDiffHandler: Adding DELETE operation for subtopic %s",
                subtopic_id,
            )
            changes.append(
                ChangeOperation(
                    operation=OperationType.DELETE,
                    entity_type=EntityType.SUBTOPIC,
                    entity_id=subtopic_id,
                    data=None,
                )
            )

        # Process created and updated subtopics by comparing across all topics
        log.debug("SubtopicDiffHandler: Checking for created and updated subtopics")
        for new_topic in new_course.topics:
            log.debug(
                "SubtopicDiffHandler: Checking subtopics in topic %s (%s)",
                new_topic.id,
                new_topic.name,
            )
            log.debug(
                "SubtopicDiffHandler: Topic contains %d subtopics",
                len(new_topic.sub_topics),
            )

            for new_subtopic in new_topic.sub_topics:
                log.debug(
                    "SubtopicDiffHandler: Processing subtopic %s (%s)",
                    new_subtopic.id,
                    new_subtopic.name,
                )

                # Find if this subtopic existed in the old course
                old_subtopic = None
                old_topic_id = None

                # First check if we can find it using the mapping
                if new_subtopic.id in old_course.structure.topic_to_sub_topic:
                    old_topic_id = old_course.structure.topic_to_sub_topic.get(
                        new_subtopic.id
                    )
                    log.debug(
                        "SubtopicDiffHandler: Found subtopic %s in mapping with parent topic %s",
                        new_subtopic.id,
                        old_topic_id,
                    )

                    if old_topic_id:
                        old_topic = old_course.get_topic_by_id(old_topic_id)
                        if old_topic:
                            log.debug(
                                "SubtopicDiffHandler: Found parent topic %s (%s)",
                                old_topic.id,
                                old_topic.name,
                            )
                            old_subtopic = next(
                                (
                                    sub
                                    for sub in old_topic.sub_topics
                                    if sub.id == new_subtopic.id
                                ),
                                None,
                            )
                            if old_subtopic:
                                log.debug(
                                    "SubtopicDiffHandler: Found subtopic %s in expected topic",
                                    new_subtopic.id,
                                )

                # If we couldn't find it in the expected topic, search all topics
                if not old_subtopic:
                    log.debug(
                        "SubtopicDiffHandler: Subtopic not found in expected topic, searching all topics"
                    )
                    for topic in old_course.topics:
                        old_subtopic = next(
                            (
                                sub
                                for sub in topic.sub_topics
                                if sub.id == new_subtopic.id
                            ),
                            None,
                        )
                        if old_subtopic:
                            old_topic_id = topic.id
                            log.debug(
                                "SubtopicDiffHandler: Found subtopic %s in topic %s",
                                new_subtopic.id,
                                old_topic_id,
                            )
                            break

                if old_subtopic is None or new_subtopic.id not in old_subtopic_ids:
                    # This is a new subtopic
                    log.info("New subtopic detected: %s", new_subtopic.id)
                    log.debug(
                        "SubtopicDiffHandler: Adding CREATE operation for new subtopic %s",
                        new_subtopic.id,
                    )
                    changes.append(
                        ChangeOperation(
                            operation=OperationType.CREATE,
                            entity_type=EntityType.SUBTOPIC,
                            entity_id=new_subtopic.id,
                            data=SubTopicChangeData(
                                name=new_subtopic.name, topic_id=new_subtopic.topic_id
                            ),
                        )
                    )
                else:
                    # Check for changes in existing subtopic
                    name_changed = old_subtopic.name != new_subtopic.name

                    log.debug(
                        "SubtopicDiffHandler: Checking changes for existing subtopic %s",
                        new_subtopic.id,
                    )
                    log.debug(
                        "SubtopicDiffHandler: Name changed: %s (old='%s', new='%s')",
                        name_changed,
                        old_subtopic.name,
                        new_subtopic.name,
                    )

                    if name_changed:
                        log.info("Subtopic updated: %s", new_subtopic.id)
                        log.debug(
                            "SubtopicDiffHandler: Adding UPDATE operation for subtopic %s",
                            new_subtopic.id,
                        )
                        changes.append(
                            ChangeOperation(
                                operation=OperationType.UPDATE,
                                entity_type=EntityType.SUBTOPIC,
                                entity_id=new_subtopic.id,
                                data=SubTopicChangeData(
                                    name=new_subtopic.name,
                                    topic_id=new_subtopic.topic_id,
                                ),
                            )
                        )

        log.debug(
            "SubtopicDiffHandler: Completed subtopic diff with %d changes", len(changes)
        )
        return changes


class TopicDiffHandler(BaseDiffHandler):
    """Topic diff handler - handles topic-level changes"""

    def handle(
        self, old_course: Optional[EdxCourseOutline], new_course: EdxCourseOutline
    ) -> List[ChangeOperation]:
        """
        Compare topics between old and new course versions and generate change operations.

        Args:
            old_course: Previous course outline version (None if this is a new course)
            new_course: Current course outline version

        Returns:
            List of change operations
        """
        log.debug(
            "TopicDiffHandler: Starting to handle topic diff for course %s",
            new_course.course_id,
        )
        changes: List[ChangeOperation] = []
        if not old_course:
            log.debug("TopicDiffHandler: No old course exists, skipping topic diff")
            return []

        # Diff topics
        log.debug("TopicDiffHandler: Comparing topics")
        changes.extend(self._diff_topics(old_course, new_course))

        # Continue the chain
        log.debug("TopicDiffHandler: Finished topic checks, continuing chain")
        changes.extend(self.process_next(old_course, new_course))

        log.debug("TopicDiffHandler: Completed handling with %d changes", len(changes))
        return changes

    def _diff_topics(
        self, old_course: EdxCourseOutline, new_course: EdxCourseOutline
    ) -> List[ChangeOperation]:
        """
        Compare topics between course versions and generate change operations.

        Args:
            old_course: Previous course outline
            new_course: Current course outline

        Returns:
            List of change operations for topics
        """
        changes = []

        # Get topic ID sets
        old_topic_ids = old_course.structure.topics
        new_topic_ids = new_course.structure.topics

        log.debug("TopicDiffHandler: Old topic IDs count: %d", len(old_topic_ids))
        log.debug("TopicDiffHandler: New topic IDs count: %d", len(new_topic_ids))
        log.debug("TopicDiffHandler: Old topic IDs: %s", old_topic_ids)
        log.debug("TopicDiffHandler: New topic IDs: %s", new_topic_ids)

        # Handle deleted topics
        log.debug("TopicDiffHandler: Checking for deleted topics")
        changes.extend(self._handle_deleted_topics(old_topic_ids, new_topic_ids))

        # Handle created or updated topics
        log.debug("TopicDiffHandler: Checking for created or updated topics")
        changes.extend(self._handle_created_or_updated_topics(old_course, new_course))

        return changes

    def _handle_deleted_topics(
        self, old_topic_ids: set, new_topic_ids: set
    ) -> List[ChangeOperation]:
        """
        Process topics that have been deleted.

        Args:
            old_topic_ids: Set of topic IDs from the old course
            new_topic_ids: Set of topic IDs from the new course

        Returns:
            List of DELETE change operations
        """
        changes = []

        # Find topics that exist in old but not in new
        deleted_topics = old_topic_ids - new_topic_ids
        log.debug("TopicDiffHandler: Found %d deleted topics", len(deleted_topics))

        for topic_id in deleted_topics:
            log.info("Topic deleted: %s", topic_id)
            log.debug(
                "TopicDiffHandler: Adding DELETE operation for topic %s", topic_id
            )
            changes.append(
                ChangeOperation(
                    operation=OperationType.DELETE,
                    entity_type=EntityType.TOPIC,
                    entity_id=topic_id,
                    data=None,
                )
            )

        return changes

    def _handle_created_or_updated_topics(
        self, old_course: EdxCourseOutline, new_course: EdxCourseOutline
    ) -> List[ChangeOperation]:
        """
        Process topics that have been created or updated.

        Args:
            old_course: The original course
            new_course: The new course

        Returns:
            List of CREATE and UPDATE change operations
        """
        changes = []

        log.debug(
            "TopicDiffHandler: Checking %d topics in new course", len(new_course.topics)
        )
        for new_topic in new_course.topics:
            log.debug(
                "TopicDiffHandler: Checking topic %s (%s)", new_topic.id, new_topic.name
            )
            old_topic = next(
                (topic for topic in old_course.topics if topic.id == new_topic.id), None
            )

            if old_topic is None:
                # Handle newly created topics
                log.debug(
                    "TopicDiffHandler: Topic %s not found in old course", new_topic.id
                )
                changes.append(self._handle_created_topic(new_topic))
            else:
                # Handle potentially updated topics
                log.debug(
                    "TopicDiffHandler: Found existing topic %s, checking for updates",
                    new_topic.id,
                )
                change = self._handle_updated_topic(old_topic, new_topic)
                if change:
                    changes.append(change)

        return changes

    def _handle_created_topic(self, new_topic) -> ChangeOperation:
        """
        Process a newly created topic.

        Args:
            new_topic: The new topic that was created

        Returns:
            CREATE change operation
        """
        log.info("New topic detected: %s", new_topic.id)
        log.debug(
            "TopicDiffHandler: Adding CREATE operation for new topic %s", new_topic.id
        )
        return ChangeOperation(
            operation=OperationType.CREATE,
            entity_type=EntityType.TOPIC,
            entity_id=new_topic.id,
            data=new_topic,
        )

    def _handle_updated_topic(self, old_topic, new_topic) -> Optional[ChangeOperation]:
        """
        Check if a topic has been updated and create the appropriate change operation.

        Args:
            old_topic: The original topic
            new_topic: The potentially modified topic

        Returns:
            UPDATE change operation if modified, None otherwise
        """
        log.debug(
            "TopicDiffHandler: Comparing topic properties: old name='%s', new name='%s'",
            old_topic.name,
            new_topic.name,
        )
        name_changed = old_topic.name != new_topic.name

        if name_changed:
            log.info("Topic name changed: %s", new_topic.id)
            log.debug(
                "TopicDiffHandler: Adding UPDATE operation for topic name change %s",
                new_topic.id,
            )
            return ChangeOperation(
                operation=OperationType.UPDATE,
                entity_type=EntityType.TOPIC,
                entity_id=new_topic.id,
                data=new_topic,
            )

        log.debug("TopicDiffHandler: No changes detected for topic %s", new_topic.id)
        return None


def validate_handlers(func):
    @wraps(func)
    def wrapper(
        self,
        course_handler=CourseDiffHandler,
        subtopic_handler=SubtopicDiffHandler,
        topic_handler=TopicDiffHandler,
        *args,
        **kwargs,
    ):
        log.debug("DiffEngine: Validating handler classes")
        # Validate that all handlers are subclasses of BaseDiffHandler
        for handler_class, handler_name in [
            (course_handler, "Course handler"),
            (subtopic_handler, "Subtopic handler"),
            (topic_handler, "Topic handler"),
        ]:
            log.debug(
                "DiffEngine: Validating %s (%s)", handler_name, handler_class.__name__
            )
            if not issubclass(handler_class, BaseDiffHandler):
                log.error(
                    "DiffEngine: Invalid handler %s: %s",
                    handler_name,
                    handler_class.__name__,
                )
                raise TypeError(
                    f"{handler_name} is invalid: {handler_class.__name__}. Must be a subclass of BaseDiffHandler"
                )

        return func(
            self, course_handler, subtopic_handler, topic_handler, *args, **kwargs
        )

    return wrapper


class DiffEngine:
    """
    Detect differences between course outline versions and generate change operations.
    Implements Chain of Responsibility pattern.
    """

    def __init__(self):
        log.debug("DiffEngine: Initializing")
        # Initialize the chain
        self.chain = self._create_handler_chain()
        log.debug("DiffEngine: Handler chain created")

    @validate_handlers
    def _create_handler_chain(
        self,
        course_handler=CourseDiffHandler,
        subtopic_handler=SubtopicDiffHandler,
        topic_handler=TopicDiffHandler,
    ) -> BaseDiffHandler:
        """Create and connect the chain of handlers"""
        log.debug("DiffEngine: Creating handler chain")
        # Order: Course -> Subtopic -> Topic
        course_handler = course_handler()
        subtopic_handler = subtopic_handler()
        topic_handler = topic_handler()

        log.debug("DiffEngine: Instantiated handlers")

        # Link the chain
        log.debug("DiffEngine: Linking handler chain")
        course_handler.set_next(topic_handler)
        topic_handler.set_next(subtopic_handler)

        log.debug("DiffEngine: Handler chain linked: Course -> Subtopic -> Topic")
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
        log.info("Starting diff process for course: %s", new_course.course_id)
        log.debug("DiffEngine: Old course exists: %s", old_course is not None)
        if old_course:
            log.debug("DiffEngine: Old course title: %s", old_course.title)
            log.debug("DiffEngine: Old course topics count: %d", len(old_course.topics))
            log.debug(
                "DiffEngine: Old course subtopics count: %d",
                old_course.structure.sub_topic_count,
            )

        log.debug("DiffEngine: New course title: %s", new_course.title)
        log.debug("DiffEngine: New course topics count: %d", len(new_course.topics))
        log.debug(
            "DiffEngine: New course subtopics count: %d",
            new_course.structure.sub_topic_count,
        )

        changes = self.chain.handle(old_course, new_course)

        log.info("Diff process completed with %d change operations", len(changes))
        for i, change in enumerate(changes):
            log.debug(
                "DiffEngine: Change %d: %s %s %s",
                i + 1,
                change.operation.value,
                change.entity_type.value,
                change.entity_id,
            )

        return changes
