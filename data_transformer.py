"""
course_sync.data_transformer
~~~~~~~~~~~~~~~

Contains code that transforms raw Edx course data
into our domain model objects for processing
"""

import logging
from typing import Dict, List, Optional, Tuple

from course_sync.data_types import CourseStructure, EdxCourseOutline, SubTopics, Topic

logger = logging.getLogger(__name__)


class EdxDataTransformer:
    """Responsible for transforming edX course data into our domain model"""

    @staticmethod
    def _extract_course_children(structure: Dict) -> List[Dict]:
        """Extract course children with proper error handling"""
        try:
            return structure.get("course_structure", {}).get("child_info", {}).get("children", [])
        except AttributeError:
            logger.warning("Invalid course structure format")
            return []

    @staticmethod
    def _create_sub_topic(sub_topic_data: Dict, topic_id: str) -> Optional[SubTopics]:
        """Create a SubTopics object from data with validation"""
        sub_topic_id = sub_topic_data.get("id")
        if not sub_topic_id:
            return None

        return SubTopics(
            id=sub_topic_id,
            name=sub_topic_data.get("display_name", ""),
            topic_id=topic_id,
        )

    @staticmethod
    def _process_single_topic(topic_data: Dict) -> Tuple[Optional[str], Optional[Topic], List[Tuple[str, str]]]:
        """
        Process a single topic and return topic_id, Topic object, and sub_topic relationships

        Returns:
            Tuple of (topic_id, Topic object, [(sub_topic_id, topic_id), ...])
        """
        topic_id = topic_data.get("id")
        if not topic_id:
            return None, None, []

        sub_topics = []
        sub_topic_relationships = []

        # Process sub_topics if they exist
        if topic_data.get("has_children"):
            for sub_topic_data in topic_data.get("child_info", {}).get("children", []):
                sub_topic = EdxDataTransformer._create_sub_topic(sub_topic_data, topic_id)
                if sub_topic:
                    sub_topics.append(sub_topic)
                    sub_topic_relationships.append((sub_topic.id, topic_id))

        topic = Topic(
            id=topic_id,
            name=topic_data.get("display_name", ""),
            sub_topics=sub_topics,
        )

        return topic_id, topic, sub_topic_relationships

    @staticmethod
    def _transform_all_data(structure: Dict) -> Tuple[CourseStructure, List[Topic]]:
        """
        Single-pass transformation of all course data

        This eliminates redundant traversals when both structure and topics are needed
        """
        topics_set = set()
        sub_topics_set = set()
        topic_to_sub_topic = {}
        topics_list = []

        course_children = EdxDataTransformer._extract_course_children(structure)

        for topic_data in course_children:
            topic_id, topic, sub_topic_relationships = EdxDataTransformer._process_single_topic(topic_data)

            if topic_id and topic:
                topics_set.add(topic_id)
                topics_list.append(topic)

                # Process sub_topic relationships
                for sub_topic_id, parent_topic_id in sub_topic_relationships:
                    sub_topics_set.add(sub_topic_id)
                    topic_to_sub_topic[sub_topic_id] = parent_topic_id

        course_structure = CourseStructure(topics_set, sub_topics_set, topic_to_sub_topic)
        return course_structure, topics_list

    @staticmethod
    def transform_structure(structure: Dict) -> CourseStructure:
        """
        Transform edX course data into CourseStructure domain model

        Args:
            structure (Dict): edX course structure
        Returns:
            CourseStructure: transformed edX course structure
        """
        course_structure, _ = EdxDataTransformer._transform_all_data(structure)
        return course_structure

    @staticmethod
    def transform_topics(structure: Dict) -> List[Topic]:
        """
        Transform edX course data into Topic domain models

        Args:
            structure (Dict): edX course structure
        Returns:
            List[Topic]: list of transformed topics
        """
        _, topics = EdxDataTransformer._transform_all_data(structure)
        return topics

    @staticmethod
    def transform_to_course_outline(
            structure: Dict, course_id: str, title: str
    ) -> EdxCourseOutline:
        """
        Transform raw edX data into a complete EdxCourseOutline

        This method is most efficient as it performs single-pass transformation

        Args:
            structure (Dict): edX course structure
            course_id (str): course identifier
            title (str): course title

        Returns:
            EdxCourseOutline: complete course outline with structure and topics
        """
        course_structure, topics = EdxDataTransformer._transform_all_data(structure)

        return EdxCourseOutline(
            course_id=course_id,
            title=title,
            structure=course_structure,
            topics=topics
        )