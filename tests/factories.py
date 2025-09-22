from unittest.mock import MagicMock

from factory import Factory, Faker, LazyAttribute, List, Sequence
from factory.fuzzy import FuzzyText

from course_sync.data_types import CourseStructure, EdxCourseOutline, SubTopics, Topic
from course_sync.diff_engine import BaseDiffHandler


class SubTopicFactory(Factory):
    class Meta:
        model = SubTopics

    id = Sequence(lambda n: f"subtopic-{n}")
    name = Sequence(lambda n: f"Subtopic {n}")
    topic_id = None  # Will be set by parent topic


class TopicFactory(Factory):
    class Meta:
        model = Topic

    id = Sequence(lambda n: f"topic-{n}")
    name = Sequence(lambda n: f"Topic {n}")
    sub_topics = List([])


class SubTopicDataFactory(Factory):
    """Factory for generating subtopic data dictionaries"""

    class Meta:
        model = dict

    id = FuzzyText(prefix="subtopic-")
    display_name = Faker("sentence", nb_words=3)
    has_children = False


class TopicDataFactory(Factory):
    """Factory for generating topic data dictionaries"""

    class Meta:
        model = dict

    id = FuzzyText(prefix="topic-")
    display_name = Faker("sentence", nb_words=4)
    has_children = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        children = []
        for _ in range(3):
            children.append(SubTopicDataFactory())

        obj["child_info"] = {"children": children}
        return obj


class CourseStructureFactory(Factory):
    """Factory for generating course structure data dictionaries"""

    class Meta:
        model = dict

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        topics = []
        for _ in range(4):  # Create 4 topics
            topics.append(TopicDataFactory())

        obj["course_structure"] = {"child_info": {"children": topics}}
        return obj


class CourseStructureFactoryV2(Factory):
    class Meta:
        model = CourseStructure

    topics = LazyAttribute(lambda o: set())
    sub_topics = LazyAttribute(lambda o: set())
    topic_to_sub_topic = LazyAttribute(lambda o: set())


class EdxCourseOutlineFactory(Factory):
    class Meta:
        model = EdxCourseOutline

    course_id = Sequence(lambda n: f"course-v1:TestOrg+Test{n}+2023")
    title = Sequence(lambda n: f"Test Course {n}")
    topics = List([])
    structure = None

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        topics = kwargs.pop("topics", [])

        course = model_class(*args, **kwargs)

        if isinstance(topics, int):
            course.topics = [TopicFactory() for _ in range(topics)]
        else:
            course.topics = topics

        topic_ids = {topic.id for topic in course.topics}
        course.structure = CourseStructureFactoryV2(topics=topic_ids)

        return course


class MockHandlerFactory(Factory):
    class Meta:
        model = BaseDiffHandler
        abstract = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        mock_handler = MagicMock(spec=model_class)
        mock_handler.handle.return_value = kwargs.pop("handle_return", [])
        mock_handler.set_next.side_effect = lambda handler: handler
        return mock_handler
