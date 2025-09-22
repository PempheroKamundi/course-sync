"""
course_sync.data_types
~~~~~~~~~~~~~~~~

Holds data types for the course sync module
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Union


@dataclass
class SubTopics:
    """Represents a sub_topic within a topic"""

    id: str
    name: str
    topic_id: str


@dataclass
class Topic:
    """Represents a topic in the course"""

    id: str
    name: str
    sub_topics: List[SubTopics]


@dataclass
class CourseStructure:
    """Represents the overall structure of an edX course"""

    topics: Set[str]  # Set of topic IDs
    sub_topics: Set[str]  # Set of sub_topics IDs
    topic_to_sub_topic: Dict[str, str]  # Maps sub_topic IDs to their parent topic IDs

    @property
    def topics_count(self) -> int:
        """Returns the number of topics in the course"""
        return len(self.topics)

    @property
    def sub_topic_count(self) -> int:
        """Returns the number of sub_topics in the course"""
        return len(self.sub_topics)


@dataclass
class EdxCourseOutline:
    """Top-level representation of the complete edX course outline"""

    course_id: str
    title: str
    structure: CourseStructure
    topics: List[Topic] = field(default_factory=list)

    def get_topic_by_id(self, topic_id: str) -> Optional[Topic]:
        """Retrieves a specific topic by its ID"""
        for topic in self.topics:
            if topic.id == topic_id:
                return topic
        return None

    def get_sub_topics_by_topic_id(self, topic_id: str) -> List[SubTopics]:
        """Retrieves all sub_topics for a specific topic_id"""
        topic = self.get_topic_by_id(topic_id)
        if not topic:
            return []
        return [
            SubTopics(id=obj.id, name=obj.name, topic_id=obj.topic_id)
            for obj in topic.sub_topics
            if obj.id
        ]


class OperationType(Enum):
    """Operation types"""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class EntityType(Enum):
    """Entity types"""

    COURSE = "course"
    TOPIC = "topic"
    SUBTOPIC = "subtopic"


@dataclass
class DefaultChangeData:
    """
    Default change data that is expected in all change operation"""

    name: str


@dataclass
class SubTopicChangeData(DefaultChangeData):
    """Subtopic data that is expected in a change operation"""

    topic_id: str


@dataclass
class CourseChangeData(DefaultChangeData):
    """Course data that is expected in a change operation"""

    course_outline: EdxCourseOutline


@dataclass
class ChangeOperation:
    """Operation Data type"""

    operation: OperationType
    entity_type: EntityType
    entity_id: str
    data: Union[CourseChangeData, SubTopicChangeData | Topic | None]
