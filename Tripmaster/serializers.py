from rest_framework import serializers
from django.contrib.auth.models import User
from Tripmaster.models import TripDb,TripMemberDb

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripDb
        fields='__all__'
        read_only = ['title','start_date','destination']
class TripMemberSerializer(serializers.ModelSerializer):
    username=serializers.CharField(write_only=True)
    member_user_name=serializers.CharField(source=User.username,read_only=True)
    member_user_id=serializers.IntegerField(source=User.id,read_only=True)


    class Meta:
        model=TripMemberDb
        field=["id","username","member_username","member_user_id","joined_at"]
        read_only=["id","joined_at"]

    def validate_username(self,value):
        try:
            user=User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this username doe snot exist")
        trip=self.context['trip']

        if user == trip.created_by:
            raise serializers.ValidationError("The creator of the trp cannot be added as a member")
        if TripMemberDb.objects.filter(trip="trip",user="user").exist():
            raise serializers.ValidationError("")
        return value
    def create(self,validated_data):
        username=validated_data.pop()
        user=User.objects.get(username="username")
        trip=self.context['trip']
        trip_member=TripMemberDb.objects.create(trip="trip",user="user")

        return trip_member