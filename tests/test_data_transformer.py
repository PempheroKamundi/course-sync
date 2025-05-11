"""
Tests for ai_core.course_sync.data_transformer
"""

from course_sync.data_transformer import EdxDataTransformer
from course_sync.data_types import CourseStructure, EdxCourseOutline, Topic
from course_sync.tests.factories import CourseStructureFactory


class TestEdxDataTransformer:
    """Test cases for EdxDataTransformer class"""

    def test_transform_structure_empty_data(self):
        """Test transforming empty structure data"""
        empty_structure = {}
        result = EdxDataTransformer.transform_structure(empty_structure)

        assert isinstance(result, CourseStructure)
        assert len(result.topics) == 0
        assert len(result.sub_topics) == 0
        assert len(result.topic_to_sub_topic) == 0

    def test_transform_structure_with_data(self):
        """Test transforming structure with actual data"""
        # Create test data with known IDs

        structure = {
            "course_release_date": "Oct 29, 2018 at 01:30 UTC",
            "course_structure": {
                "id": "block-v1:VirtuEducate+JCE+101+type@course+block@course",
                "display_name": "Chemistry Basics: Form 1",
                "category": "course",
                "has_children": True,
                "unit_level_discussions": True,
                "edited_on": "Apr 17, 2025 at 14:21 UTC",
                "published": True,
                "published_on": "Apr 17, 2025 at 14:21 UTC",
                "studio_url": "/course/course-v1:VirtuEducate+JCE+101",
                "lms_url": "https://local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@course+block@course",
                "embed_lms_url": "https://local.edly.io/xblock/block-v1:VirtuEducate+JCE+101+type@course+block@course",
                "released_to_students": True,
                "release_date": "Oct 29, 2018 at 01:30 UTC",
                "visibility_state": None,
                "has_explicit_staff_lock": False,
                "start": "2018-10-29T01:30:00Z",
                "graded": False,
                "due_date": "",
                "due": None,
                "relative_weeks_due": None,
                "format": None,
                "course_graders": ["Assesment"],
                "has_changes": True,
                "actions": {
                    "deletable": True,
                    "draggable": True,
                    "childAddable": True,
                    "duplicable": True,
                },
                "explanatory_message": None,
                "group_access": {},
                "user_partitions": [
                    {
                        "id": 50,
                        "name": "Enrollment Track Groups",
                        "scheme": "enrollment_track",
                        "groups": [
                            {
                                "id": 1,
                                "name": "Audit",
                                "selected": False,
                                "deleted": False,
                            }
                        ],
                    }
                ],
                "show_correctness": "always",
                "hide_from_toc": False,
                "enable_hide_from_toc_ui": False,
                "xblock_type": "problem",
                "highlights_enabled_for_messaging": False,
                "highlights_enabled": True,
                "highlights_preview_only": False,
                "highlights_doc_url": "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/open-release-redwood.master/developing_course/course_sections.html#set-section-highlights-for-weekly-course-highlight-messages",
                "child_info": {
                    "category": "chapter",
                    "display_name": "Section",
                    "children": [
                        {
                            "id": "block-v1:VirtuEducate+JCE+101+type@chapter+block@0224306c140145edbecbbb6492a9ebe1",
                            "display_name": "Introduction to Chemistry",
                            "category": "chapter",
                            "has_children": True,
                            "edited_on": "Apr 17, 2025 at 08:44 UTC",
                            "published": True,
                            "published_on": "Apr 17, 2025 at 13:13 UTC",
                            "studio_url": "/course/course-v1:VirtuEducate+JCE+101?show=block-v1%3AVirtuEducate%2BJCE%2B101%2Btype%40chapter%2Bblock%400224306c140145edbecbbb6492a9ebe1",
                            "lms_url": "https://local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@chapter+block@0224306c140145edbecbbb6492a9ebe1",
                            "embed_lms_url": "https://local.edly.io/xblock/block-v1:VirtuEducate+JCE+101+type@chapter+block@0224306c140145edbecbbb6492a9ebe1",
                            "released_to_students": True,
                            "release_date": "Apr 10, 2024 at 01:30 UTC",
                            "visibility_state": "live",
                            "has_explicit_staff_lock": False,
                            "start": "2024-04-10T01:30:00Z",
                            "graded": False,
                            "due_date": "",
                            "due": None,
                            "relative_weeks_due": None,
                            "format": None,
                            "course_graders": ["Assesment"],
                            "has_changes": False,
                            "actions": {
                                "deletable": True,
                                "draggable": True,
                                "childAddable": True,
                                "duplicable": True,
                            },
                            "explanatory_message": None,
                            "group_access": {},
                            "user_partitions": [
                                {
                                    "id": 50,
                                    "name": "Enrollment Track Groups",
                                    "scheme": "enrollment_track",
                                    "groups": [
                                        {
                                            "id": 1,
                                            "name": "Audit",
                                            "selected": False,
                                            "deleted": False,
                                        }
                                    ],
                                }
                            ],
                            "show_correctness": "always",
                            "hide_from_toc": False,
                            "enable_hide_from_toc_ui": False,
                            "xblock_type": "problem",
                            "highlights": [],
                            "highlights_enabled": True,
                            "highlights_preview_only": False,
                            "highlights_doc_url": "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/open-release-redwood.master/developing_course/course_sections.html#set-section-highlights-for-weekly-course-highlight-messages",
                            "child_info": {
                                "category": "sequential",
                                "display_name": "Subsection",
                                "children": [
                                    {
                                        "id": "block-v1:VirtuEducate+JCE+101+type@sequential+block@3dc52eac6f7e42c19f15394f55cab2b8",
                                        "display_name": "Meaning of Chemistry",
                                        "category": "sequential",
                                        "has_children": True,
                                        "edited_on": "Feb 22, 2025 at 14:24 UTC",
                                        "published": True,
                                        "published_on": "Apr 17, 2025 at 13:13 UTC",
                                        "studio_url": "/course/course-v1:VirtuEducate+JCE+101?show=block-v1%3AVirtuEducate%2BJCE%2B101%2Btype%40sequential%2Bblock%403dc52eac6f7e42c19f15394f55cab2b8",
                                        "lms_url": "https://local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@sequential+block@3dc52eac6f7e42c19f15394f55cab2b8",
                                        "embed_lms_url": "https://local.edly.io/xblock/block-v1:VirtuEducate+JCE+101+type@sequential+block@3dc52eac6f7e42c19f15394f55cab2b8",
                                        "released_to_students": True,
                                        "release_date": "Apr 10, 2024 at 01:30 UTC",
                                        "visibility_state": "live",
                                        "has_explicit_staff_lock": False,
                                        "start": "2024-04-10T01:30:00Z",
                                        "graded": True,
                                        "due_date": "",
                                        "due": None,
                                        "relative_weeks_due": None,
                                        "format": "Assesment",
                                        "course_graders": ["Assesment"],
                                        "has_changes": False,
                                        "actions": {
                                            "deletable": True,
                                            "draggable": True,
                                            "childAddable": True,
                                            "duplicable": True,
                                        },
                                        "explanatory_message": None,
                                        "group_access": {},
                                        "user_partitions": [
                                            {
                                                "id": 50,
                                                "name": "Enrollment Track Groups",
                                                "scheme": "enrollment_track",
                                                "groups": [
                                                    {
                                                        "id": 1,
                                                        "name": "Audit",
                                                        "selected": False,
                                                        "deleted": False,
                                                    }
                                                ],
                                            }
                                        ],
                                        "show_correctness": "always",
                                        "hide_from_toc": False,
                                        "enable_hide_from_toc_ui": False,
                                        "xblock_type": "problem",
                                        "hide_after_due": False,
                                        "child_info": {
                                            "category": "vertical",
                                            "display_name": "Unit",
                                            "children": [
                                                {
                                                    "id": "block-v1:VirtuEducate+JCE+101+type@vertical+block@f291f6e519e54bf880bf0cc2c155d7d8",
                                                    "display_name": "Skill",
                                                    "category": "vertical",
                                                    "has_children": True,
                                                    "edited_on": "Feb 22, 2025 at 14:24 UTC",
                                                    "published": True,
                                                    "published_on": "Apr 17, 2025 at 13:13 UTC",
                                                    "studio_url": "/container/block-v1:VirtuEducate+JCE+101+type@vertical+block@f291f6e519e54bf880bf0cc2c155d7d8",
                                                    "lms_url": "https://local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@vertical+block@f291f6e519e54bf880bf0cc2c155d7d8",
                                                    "embed_lms_url": "https://local.edly.io/xblock/block-v1:VirtuEducate+JCE+101+type@vertical+block@f291f6e519e54bf880bf0cc2c155d7d8",
                                                    "released_to_students": True,
                                                    "release_date": "Apr 10, 2024 at 01:30 UTC",
                                                    "visibility_state": "live",
                                                    "has_explicit_staff_lock": False,
                                                    "start": "2024-04-10T01:30:00Z",
                                                    "graded": True,
                                                    "due_date": "",
                                                    "due": None,
                                                    "relative_weeks_due": None,
                                                    "format": None,
                                                    "course_graders": ["Assesment"],
                                                    "has_changes": False,
                                                    "actions": {
                                                        "deletable": True,
                                                        "draggable": True,
                                                        "childAddable": True,
                                                        "duplicable": True,
                                                    },
                                                    "explanatory_message": None,
                                                    "group_access": {},
                                                    "user_partitions": [
                                                        {
                                                            "id": 50,
                                                            "name": "Enrollment Track Groups",
                                                            "scheme": "enrollment_track",
                                                            "groups": [
                                                                {
                                                                    "id": 1,
                                                                    "name": "Audit",
                                                                    "selected": False,
                                                                    "deleted": False,
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                    "show_correctness": "always",
                                                    "hide_from_toc": False,
                                                    "enable_hide_from_toc_ui": False,
                                                    "xblock_type": "problem",
                                                    "discussion_enabled": True,
                                                    "ancestor_has_staff_lock": False,
                                                    "is_tagging_feature_disabled": False,
                                                    "taxonomy_tags_widget_url": "https://apps.local.edly.io/course-authoring/tagging/components/widget/",
                                                    "course_authoring_url": "https://apps.local.edly.io/course-authoring",
                                                    "staff_only_message": False,
                                                    "hide_from_toc_message": False,
                                                    "course_tags_count": {},
                                                    "tag_counts_by_block": {},
                                                    "has_partition_group_components": False,
                                                    "user_partition_info": {
                                                        "selectable_partitions": [],
                                                        "selected_partition_index": -1,
                                                        "selected_groups_label": "",
                                                    },
                                                    "enable_copy_paste_units": True,
                                                },
                                                {
                                                    "id": "block-v1:VirtuEducate+JCE+101+type@vertical+block@ba21f482a4504d39802dc1e1714498ff",
                                                    "display_name": "Unit",
                                                    "category": "vertical",
                                                    "has_children": True,
                                                    "edited_on": "Feb 12, 2025 at 19:29 UTC",
                                                    "published": True,
                                                    "published_on": "Apr 17, 2025 at 13:13 UTC",
                                                    "studio_url": "/container/block-v1:VirtuEducate+JCE+101+type@vertical+block@ba21f482a4504d39802dc1e1714498ff",
                                                    "lms_url": "https://local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@vertical+block@ba21f482a4504d39802dc1e1714498ff",
                                                    "embed_lms_url": "https://local.edly.io/xblock/block-v1:VirtuEducate+JCE+101+type@vertical+block@ba21f482a4504d39802dc1e1714498ff",
                                                    "released_to_students": True,
                                                    "release_date": "Apr 10, 2024 at 01:30 UTC",
                                                    "visibility_state": "live",
                                                    "has_explicit_staff_lock": False,
                                                    "start": "2024-04-10T01:30:00Z",
                                                    "graded": True,
                                                    "due_date": "",
                                                    "due": None,
                                                    "relative_weeks_due": None,
                                                    "format": None,
                                                    "course_graders": ["Assesment"],
                                                    "has_changes": False,
                                                    "actions": {
                                                        "deletable": True,
                                                        "draggable": True,
                                                        "childAddable": True,
                                                        "duplicable": True,
                                                    },
                                                    "explanatory_message": None,
                                                    "group_access": {},
                                                    "user_partitions": [
                                                        {
                                                            "id": 50,
                                                            "name": "Enrollment Track Groups",
                                                            "scheme": "enrollment_track",
                                                            "groups": [
                                                                {
                                                                    "id": 1,
                                                                    "name": "Audit",
                                                                    "selected": False,
                                                                    "deleted": False,
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                    "show_correctness": "always",
                                                    "hide_from_toc": False,
                                                    "enable_hide_from_toc_ui": False,
                                                    "xblock_type": "video",
                                                    "discussion_enabled": True,
                                                    "ancestor_has_staff_lock": False,
                                                    "is_tagging_feature_disabled": False,
                                                    "taxonomy_tags_widget_url": "https://apps.local.edly.io/course-authoring/tagging/components/widget/",
                                                    "course_authoring_url": "https://apps.local.edly.io/course-authoring",
                                                    "staff_only_message": False,
                                                    "hide_from_toc_message": False,
                                                    "course_tags_count": {},
                                                    "tag_counts_by_block": {},
                                                    "has_partition_group_components": False,
                                                    "user_partition_info": {
                                                        "selectable_partitions": [],
                                                        "selected_partition_index": -1,
                                                        "selected_groups_label": "",
                                                    },
                                                    "enable_copy_paste_units": True,
                                                },
                                            ],
                                        },
                                        "ancestor_has_staff_lock": False,
                                        "is_tagging_feature_disabled": False,
                                        "taxonomy_tags_widget_url": "https://apps.local.edly.io/course-authoring/tagging/components/widget/",
                                        "course_authoring_url": "https://apps.local.edly.io/course-authoring",
                                        "staff_only_message": False,
                                        "hide_from_toc_message": False,
                                        "course_tags_count": {},
                                        "tag_counts_by_block": {},
                                        "has_partition_group_components": False,
                                        "user_partition_info": {
                                            "selectable_partitions": [],
                                            "selected_partition_index": -1,
                                            "selected_groups_label": "",
                                        },
                                        "enable_copy_paste_units": True,
                                    },
                                    {
                                        "id": "block-v1:VirtuEducate+JCE+101+type@sequential+block@5a58b9c06ea6415db6ab8979e0e9531a",
                                        "display_name": "Application of Chemistry",
                                        "category": "sequential",
                                        "has_children": True,
                                        "edited_on": "Feb 13, 2025 at 15:03 UTC",
                                        "published": True,
                                        "published_on": "Apr 17, 2025 at 13:13 UTC",
                                        "studio_url": "/course/course-v1:VirtuEducate+JCE+101?show=block-v1%3AVirtuEducate%2BJCE%2B101%2Btype%40sequential%2Bblock%405a58b9c06ea6415db6ab8979e0e9531a",
                                        "lms_url": "https://local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@sequential+block@5a58b9c06ea6415db6ab8979e0e9531a",
                                        "embed_lms_url": "https://local.edly.io/xblock/block-v1:VirtuEducate+JCE+101+type@sequential+block@5a58b9c06ea6415db6ab8979e0e9531a",
                                        "released_to_students": True,
                                        "release_date": "Apr 10, 2024 at 01:30 UTC",
                                        "visibility_state": "live",
                                        "has_explicit_staff_lock": False,
                                        "start": "2024-04-10T01:30:00Z",
                                        "graded": True,
                                        "due_date": "",
                                        "due": None,
                                        "relative_weeks_due": None,
                                        "format": "Assesment",
                                        "course_graders": ["Assesment"],
                                        "has_changes": False,
                                        "actions": {
                                            "deletable": True,
                                            "draggable": True,
                                            "childAddable": True,
                                            "duplicable": True,
                                        },
                                        "explanatory_message": None,
                                        "group_access": {},
                                        "user_partitions": [
                                            {
                                                "id": 50,
                                                "name": "Enrollment Track Groups",
                                                "scheme": "enrollment_track",
                                                "groups": [
                                                    {
                                                        "id": 1,
                                                        "name": "Audit",
                                                        "selected": False,
                                                        "deleted": False,
                                                    }
                                                ],
                                            }
                                        ],
                                        "show_correctness": "always",
                                        "hide_from_toc": False,
                                        "enable_hide_from_toc_ui": False,
                                        "xblock_type": "video",
                                        "hide_after_due": False,
                                        "child_info": {
                                            "category": "vertical",
                                            "display_name": "Unit",
                                            "children": [
                                                {
                                                    "id": "block-v1:VirtuEducate+JCE+101+type@vertical+block@ebc418bf11684376a8d29f9f01b452a3",
                                                    "display_name": "Unit",
                                                    "category": "vertical",
                                                    "has_children": True,
                                                    "edited_on": "Jan 29, 2025 at 23:06 UTC",
                                                    "published": True,
                                                    "published_on": "Apr 17, 2025 at 13:13 UTC",
                                                    "studio_url": "/container/block-v1:VirtuEducate+JCE+101+type@vertical+block@ebc418bf11684376a8d29f9f01b452a3",
                                                    "lms_url": "https://local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@vertical+block@ebc418bf11684376a8d29f9f01b452a3",
                                                    "embed_lms_url": "https://local.edly.io/xblock/block-v1:VirtuEducate+JCE+101+type@vertical+block@ebc418bf11684376a8d29f9f01b452a3",
                                                    "released_to_students": True,
                                                    "release_date": "Apr 10, 2024 at 01:30 UTC",
                                                    "visibility_state": "live",
                                                    "has_explicit_staff_lock": False,
                                                    "start": "2024-04-10T01:30:00Z",
                                                    "graded": True,
                                                    "due_date": "",
                                                    "due": None,
                                                    "relative_weeks_due": None,
                                                    "format": None,
                                                    "course_graders": ["Assesment"],
                                                    "has_changes": False,
                                                    "actions": {
                                                        "deletable": True,
                                                        "draggable": True,
                                                        "childAddable": True,
                                                        "duplicable": True,
                                                    },
                                                    "explanatory_message": None,
                                                    "group_access": {},
                                                    "user_partitions": [
                                                        {
                                                            "id": 50,
                                                            "name": "Enrollment Track Groups",
                                                            "scheme": "enrollment_track",
                                                            "groups": [
                                                                {
                                                                    "id": 1,
                                                                    "name": "Audit",
                                                                    "selected": False,
                                                                    "deleted": False,
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                    "show_correctness": "always",
                                                    "hide_from_toc": False,
                                                    "enable_hide_from_toc_ui": False,
                                                    "xblock_type": "other",
                                                    "discussion_enabled": True,
                                                    "ancestor_has_staff_lock": False,
                                                    "is_tagging_feature_disabled": False,
                                                    "taxonomy_tags_widget_url": "https://apps.local.edly.io/course-authoring/tagging/components/widget/",
                                                    "course_authoring_url": "https://apps.local.edly.io/course-authoring",
                                                    "staff_only_message": False,
                                                    "hide_from_toc_message": False,
                                                    "course_tags_count": {},
                                                    "tag_counts_by_block": {},
                                                    "has_partition_group_components": False,
                                                    "user_partition_info": {
                                                        "selectable_partitions": [],
                                                        "selected_partition_index": -1,
                                                        "selected_groups_label": "",
                                                    },
                                                    "enable_copy_paste_units": True,
                                                },
                                                {
                                                    "id": "block-v1:VirtuEducate+JCE+101+type@vertical+block@f51b316c5146468d9a42cf773239bcf7",
                                                    "display_name": "Unit",
                                                    "category": "vertical",
                                                    "has_children": True,
                                                    "edited_on": "Feb 12, 2025 at 22:29 UTC",
                                                    "published": True,
                                                    "published_on": "Apr 17, 2025 at 13:13 UTC",
                                                    "studio_url": "/container/block-v1:VirtuEducate+JCE+101+type@vertical+block@f51b316c5146468d9a42cf773239bcf7",
                                                    "lms_url": "https://local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@vertical+block@f51b316c5146468d9a42cf773239bcf7",
                                                    "embed_lms_url": "https://local.edly.io/xblock/block-v1:VirtuEducate+JCE+101+type@vertical+block@f51b316c5146468d9a42cf773239bcf7",
                                                    "released_to_students": True,
                                                    "release_date": "Apr 10, 2024 at 01:30 UTC",
                                                    "visibility_state": "live",
                                                    "has_explicit_staff_lock": False,
                                                    "start": "2024-04-10T01:30:00Z",
                                                    "graded": True,
                                                    "due_date": "",
                                                    "due": None,
                                                    "relative_weeks_due": None,
                                                    "format": None,
                                                    "course_graders": ["Assesment"],
                                                    "has_changes": False,
                                                    "actions": {
                                                        "deletable": True,
                                                        "draggable": True,
                                                        "childAddable": True,
                                                        "duplicable": True,
                                                    },
                                                    "explanatory_message": None,
                                                    "group_access": {},
                                                    "user_partitions": [
                                                        {
                                                            "id": 50,
                                                            "name": "Enrollment Track Groups",
                                                            "scheme": "enrollment_track",
                                                            "groups": [
                                                                {
                                                                    "id": 1,
                                                                    "name": "Audit",
                                                                    "selected": False,
                                                                    "deleted": False,
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                    "show_correctness": "always",
                                                    "hide_from_toc": False,
                                                    "enable_hide_from_toc_ui": False,
                                                    "xblock_type": "video",
                                                    "discussion_enabled": True,
                                                    "ancestor_has_staff_lock": False,
                                                    "is_tagging_feature_disabled": False,
                                                    "taxonomy_tags_widget_url": "https://apps.local.edly.io/course-authoring/tagging/components/widget/",
                                                    "course_authoring_url": "https://apps.local.edly.io/course-authoring",
                                                    "staff_only_message": False,
                                                    "hide_from_toc_message": False,
                                                    "course_tags_count": {},
                                                    "tag_counts_by_block": {},
                                                    "has_partition_group_components": False,
                                                    "user_partition_info": {
                                                        "selectable_partitions": [],
                                                        "selected_partition_index": -1,
                                                        "selected_groups_label": "",
                                                    },
                                                    "enable_copy_paste_units": True,
                                                },
                                            ],
                                        },
                                        "ancestor_has_staff_lock": False,
                                        "is_tagging_feature_disabled": False,
                                        "taxonomy_tags_widget_url": "https://apps.local.edly.io/course-authoring/tagging/components/widget/",
                                        "course_authoring_url": "https://apps.local.edly.io/course-authoring",
                                        "staff_only_message": False,
                                        "hide_from_toc_message": False,
                                        "course_tags_count": {},
                                        "tag_counts_by_block": {},
                                        "has_partition_group_components": False,
                                        "user_partition_info": {
                                            "selectable_partitions": [],
                                            "selected_partition_index": -1,
                                            "selected_groups_label": "",
                                        },
                                        "enable_copy_paste_units": True,
                                    },
                                ],
                            },
                            "ancestor_has_staff_lock": False,
                            "is_tagging_feature_disabled": False,
                            "taxonomy_tags_widget_url": "https://apps.local.edly.io/course-authoring/tagging/components/widget/",
                            "course_authoring_url": "https://apps.local.edly.io/course-authoring",
                            "staff_only_message": False,
                            "hide_from_toc_message": False,
                            "course_tags_count": {},
                            "tag_counts_by_block": {},
                            "has_partition_group_components": False,
                            "user_partition_info": {
                                "selectable_partitions": [],
                                "selected_partition_index": -1,
                                "selected_groups_label": "",
                            },
                            "enable_copy_paste_units": True,
                        },
                        {
                            "id": "block-v1:VirtuEducate+JCE+101+type@chapter+block@a41cef5aab0844cbac39c57091990839",
                            "display_name": "Mallen Kamundi",
                            "category": "chapter",
                            "has_children": True,
                            "edited_on": "Apr 17, 2025 at 13:47 UTC",
                            "published": True,
                            "published_on": "Apr 17, 2025 at 13:47 UTC",
                            "studio_url": "/course/course-v1:VirtuEducate+JCE+101?show=block-v1%3AVirtuEducate%2BJCE%2B101%2Btype%40chapter%2Bblock%40a41cef5aab0844cbac39c57091990839",
                            "lms_url": "https://local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@chapter+block@a41cef5aab0844cbac39c57091990839",
                            "embed_lms_url": "https://local.edly.io/xblock/block-v1:VirtuEducate+JCE+101+type@chapter+block@a41cef5aab0844cbac39c57091990839",
                            "released_to_students": True,
                            "release_date": "Oct 29, 2018 at 01:30 UTC",
                            "visibility_state": "live",
                            "has_explicit_staff_lock": False,
                            "start": "2018-10-29T01:30:00Z",
                            "graded": False,
                            "due_date": "",
                            "due": None,
                            "relative_weeks_due": None,
                            "format": None,
                            "course_graders": ["Assesment"],
                            "has_changes": True,
                            "actions": {
                                "deletable": True,
                                "draggable": True,
                                "childAddable": True,
                                "duplicable": True,
                            },
                            "explanatory_message": None,
                            "group_access": {},
                            "user_partitions": [
                                {
                                    "id": 50,
                                    "name": "Enrollment Track Groups",
                                    "scheme": "enrollment_track",
                                    "groups": [
                                        {
                                            "id": 1,
                                            "name": "Audit",
                                            "selected": False,
                                            "deleted": False,
                                        }
                                    ],
                                }
                            ],
                            "show_correctness": "always",
                            "hide_from_toc": False,
                            "enable_hide_from_toc_ui": False,
                            "xblock_type": "other",
                            "highlights": [],
                            "highlights_enabled": True,
                            "highlights_preview_only": False,
                            "highlights_doc_url": "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/open-release-redwood.master/developing_course/course_sections.html#set-section-highlights-for-weekly-course-highlight-messages",
                            "child_info": {
                                "category": "sequential",
                                "display_name": "Subsection",
                                "children": [
                                    {
                                        "id": "block-v1:VirtuEducate+JCE+101+type@sequential+block@40e6cce996c5428f9c34e60316e7d0e2",
                                        "display_name": "Subsection",
                                        "category": "sequential",
                                        "has_children": True,
                                        "edited_on": "Apr 17, 2025 at 13:41 UTC",
                                        "published": True,
                                        "published_on": "Apr 17, 2025 at 13:16 UTC",
                                        "studio_url": "/course/course-v1:VirtuEducate+JCE+101?show=block-v1%3AVirtuEducate%2BJCE%2B101%2Btype%40sequential%2Bblock%4040e6cce996c5428f9c34e60316e7d0e2",
                                        "lms_url": "https://local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@sequential+block@40e6cce996c5428f9c34e60316e7d0e2",
                                        "embed_lms_url": "https://local.edly.io/xblock/block-v1:VirtuEducate+JCE+101+type@sequential+block@40e6cce996c5428f9c34e60316e7d0e2",
                                        "released_to_students": True,
                                        "release_date": "Oct 29, 2018 at 01:30 UTC",
                                        "visibility_state": "live",
                                        "has_explicit_staff_lock": False,
                                        "start": "2018-10-29T01:30:00Z",
                                        "graded": False,
                                        "due_date": "",
                                        "due": None,
                                        "relative_weeks_due": None,
                                        "format": None,
                                        "course_graders": ["Assesment"],
                                        "has_changes": True,
                                        "actions": {
                                            "deletable": True,
                                            "draggable": True,
                                            "childAddable": True,
                                            "duplicable": True,
                                        },
                                        "explanatory_message": None,
                                        "group_access": {},
                                        "user_partitions": [
                                            {
                                                "id": 50,
                                                "name": "Enrollment Track Groups",
                                                "scheme": "enrollment_track",
                                                "groups": [
                                                    {
                                                        "id": 1,
                                                        "name": "Audit",
                                                        "selected": False,
                                                        "deleted": False,
                                                    }
                                                ],
                                            }
                                        ],
                                        "show_correctness": "always",
                                        "hide_from_toc": False,
                                        "enable_hide_from_toc_ui": False,
                                        "xblock_type": "other",
                                        "hide_after_due": False,
                                        "child_info": {
                                            "category": "vertical",
                                            "display_name": "Unit",
                                            "children": [
                                                {
                                                    "id": "block-v1:VirtuEducate+JCE+101+type@vertical+block@c2aef35c280b4302a92ea9917583cf4f",
                                                    "display_name": "Unit",
                                                    "category": "vertical",
                                                    "has_children": True,
                                                    "edited_on": "Apr 17, 2025 at 08:40 UTC",
                                                    "published": True,
                                                    "published_on": "Apr 17, 2025 at 13:16 UTC",
                                                    "studio_url": "/container/block-v1:VirtuEducate+JCE+101+type@vertical+block@c2aef35c280b4302a92ea9917583cf4f",
                                                    "lms_url": "https://local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@vertical+block@c2aef35c280b4302a92ea9917583cf4f",
                                                    "embed_lms_url": "https://local.edly.io/xblock/block-v1:VirtuEducate+JCE+101+type@vertical+block@c2aef35c280b4302a92ea9917583cf4f",
                                                    "released_to_students": True,
                                                    "release_date": "Oct 29, 2018 at 01:30 UTC",
                                                    "visibility_state": "live",
                                                    "has_explicit_staff_lock": False,
                                                    "start": "2018-10-29T01:30:00Z",
                                                    "graded": False,
                                                    "due_date": "",
                                                    "due": None,
                                                    "relative_weeks_due": None,
                                                    "format": None,
                                                    "course_graders": ["Assesment"],
                                                    "has_changes": False,
                                                    "actions": {
                                                        "deletable": True,
                                                        "draggable": True,
                                                        "childAddable": True,
                                                        "duplicable": True,
                                                    },
                                                    "explanatory_message": None,
                                                    "group_access": {},
                                                    "user_partitions": [
                                                        {
                                                            "id": 50,
                                                            "name": "Enrollment Track Groups",
                                                            "scheme": "enrollment_track",
                                                            "groups": [
                                                                {
                                                                    "id": 1,
                                                                    "name": "Audit",
                                                                    "selected": False,
                                                                    "deleted": False,
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                    "show_correctness": "always",
                                                    "hide_from_toc": False,
                                                    "enable_hide_from_toc_ui": False,
                                                    "xblock_type": "other",
                                                    "discussion_enabled": True,
                                                    "ancestor_has_staff_lock": False,
                                                    "is_tagging_feature_disabled": False,
                                                    "taxonomy_tags_widget_url": "https://apps.local.edly.io/course-authoring/tagging/components/widget/",
                                                    "course_authoring_url": "https://apps.local.edly.io/course-authoring",
                                                    "staff_only_message": False,
                                                    "hide_from_toc_message": False,
                                                    "course_tags_count": {},
                                                    "tag_counts_by_block": {},
                                                    "has_partition_group_components": False,
                                                    "user_partition_info": {
                                                        "selectable_partitions": [],
                                                        "selected_partition_index": -1,
                                                        "selected_groups_label": "",
                                                    },
                                                    "enable_copy_paste_units": True,
                                                },
                                                {
                                                    "id": "block-v1:VirtuEducate+JCE+101+type@vertical+block@60e458d15504472abd424ca3de47fcd4",
                                                    "display_name": "Unit",
                                                    "category": "vertical",
                                                    "has_children": True,
                                                    "edited_on": "Apr 17, 2025 at 13:41 UTC",
                                                    "published": True,
                                                    "published_on": "Apr 17, 2025 at 13:41 UTC",
                                                    "studio_url": "/container/block-v1:VirtuEducate+JCE+101+type@vertical+block@60e458d15504472abd424ca3de47fcd4",
                                                    "lms_url": "https://local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@vertical+block@60e458d15504472abd424ca3de47fcd4",
                                                    "embed_lms_url": "https://local.edly.io/xblock/block-v1:VirtuEducate+JCE+101+type@vertical+block@60e458d15504472abd424ca3de47fcd4",
                                                    "released_to_students": True,
                                                    "release_date": "Oct 29, 2018 at 01:30 UTC",
                                                    "visibility_state": "live",
                                                    "has_explicit_staff_lock": False,
                                                    "start": "2018-10-29T01:30:00Z",
                                                    "graded": False,
                                                    "due_date": "",
                                                    "due": None,
                                                    "relative_weeks_due": None,
                                                    "format": None,
                                                    "course_graders": ["Assesment"],
                                                    "has_changes": False,
                                                    "actions": {
                                                        "deletable": True,
                                                        "draggable": True,
                                                        "childAddable": True,
                                                        "duplicable": True,
                                                    },
                                                    "explanatory_message": None,
                                                    "group_access": {},
                                                    "user_partitions": [
                                                        {
                                                            "id": 50,
                                                            "name": "Enrollment Track Groups",
                                                            "scheme": "enrollment_track",
                                                            "groups": [
                                                                {
                                                                    "id": 1,
                                                                    "name": "Audit",
                                                                    "selected": False,
                                                                    "deleted": False,
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                    "show_correctness": "always",
                                                    "hide_from_toc": False,
                                                    "enable_hide_from_toc_ui": False,
                                                    "xblock_type": "other",
                                                    "discussion_enabled": True,
                                                    "ancestor_has_staff_lock": False,
                                                    "is_tagging_feature_disabled": False,
                                                    "taxonomy_tags_widget_url": "https://apps.local.edly.io/course-authoring/tagging/components/widget/",
                                                    "course_authoring_url": "https://apps.local.edly.io/course-authoring",
                                                    "staff_only_message": False,
                                                    "hide_from_toc_message": False,
                                                    "course_tags_count": {},
                                                    "tag_counts_by_block": {},
                                                    "has_partition_group_components": False,
                                                    "user_partition_info": {
                                                        "selectable_partitions": [],
                                                        "selected_partition_index": -1,
                                                        "selected_groups_label": "",
                                                    },
                                                    "enable_copy_paste_units": True,
                                                },
                                            ],
                                        },
                                        "ancestor_has_staff_lock": False,
                                        "is_tagging_feature_disabled": False,
                                        "taxonomy_tags_widget_url": "https://apps.local.edly.io/course-authoring/tagging/components/widget/",
                                        "course_authoring_url": "https://apps.local.edly.io/course-authoring",
                                        "staff_only_message": False,
                                        "hide_from_toc_message": False,
                                        "course_tags_count": {},
                                        "tag_counts_by_block": {},
                                        "has_partition_group_components": False,
                                        "user_partition_info": {
                                            "selectable_partitions": [],
                                            "selected_partition_index": -1,
                                            "selected_groups_label": "",
                                        },
                                        "enable_copy_paste_units": True,
                                    }
                                ],
                            },
                            "ancestor_has_staff_lock": False,
                            "is_tagging_feature_disabled": False,
                            "taxonomy_tags_widget_url": "https://apps.local.edly.io/course-authoring/tagging/components/widget/",
                            "course_authoring_url": "https://apps.local.edly.io/course-authoring",
                            "staff_only_message": False,
                            "hide_from_toc_message": False,
                            "course_tags_count": {},
                            "tag_counts_by_block": {},
                            "has_partition_group_components": False,
                            "user_partition_info": {
                                "selectable_partitions": [],
                                "selected_partition_index": -1,
                                "selected_groups_label": "",
                            },
                            "enable_copy_paste_units": True,
                        },
                        {
                            "id": "block-v1:VirtuEducate+JCE+101+type@chapter+block@0cf3e0f18e4341de853100163d4bb23d",
                            "display_name": "Section",
                            "category": "chapter",
                            "has_children": True,
                            "edited_on": "Apr 17, 2025 at 14:21 UTC",
                            "published": True,
                            "published_on": "Apr 17, 2025 at 14:21 UTC",
                            "studio_url": "/course/course-v1:VirtuEducate+JCE+101?show=block-v1%3AVirtuEducate%2BJCE%2B101%2Btype%40chapter%2Bblock%400cf3e0f18e4341de853100163d4bb23d",
                            "lms_url": "https://local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@chapter+block@0cf3e0f18e4341de853100163d4bb23d",
                            "embed_lms_url": "https://local.edly.io/xblock/block-v1:VirtuEducate+JCE+101+type@chapter+block@0cf3e0f18e4341de853100163d4bb23d",
                            "released_to_students": True,
                            "release_date": "Oct 29, 2018 at 01:30 UTC",
                            "visibility_state": "live",
                            "has_explicit_staff_lock": False,
                            "start": "2018-10-29T01:30:00Z",
                            "graded": False,
                            "due_date": "",
                            "due": None,
                            "relative_weeks_due": None,
                            "format": None,
                            "course_graders": ["Assesment"],
                            "has_changes": False,
                            "actions": {
                                "deletable": True,
                                "draggable": True,
                                "childAddable": True,
                                "duplicable": True,
                            },
                            "explanatory_message": None,
                            "group_access": {},
                            "user_partitions": [
                                {
                                    "id": 50,
                                    "name": "Enrollment Track Groups",
                                    "scheme": "enrollment_track",
                                    "groups": [
                                        {
                                            "id": 1,
                                            "name": "Audit",
                                            "selected": False,
                                            "deleted": False,
                                        }
                                    ],
                                }
                            ],
                            "show_correctness": "always",
                            "hide_from_toc": False,
                            "enable_hide_from_toc_ui": False,
                            "xblock_type": "other",
                            "highlights": [],
                            "highlights_enabled": True,
                            "highlights_preview_only": False,
                            "highlights_doc_url": "https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/open-release-redwood.master/developing_course/course_sections.html#set-section-highlights-for-weekly-course-highlight-messages",
                            "child_info": {
                                "category": "sequential",
                                "display_name": "Subsection",
                                "children": [],
                            },
                            "ancestor_has_staff_lock": False,
                            "is_tagging_feature_disabled": False,
                            "taxonomy_tags_widget_url": "https://apps.local.edly.io/course-authoring/tagging/components/widget/",
                            "course_authoring_url": "https://apps.local.edly.io/course-authoring",
                            "staff_only_message": False,
                            "hide_from_toc_message": False,
                            "course_tags_count": {},
                            "tag_counts_by_block": {},
                            "has_partition_group_components": False,
                            "user_partition_info": {
                                "selectable_partitions": [],
                                "selected_partition_index": -1,
                                "selected_groups_label": "",
                            },
                            "enable_copy_paste_units": True,
                        },
                    ],
                },
                "ancestor_has_staff_lock": False,
                "is_tagging_feature_disabled": False,
                "taxonomy_tags_widget_url": "https://apps.local.edly.io/course-authoring/tagging/components/widget/",
                "course_authoring_url": "https://apps.local.edly.io/course-authoring",
                "staff_only_message": False,
                "hide_from_toc_message": False,
                "course_tags_count": {},
                "tag_counts_by_block": {},
                "has_partition_group_components": False,
                "user_partition_info": {
                    "selectable_partitions": [],
                    "selected_partition_index": -1,
                    "selected_groups_label": "",
                },
                "enable_copy_paste_units": True,
            },
            "deprecated_blocks_info": {
                "deprecated_enabled_block_types": [],
                "blocks": [],
                "advance_settings_url": "/settings/advanced/course-v1:VirtuEducate+JCE+101",
            },
            "discussions_incontext_feedback_url": "",
            "discussions_incontext_learnmore_url": "",
            "discussions_settings": {
                "enable_in_context": True,
                "enable_graded_units": False,
                "unit_level_visibility": True,
                "provider_type": "openedx",
                "discussion_configuration_url": "https://apps.local.edly.io/course-authoring/course/course-v1:VirtuEducate+JCE+101/pages-and-resources/discussion/settings",
            },
            "initial_state": None,
            "initial_user_clipboard": {
                "content": None,
                "source_usage_key": "",
                "source_context_title": "",
                "source_edit_url": "",
            },
            "language_code": "en",
            "lms_link": "//local.edly.io/courses/course-v1:VirtuEducate+JCE+101/jump_to/block-v1:VirtuEducate+JCE+101+type@course+block@course",
            "mfe_proctored_exam_settings_url": "",
            "notification_dismiss_url": None,
            "proctoring_errors": [],
            "reindex_link": "/course/course-v1:VirtuEducate+JCE+101/search_reindex",
            "rerun_notification_id": None,
            "advance_settings_url": "/settings/advanced/course-v1:VirtuEducate+JCE+101",
            "is_custom_relative_dates_active": False,
        }
        result = EdxDataTransformer.transform_structure(structure)

        assert isinstance(result, CourseStructure)
        assert (
            "block-v1:VirtuEducate+JCE+101+type@chapter+block@0224306c140145edbecbbb6492a9ebe1"
            in result.topics
        )
        assert (
            "block-v1:VirtuEducate+JCE+101+type@sequential+block@3dc52eac6f7e42c19f15394f55cab2b8"
            in result.sub_topics
        )
        assert (
            result.topic_to_sub_topic[
                "block-v1:VirtuEducate+JCE+101+type@sequential+block@3dc52eac6f7e42c19f15394f55cab2b8"
            ]
            == "block-v1:VirtuEducate+JCE+101+type@chapter+block@0224306c140145edbecbbb6492a9ebe1"
        )

    def test_transform_structure_with_factory_data(self):
        """Test transform_structure with factory-generated data"""
        structure = CourseStructureFactory()
        result = EdxDataTransformer.transform_structure(structure)

        # Get expected values from factory data
        topics_set = set()
        sub_topics_set = set()
        topic_to_sub_topic = {}

        for topic in structure["course_structure"]["child_info"]["children"]:
            topic_id = topic.get("id")
            if topic_id:
                topics_set.add(topic_id)

            for sub_topic in topic.get("child_info", {}).get("children", []):
                sub_topic_id = sub_topic.get("id")
                if sub_topic_id:
                    sub_topics_set.add(sub_topic_id)
                    topic_to_sub_topic[sub_topic_id] = topic_id

        assert result.topics == topics_set
        assert result.sub_topics == sub_topics_set
        assert result.topic_to_sub_topic == topic_to_sub_topic

    def test_transform_topics_empty_data(self):
        """Test transforming empty topics data"""
        empty_structure = {}
        result = EdxDataTransformer.transform_topics(empty_structure)

        assert isinstance(result, list)
        assert len(result) == 0

    def test_transform_topics_with_data(self):
        """Test transforming topics with actual data"""
        # Create test data with known values
        topic_id = "topic-abc"
        topic_name = "Test Topic"
        subtopic_id = "subtopic-xyz"
        subtopic_name = "Test Subtopic"

        structure = {
            "course_structure": {
                "child_info": {
                    "children": [
                        {
                            "id": topic_id,
                            "display_name": topic_name,
                            "has_children": True,
                            "child_info": {
                                "children": [
                                    {"id": subtopic_id, "display_name": subtopic_name}
                                ]
                            },
                        }
                    ]
                }
            }
        }

        result = EdxDataTransformer.transform_topics(structure)

        assert len(result) == 1
        assert isinstance(result[0], Topic)
        assert result[0].id == topic_id
        assert result[0].name == topic_name
        assert len(result[0].sub_topics) == 1
        assert result[0].sub_topics[0].id == subtopic_id
        assert result[0].sub_topics[0].name == subtopic_name
        assert result[0].sub_topics[0].topic_id == topic_id

    def test_transform_topics_with_factory_data(self):
        """Test transform_topics with factory-generated data"""
        structure = CourseStructureFactory()
        result = EdxDataTransformer.transform_topics(structure)

        # Verify topics match the input structure
        topic_data_list = structure["course_structure"]["child_info"]["children"]
        assert len(result) == len(topic_data_list)

        for i, topic in enumerate(result):
            topic_data = topic_data_list[i]
            assert topic.id == topic_data["id"]
            assert topic.name == topic_data["display_name"]

            # Verify subtopics
            subtopic_data_list = topic_data["child_info"]["children"]
            assert len(topic.sub_topics) == len(subtopic_data_list)

            for j, subtopic in enumerate(topic.sub_topics):
                subtopic_data = subtopic_data_list[j]
                assert subtopic.id == subtopic_data["id"]
                assert subtopic.name == subtopic_data["display_name"]
                assert subtopic.topic_id == topic_data["id"]

    def test_transform_to_course_outline(self):
        """Test transform_to_course_outline method"""
        structure = CourseStructureFactory()
        course_id = "course-123"
        title = "Test Course"

        result = EdxDataTransformer.transform_to_course_outline(
            structure, course_id, title
        )

        assert isinstance(result, EdxCourseOutline)
        assert result.course_id == course_id
        assert result.title == title
        assert isinstance(result.structure, CourseStructure)
        assert isinstance(result.topics, list)
        assert all(isinstance(topic, Topic) for topic in result.topics)

    def test_transform_to_course_outline_empty_data(self):
        """Test transform_to_course_outline with empty data"""
        empty_structure = {}
        course_id = "empty-course"
        title = "Empty Course"

        result = EdxDataTransformer.transform_to_course_outline(
            empty_structure, course_id, title
        )

        assert isinstance(result, EdxCourseOutline)
        assert result.course_id == course_id
        assert result.title == title
        assert isinstance(result.structure, CourseStructure)
        assert len(result.structure.topics) == 0
        assert len(result.structure.sub_topics) == 0
        assert len(result.structure.topic_to_sub_topic) == 0
        assert isinstance(result.topics, list)
        assert len(result.topics) == 0

    def test_structure_with_missing_data(self):
        """Test handling of missing data in structure"""
        # Structure with missing child_info
        structure = {
            "course_structure": {
                "some_other_field": "value"
                # No child_info field
            }
        }

        result = EdxDataTransformer.transform_structure(structure)
        assert len(result.topics) == 0
        assert len(result.sub_topics) == 0

        # Structure with topics missing IDs
        structure = {
            "course_structure": {
                "child_info": {
                    "children": [
                        {
                            # No ID field
                            "display_name": "Topic without ID",
                            "has_children": False,
                        }
                    ]
                }
            }
        }

        result = EdxDataTransformer.transform_structure(structure)
        assert len(result.topics) == 0

        # Structure with subtopics missing IDs
        structure = {
            "course_structure": {
                "child_info": {
                    "children": [
                        {
                            "id": "topic-with-invalid-subtopics",
                            "has_children": True,
                            "child_info": {
                                "children": [
                                    {
                                        # No ID field
                                        "display_name": "Subtopic without ID"
                                    }
                                ]
                            },
                        }
                    ]
                }
            }
        }

        result = EdxDataTransformer.transform_structure(structure)
        assert len(result.topics) == 1
        assert len(result.sub_topics) == 0
