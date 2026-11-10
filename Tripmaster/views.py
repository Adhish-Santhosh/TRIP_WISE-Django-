from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from Tripmaster.serializers import UserSerializer,TripSerializer,TripMemberSerializer
from django.contrib.auth.models import User
from Tripmaster.models import TripDb,TripMemberDb
from rest_framework import authentication,permissions,serializers
from Tripmaster.permissions import OwnerOnly
# Create your views here.

class SignUpView(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=UserSerializer(data=form_data)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={"message":"User created successfully"},status=201)
        else:
            return Response(data=serializer_instance.errors,status=400)
class TripListCreateView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        qs = TripDb.objects.filter(created_by=request.user)
        serializer_instance=TripSerializer(qs,many=True)
        return Response(data=serializer_instance.data,status=200)
    def post(self,request):
        form_data=request.data
        serializer_instance=TripSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response(data={"message":"Trip Created Sucessfully",
                                  "trip": serializer_instance.data},status=200)
        else:
            return Response(data=serializer_instance.errors,status=400)  
class TripsRetrieveUpdateDeleteView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [OwnerOnly]

    def get(self, request, pk):
        qs = get_object_or_404(TripDb, id=pk)

        serializer_instance = TripSerializer(qs)
        return Response(data=serializer_instance.data)
    def put(self,request,pk):
        qs=get_object_or_404(TripDb,id=pk)
        serializer_instance = TripSerializer(
            qs,
            data=request.data
        )

        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)

            return Response(data={"message": "Trip Updated Successfully","trip": serializer_instance.data},status=200)

        else:
            return Response(data=serializer_instance.errors,status=400)
    def delete(self,request,pk):
        qs=get_object_or_404(TripDb,id=pk)
        qs.delete()
        return Response({"message":"Trip deleted successfully"},status=200)
class Userview(APIView):
    def get(self,request):
        qs=User.objects.all()
        serializer=UserSerializer(qs,many=True)
        return Response(serializer.data,status=200)

class TripMemberListCreateView(APIView):
    def get(self,request,trip_id):
        trip_object=get_object_or_404(TripDb,id=trip_id)
        is_owner=trip_object.created_by==request.user
        is_member=TripMemberDb.objects.filter(trip=trip_object,user=request.user).exists()
        if not (is_owner or is_member):
            raise serializers.ValidationError("You are not allowed to access the Trip")
        members=TripMemberDb.objects.filter(trip=trip_object)
        serializer_instance= TripMemberSerializer(members,many=True)
        return Response(data=serializer_instance.data,status=200)