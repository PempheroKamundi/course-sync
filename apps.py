from django.apps import AppConfig


class CourseSyncConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "course_sync"

    def ready(self):
        pass
