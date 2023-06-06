from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import WatchList, StreamPlatform, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer


# Create your views here.
class ReviewList(generics.ListAPIView):
    """
    View for listing the reviews based on movies or watch items
    """    
    
    serializer_class = ReviewSerializer
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Method for creating custom query set based on watchlist (movie)

        Returns:
            QuerySet[Review]: queryset based on watchlist
        """        
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)



class ReviewCreate(generics.CreateAPIView):
    """
    View for creating reviews for watch items
    """    
    
    Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """
        Method for providing the queryset

        Returns:
            QuerySet[Review]: all review items
        """        
        
        return Review.objects.all()
    
    
    def perform_create(self, serializer):
        """
        Method to create a review for the watch item and
        displaying the avg_rating for the movies based on number of reviews
        given to the movie

        Args:
            serializer (Serializer): seriaalizer object for performing the creation step

        Raises:
            ValidationError: if single user tries to submit multiple reviews
        """        
        
        pk = self.kwargs.get('pk')        
        watchlist = WatchList.objects.get(pk=pk)
        
        # Checking if user had already submitted review
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError('Review already submitted!')
        
        # Generating avg rating for the movie and increaing number of reviews
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
        
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        
        # Saving the review object
        serializer.save(watchlist=watchlist, review_user=review_user)
        

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View for displaying details of a single review
    """    
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class StreamPlatformView(viewsets.ModelViewSet):
    """
    Model viewset for handling the stream platform view requests
    """    
    
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


class WatchListAV(APIView):
    """
    View for handling the list of watch items and creating new watch items
    """    
    
    def get(self, request):
        """
        Request method for handling the 'GET' request

        Args:
            request (Request): request object from the client side

        Returns:
            Response: personalized response object for the request recieved
        """        
        
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Request method for handling the 'POST' request

        Args:
            request (Request): request object from the client side

        Returns:
            Response: personalized response object for the request recieved
        """        
        
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailAV(APIView):
    """
    View for handling the single watch item
    """    
    
    def get(self, request, pk):
        """
        Request method to handle 'GET' request to display record

        Args:
            request (Request): request object recieved from client side
            pk (int): instance primary key

        Returns:
            Response: customized response object based on request recieved
        """        
        
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, pk):
        """
        Request method to handle 'PUT' request to completely update record

        Args:
            request (Request): request object recieved from client side
            pk (int): instance primary key

        Returns:
            Response: customized response object based on request recieved
        """        
        
        instance = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Request method to handle 'DELETE' request to remove record

        Args:
            request (Request): request object recieved from client side
            pk (int): instance primary key

        Returns:
            Response: customized response object based on request recieved
        """        

        instance = WatchList.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
