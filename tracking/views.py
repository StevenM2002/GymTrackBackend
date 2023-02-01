from django.http import HttpResponseForbidden, HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from rest_framework import serializers


# Create your views here.
class SessionTrack(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        session = Session(owner_id=user)
        session.save()
        return Response({"key": session.pk, "date_created": session.date_created})

    def get(self, request):
        user = request.user
        all_sessions = Session.objects.filter(owner_id=user)
        all_sessions = [{"key": session.pk, "date_created": session.date_created} for session in all_sessions]
        return Response(all_sessions)

    def delete(self, request):
        user = request.user
        instance = Session.objects.get(pk=request.GET.get("key"))
        if instance.owner_id != user:
            return HttpResponseForbidden()
        instance.delete()
        ret = [val.toJSON() for val in Session.objects.filter(owner_id=user)]
        [val.pop('owner_id', None) for val in ret]
        return Response(ret)


class WeightExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightExercise
        fields = ["owner_id", "weight", "exercise"]


class WeightExerciseTrack(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seri = WeightExerciseSerializer(data=request.data)
        if not seri.is_valid():
            return HttpResponse(seri.errors, status=400)
        instance = seri.create(validated_data=seri.validated_data)
        if request.user != instance.owner_id.owner_id:
            return HttpResponseForbidden()
        instance.save()
        return Response(instance.toJSON())

    def get(self, request):
        session = Session.objects.get(pk=request.GET.get("owner_id"))
        if request.user != session.owner_id:
            return HttpResponseForbidden()
        instances = WeightExercise.objects.filter(owner_id=session)
        instances = [instance.toJSON() for instance in instances]
        return Response(instances)

    def delete(self, request):
        weight = WeightExercise.objects.get(pk=request.GET.get("key"))
        if request.user != weight.owner_id.owner_id:
            return HttpResponseForbidden()
        weight_ownerid = weight.owner_id
        weight.delete()
        instances = WeightExercise.objects.filter(owner_id=weight_ownerid)
        return Response([instance.toJSON() for instance in instances])

    def put(self, request):
        instance = WeightExercise.objects.get(pk=request.data["key"])
        if request.user != instance.owner_id.owner_id:
            return HttpResponseForbidden()
        instance.weight = request.data["weight"]
        instance.exercise = request.data["exercise"]
        instance.save()
        return Response(instance.toJSON())


class SetRepInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetRepInfo
        fields = ("number_reps", "did_fail", "owner_id", "set_number")


class SetRepInfoTrack(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        set_number = len(SetRepInfo.objects.filter(owner_id=request.data["owner_id"])) + 1
        # data = {
        #     "number_reps": request.data["number_reps"],
        #     "did_fail": request.data["did_fail"],
        #     "owner_id": request.data["owner_id"],
        #     "set_number": set_number,
        # }
        data = {}
        [data.update({k: v}) for k, v in request.data.items()]
        data["set_number"] = set_number
        seri = SetRepInfoSerializer(data=data)
        if not seri.is_valid():
            return HttpResponse(seri.errors, status=400)
        instance: SetRepInfo = seri.create(validated_data=seri.validated_data)
        if instance.owner_id.owner_id.owner_id != request.user:
            return HttpResponseForbidden()
        instance.save()
        return Response(instance.toJSON())

    def get(self, request):
        weightexercise_instance = WeightExercise.objects.get(pk=request.GET.get("owner_id"))
        if weightexercise_instance.owner_id.owner_id != request.user:
            return HttpResponseForbidden()
        instances = SetRepInfo.objects.filter(owner_id=weightexercise_instance)
        instances = [instance.toJSON() for instance in instances]
        return Response(instances)

    def delete(self, request):
        delete_instance = SetRepInfo.objects.get(pk=request.GET.get("key"))
        if delete_instance.owner_id.owner_id.owner_id != request.user:
            return HttpResponseForbidden()
        all_instances = SetRepInfo.objects.filter(owner_id=delete_instance.owner_id)
        for instance in all_instances:
            if instance.set_number > delete_instance.set_number:
                instance.set_number -= 1
                instance.save()
        delete_instance.delete()
        all_instances = SetRepInfo.objects.filter(owner_id=delete_instance.owner_id)
        return Response([instance.toJSON() for instance in all_instances])

    def put(self, request):
        instance = SetRepInfo.objects.get(pk=request.data["key"])
        if instance.owner_id.owner_id.owner_id != request.user:
            return HttpResponseForbidden()
        data = {}
        [data.update({k: v}) for k, v in request.data.items()]
        del data["key"]
        data["owner_id"] = instance.owner_id.pk
        data["set_number"] = instance.set_number
        seri = SetRepInfoSerializer(instance=instance, data=data)
        if not seri.is_valid():
            return HttpResponse(seri.errors, status=400)
        seri.save()
        instance = SetRepInfo.objects.get(pk=request.data["key"])
        return Response(instance.toJSON())
