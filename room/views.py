from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from room.models import RoomOrder
from room.serializers import RoomOrderSerializer
# Create your views here.


class OrderTask(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk == None:
            if request.user.is_admin:
                data = RoomOrder.objects.filter(
                    start_time__gte=str(datetime.now()))
            else:
                data = RoomOrder.objects.filter(user_id=request.user.id).filter(
                    start_time__gte=str(datetime.now()))
        else:
            try:
                if request.user.is_admin:
                    data = RoomOrder.objects.filter(pk=pk).filter(
                        start_time__gte=str(datetime.now()))
                else:
                    data = RoomOrder.objects.filter(
                        user_id=request.user.id).filter(pk=pk).filter(
                        start_time__gte=str(datetime.now()))
            except:
                return Response({'message': 'No valid records found'})

        serializer = RoomOrderSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        # time = request.data['start_time']
        # new_time = datetime.strptime(time, '%Y/%m/%d %H:%M')
        # new_time = new_time + timedelta(minutes=15)
        # print('>>>>>>>>>>', new_time)
        # print('>>>>>>>>>>', type(new_time))

        data = request.data
        start_time = datetime.strptime(
            request.data['start_time'], '%Y/%m/%d %H:%M')
        end_time = datetime.strptime(
            request.data['end_time'], '%Y/%m/%d %H:%M')

        if start_time > end_time or start_time < datetime.now():
            return Response({'message': 'Input time invalid'}, status=status.HTTP_400_BAD_REQUEST)

        if start_time < (datetime.now() + timedelta(minutes=15)):
            return Response({"message": 'Enter time 15 minutes from now'}, status=status.HTTP_400_BAD_REQUEST)

        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', request.user.id)
        data['user_id'] = request.user.id
        data['start_time'] = start_time
        data['end_time'] = end_time
        serializer = RoomOrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user.id)

        return Response({'message': 'Record creation successful'}, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        if request.user.is_admin:
            return Response({'message': 'Permission not granted'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if RoomOrder.objects.filter(pk=pk).filter(user_id=request.user.id).count() <= 0:
                return Response({'message': 'Objects do not exist'}, status=status.HTTP_400_BAD_REQUEST)

            room_order = RoomOrder.objects.filter(
                pk=pk).filter(user_id=request.user.id)
            data = request.data

            serializer = RoomOrderSerializer(room_order[0], data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Object updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        if request.user.is_admin:
            return Response({'message': 'Permission not granted'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if RoomOrder.objects.filter(pk=pk).filter(user_id=request.user.id).count() <= 0:
                return Response({'message': 'Objects do not exist'}, status=status.HTTP_400_BAD_REQUEST)

            room_order = RoomOrder.objects.filter(
                pk=pk).filter(user_id=request.user.id)[0]
            data = request.data

            room_order.delete()

            return Response({'message': 'Object deleted successfully'}, status=status.HTTP_200_OK)
