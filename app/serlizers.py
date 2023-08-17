from rest_framework import serializers  
from.models import Watchlist, Platforms , Reviews


class WatchlistSer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = "__all__"

class PlatformsSer (serializers.ModelSerializer):
    # field level validation 
    # in this we use validation_<fieldname>
    def validate_name(self,value):
        if len(value)<=2:
            raise serializers.ValidationError("Name is too short")
        return value
    def validate_about(self,value):
        if len(value)<=2:
            raise serializers.ValidationError("about is too short")
        return value

    # fullmodel validation
    def validate(self,value): 
        if value['name'] == value["about"]:
            raise serializers.ValidationError("name and about must be different")
        return value


    # ------------------------------- hyperlinking ------------------------------- #
    # url  = serializers.HyperlinkedIdentityField(view_name="Platforms-detail")

    # ---------------------------- nested serlisation ---------------------------- #
    Watch_List = WatchlistSer(many=True,read_only=True)

    class Meta:
        model = Platforms
        fields = "__all__"



class ReviewsSer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    watchlist = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Reviews
        fields = "__all__"
        






# class WatchlistSer(serializers.Serializer):
#     title = serializers.CharField(max_length=30)
#     storyline = serializers.CharField(max_length=100)
#     # platform = serializers.ForeignKey(Platforms, on_delete=models.CASCADE)
#     active = serializers.BooleanField(default=True)
#     created = serializers.DateTimeField()

# class PlatformsSer (serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     about = serializers.CharField(max_length=100)
#     website = serializers.URLField(max_length=100)

#     def create(self, validated_data):
#         return Platforms.objects.create(**validated_data)


#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.about = validated_data.get('about', instance.about)
#         instance.website = validated_data.get('website', instance.website)
#         instance.save()
#         return instance
    