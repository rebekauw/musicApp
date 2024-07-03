from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class RoomView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class CreateRoomView(APIView):
    # specify the serializer class to use for 
    # validating and deserializing input data
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        # Session Management
        if not self.request.session.exists(self.request.session.session_key):
             self.request.session.create()
        
        #  the serializer is initialized with the data from the request('request.data')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data['guest_can_pause']
            vote_to_skip = serializer.data['vote_to_skip']
            host = self.request.session.session_key

            # filter rooms by host
            queryset = Room.objects.filter(host=host)

            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.vote_to_skip = vote_to_skip
                room.save(update_fields=['guest_can_pause', 'vote_to_skip'])
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, vote_to_skip=vote_to_skip)
                room.save()
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

