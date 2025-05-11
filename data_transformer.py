"""
course_sync.data_transformer
~~~~~~~~~~~~~~~

Contains code that transforms raw Edx course data
into our domain model objects for processing
"""

import logging
from typing import Dict, List

from course_sync.data_types import CourseStructure, EdxCourseOutline, SubTopics, Topic

log = logging.getLogger(__name__)


class EdxDataTransformer:
    """Responsible for transforming edX course data into our domain model"""

    @staticmethod
    def transform_structure(structure: Dict) -> CourseStructure:
        """
        Main function for transforming edX course data into our domain model

        Args:
           structure (Dict): edX course structure
        Returns:
           course structure(CourseStructure): transformed edX course structure
        """
        topics_set = set()
        sub_topics_set = set()
        topic_to_sub_topic = {}

        course_data = structure.get("course_structure", {})
        for topic in course_data.get("child_info", {}).get("children", []):
            topic_id = topic.get("id")
            if topic_id:
                topics_set.add(topic_id)

            if topic.get("has_children"):
                for sub_topic in topic.get("child_info", {}).get("children", []):
                    sub_topic_id = sub_topic.get("id")
                    if sub_topic_id:
                        sub_topics_set.add(sub_topic_id)
                        topic_to_sub_topic[sub_topic_id] = topic_id

        return CourseStructure(topics_set, sub_topics_set, topic_to_sub_topic)

    @staticmethod
    def transform_topics(structure: Dict) -> List[Topic]:
        topics = []
        course_data = structure.get("course_structure", {})

        for topic_data in course_data.get("child_info", {}).get("children", []):
            if topic_data.get("id"):
                # Transform sub_topics for this topic
                sub_topics = []
                for sub_topic_data in topic_data.get("child_info", {}).get(
                    "children", []
                ):
                    if sub_topic_data.get("id"):
                        sub_topics.append(
                            SubTopics(
                                id=sub_topic_data["id"],
                                name=sub_topic_data["display_name"],
                                topic_id=topic_data["id"],
                            )
                        )

                # Create the Topic object
                topics.append(
                    Topic(
                        id=topic_data["id"],
                        name=topic_data["display_name"],
                        sub_topics=sub_topics,
                    )
                )
        return topics

    @staticmethod
    def transform_to_course_outline(
        structure: Dict, course_id: str, title: str
    ) -> EdxCourseOutline:
        """Transforms the raw edX data into a complete EdxCourseOutline"""
        course_structure = EdxDataTransformer.transform_structure(structure)
        topics = EdxDataTransformer.transform_topics(structure)

        return EdxCourseOutline(
            course_id=course_id, title=title, structure=course_structure, topics=topics
        )
