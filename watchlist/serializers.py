from rest_framework import serializers
from .models import WatchList, StreamPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    """
    Custom serializer class inherting 'ModelSerializer' 
    """    
    
    # user object string to display name of reviewer performing review
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        """
        Meta class for 'Review' serializer having 'Review' model
        and all 'fields excluding wacthlist field
        """        
        
        model = Review
        exclude = ('watchlist',)



class WatchListSerializer(serializers.ModelSerializer):
    """
    Custom serializer class inherting 'ModelSerializer' 
    """    
    
    # review objects to be displayed with watchlists
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        """
        Meta class for 'Watch List' serializer having 'WatchList' model and
        all 'fields
        """        
        
        model = WatchList
        fields = '__all__'
        
        
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    """
    Custom serializer class inherting 'ModelSerializer' 
    """    
    
    # item to show watchlists while searching for platforms
    watchlist = WatchListSerializer(many=True, read_only=True)
    
    class Meta:
        """
        Meta class for 'Streaming Platform' serializer having 'StreamPlatform' model
        and all 'fields
        """        
        
        model = StreamPlatform
        fields = '__all__'
        