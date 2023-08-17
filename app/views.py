from django.shortcuts import render , HttpResponse
from.models import Watchlist , Platforms , Reviews
from .serlizers import WatchlistSer , PlatformsSer , ReviewsSer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.decorators import api_view , APIView
from rest_framework import mixins , generics
from rest_framework.reverse import reverse
from rest_framework.serializers import ValidationError
from rest_framework.authentication import BasicAuthentication 
from rest_framework.permissions import IsAuthenticated ,IsAuthenticatedOrReadOnly

# ------------------------------ using generics ------------------------------ #
# ---------------------------- entry point of api ---------------------------- #
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'watchlist': reverse('Watchlist-list', request=request, format=format),
        'platforms': reverse('Platforms-list', request=request, format=format)
    })






class stream_list(generics.ListCreateAPIView):
    queryset = Platforms.objects.all()
    serializer_class = PlatformsSer
    # pagination_class = PageNumberPagination

class stream_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Platforms.objects.all()
    serializer_class = PlatformsSer


class Review_list(generics.ListAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSer
    # only login user can see
    # permission_classes = [IsAuthenticated]
    # if not login only you can see 
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Reviews.objects.filter(watchlist=pk)
    

class Review_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSer


class Review_create(generics.CreateAPIView):
    serializer_class = ReviewsSer

    def perform_create(self, serializer):
        # Get the watchlist item to which the review belongs
        watchlist_pk = self.kwargs['pk']
        try:
            watchlist = Watchlist.objects.get(pk=watchlist_pk)
        except Watchlist.DoesNotExist:
            raise ValidationError("Watchlist item not found")

        # Get the current logged-in user (review_user)
        review_user = self.request.user

        # Check if the user has already reviewed the same watchlist item
        review_queryset = Reviews.objects.filter(review_user=review_user, watchlist=watchlist)
        if review_queryset.exists():
            raise ValidationError("Can't review the same item multiple times")

        # Save the review with the watchlist and review_user
        serializer.save(watchlist=watchlist, review_user=review_user)

        # Calculate the average rating
        rating_sum = 0
        number_ratings = 0
        for review in Reviews.objects.filter(watchlist=watchlist):
            rating_sum += review.rating
            number_ratings += 1

        avg_rating = rating_sum / number_ratings if number_ratings else 0

        # Update the watchlist item with the calculated values
        watchlist.number_rating = number_ratings
        watchlist.avg_rating = avg_rating
        watchlist.save()




class Review_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSer


 # ------------------------------- using mixins ------------------------------- #




# class stream_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Platforms.objects.all()
#     serializer_class = PlatformsSer

#     def get(self,request):
#         return self.list(request)

#     def post(self,request):
#         return self.create(request)

# class stream_detail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,generics.GenericAPIView, mixins.DestroyModelMixin):
#     queryset = Platforms.objects.all()
#     serializer_class = PlatformsSer

#     def get(self,request, pk):
#         return self.retrieve(request, pk)

#     def put(self,request, pk):
#         return self.update(request, pk)
#     def delete(self,request, pk):
#         return self.destroy(request, pk)







 # ----------------------------- class based views ---------------------------- #





# class stream_list(APIView):
#     def get(self,request):
#         if request.method == "GET":
#             try:  
#                 stream_list = Platforms.objects.all()
#             except Platforms.DoesNotExist:
#                 return Response(status=status.HTTP_204_NO_CONTENT)
#             ser = PlatformsSer(stream_list, many=True)
#             return Response(ser.data, status=status.HTTP_201_CREATED)
        
#     def post(self,request):
#         try:   
#             nayadata = request.data
#         except Platforms.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         ser =  PlatformsSer(data=nayadata)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data, status=status.HTTP_201_CREATED)
#         return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)

# class stream_detail(APIView):
#     def pkk(self,pk):
#         try:
#             return Platforms.objects.get(pk=pk)
#         except Platforms.DoesNotExist:
#             raise http404

#     def get(self,request,pk):
#         data = self.pkk(pk)
#         ser = PlatformsSer(data)
#         return Response(ser.data)

#     def put(self,request,pk):
#         datas = self.pkk(pk)
#         ser = PlatformsSer(datas,data=request.data)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data, status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#     def delete(self,request,pk):
#         datas = self.pkk(pk)
#         datas.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




 # --------------------------- function based views --------------------------- #




@api_view(["GET"])
def movie_list(request):
    movies_list = Watchlist.objects.all()
    ser = WatchlistSer(movies_list, many=True)
    return Response(ser.data)

@api_view(["GET"])
def movie_detail(request,pk):
    movie = Watchlist.objects.get(pk=pk)
    ser = WatchlistSer(movie)
    return Response(ser.data)


# @api_view(["GET","POST"])
# def stream_list(request, format= None):
#     if request.method == "GET":
#         try:  
#             stream_list = Platforms.objects.all()
#         except Platforms.DoesNotExist:
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         ser = PlatformsSer(stream_list, many=True)
#         return Response(ser.data, status=status.HTTP_201_CREATED)

#     elif request.method == "POST":
#         try:   
#             nayadata = request.data
#         except Platforms.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         ser =  PlatformsSer(data=nayadata)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data, status=status.HTTP_201_CREATED)
#         return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(["GET","PUT","DELETE"])
# def stream_detail(request,pk,format= None):
#     try:
#         stream_detail = Platforms.objects.get(pk=pk)
#     except Platforms.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)


#     if request.method == "GET":
#         ser = PlatformsSer(stream_detail)
#         return Response(ser.data)

#     elif request.method == "PUT":
#         ser = PlatformsSer(stream_detail , data=request.data)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data, status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == "DELETE":
#         stream_detail.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

