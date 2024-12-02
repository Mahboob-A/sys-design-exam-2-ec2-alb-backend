import uuid 
from django.db import models
from django.utils.translation import gettext_lazy as _ 

from core_apps.common.models import TimeStampModel


class TodoTasks(TimeStampModel):
    """Model for Todo Tasks"""

    title = models.CharField(verbose_name=_("Title of the Task"), max_length=255, db_index=True)
    description = models.TextField(verbose_name=_("Description of the Task"), blank=True, null=True)
    is_completed = models.BooleanField(default=False)


    class Meta:
        verbose_name = _("Todo App")
        verbose_name_plural = _("Todo Apps")

    def __str__(self):
        return self.title 

    @property
    def is_task_completed(self):
        return self.is_completed 
