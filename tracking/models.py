from django.db import models
from django.contrib.auth import get_user_model
from django.db.migrations import serializer


# Create your models here.
class Session(models.Model):
    owner_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Owned by: {self.owner_id}, Key: {self.pk}, Created on: {self.date_created}"

    def toJSON(self):
        return {"owner_id": self.owner_id.pk, "date_created": self.date_created, "key": self.pk}


class WeightExercise(models.Model):
    owner_id = models.ForeignKey("Session", verbose_name="Owned by session", on_delete=models.CASCADE)
    weight = models.FloatField(blank=False)
    exercise = models.TextField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def toJSON(self):
        return {
            "owner_key": self.owner_id.pk,
            "weight": self.weight,
            "exercise": self.exercise,
            "date_created": self.date_created,
            "key": self.pk,
        }


class SetRepInfo(models.Model):
    owner_id = models.ForeignKey("WeightExercise", verbose_name="Owned by WeightExercise", on_delete=models.CASCADE)
    # Monotonically increasing relative to WeightExercise
    set_number = models.IntegerField(blank=False)
    number_reps = models.IntegerField(blank=False)
    did_fail = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def toJSON(self):
        return {
            "owner_id": self.owner_id.pk,
            "set_number": self.set_number,
            "number_reps": self.number_reps,
            "did_fail": self.did_fail,
            "date_created": self.date_created,
            "key": self.pk,
        }