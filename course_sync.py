"""
course_sync.service
~~~~~~~~~~~~

Contains the CourseSyncService that orchestrates the interaction between
the DiffEngine and ChangeProcessor to synchronize course content.
"""

import logging
from collections import namedtuple
from typing import List, Optional

from course_sync.change_processor import ChangeProcessor
from course_sync.data_transformer import EdxDataTransformer
from course_sync.data_types import ChangeOperation, EdxCourseOutline
from course_sync.diff_engine import DiffEngine
from course_ware.models import AcademicClass, Course, ExaminationLevel

logger = logging.getLogger(__name__)

ChangeResult = namedtuple("ChangeResult", ["num_failed", "num_success"])


class CourseSyncService:
    """
    Service that orchestrates the course synchronization process.
    Coordinates the detection of changes using DiffEngine and
    the application of those changes using ChangeProcessor.
    """

    def __init__(self, diff_engine: DiffEngine):
        self.diff_engine = diff_engine

    def sync_course(
        self,
        new_course_outline: EdxCourseOutline,
        course: Course,
        examination_level: ExaminationLevel,
        academic_class: AcademicClass,
    ) -> ChangeResult:
        """
        Synchronizes a course by detecting changes between the existing course
        outline and the new course outline, then applying those changes.

        Args:
            new_course_outline: The new course outline from edX
            course: The existing course in the database
            examination_level: The examination level for the course
            academic_class: The academic class for the course

        Returns:
            Tuple containing (number of successful changes, number of failed changes)
        """
        logger.info(
            "Starting course sync for course ID: %s, examination level: %s, academic class: %s",
            course.id,
            examination_level.name,
            academic_class.name,
        )

        old_course_outline = EdxDataTransformer.transform_to_course_outline(
            structure=course.course_outline,
            course_id=course.course_key,
            title=course.name,
        )

        changes = self._detect_changes(old_course_outline, new_course_outline)

        if not changes:
            logger.info("No changes detected for course ID: %s", course.id)
            return ChangeResult(num_failed=0, num_success=0)

        logger.info("Detected %d changes for course ID: %s", len(changes), course.id)

        failed_changes = self._process_changes(
            changes, course, examination_level, academic_class
        )

        successful_changes = len(changes) - len(failed_changes)

        logger.info(
            "Course sync completed for course ID: %s - %d changes applied, %d changes failed",
            course.id,
            successful_changes,
            len(failed_changes),
        )

        return ChangeResult(
            num_failed=len(failed_changes), num_success=successful_changes
        )

    def _detect_changes(
        self,
        old_course_outline: Optional[EdxCourseOutline],
        new_course_outline: EdxCourseOutline,
    ) -> List[ChangeOperation]:
        """
        Detects changes between the old and new course outlines.

        Args:
            old_course_outline: The existing course outline (can be None)
            new_course_outline: The new course outline

        Returns:
            List of change operations
        """
        logger.info("Detecting changes for course ID: %s", new_course_outline.course_id)
        return self.diff_engine.diff(old_course_outline, new_course_outline)

    def _process_changes(
        self,
        changes: List[ChangeOperation],
        course: Course,
        examination_level: ExaminationLevel,
        academic_class: AcademicClass,
    ) -> List[ChangeOperation]:
        """
        Processes the detected changes using the ChangeProcessor.

        Args:
            changes: List of change operations
            course: The course being synchronized
            examination_level: The examination level for the course
            academic_class: The academic class for the course

        Returns:
            List of failed change operations
        """
        logger.info("Processing %d changes for course ID: %s", len(changes), course.id)

        change_processor = ChangeProcessor(
            course=course,
            examination_level=examination_level,
            academic_class=academic_class,
        )

        return change_processor.process_changes(changes)

    @classmethod
    def create_service(cls):
        return CourseSyncService(diff_engine=DiffEngine())
