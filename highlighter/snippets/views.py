from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from .models import Snippet
from django.contrib.auth.models import User
from .serializers import SnippetSerializer, UserSerializer
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import renderers





@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


"""
  Example on how to use generics
"""

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

"""
   Example on how to use class based on views
"""

# class SnippetList(APIView):
#     """
#      List all code snippets, or create a new snippet
#     """
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    

# class SnippetDetail(APIView):
#     def get_object(self,pk):
#         try:
#             snippet = Snippet.objects.get(pk=pk)
#             return snippet
#         except Snippet.DoesNotExist:
#             raise Http404
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, many=False)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk=pk)
#         serializer = SnippetSerializer(snippet, data=request.data)

#         if serializer.is_valid:
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND )
    
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk=pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        

"""
   example on how to use function based views
"""
# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#     """
#     List all code snippets, or create a new snippet
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['GET', 'PUT', 'DELETE'])   
# def snippet_detail(request, pk):
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet, many=False)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'PUT':
#          serializer = SnippetSerializer(snippet, data=request.data)

#          if serializer.is_valid:
#                 serializer.save()
#                 return Response(serializer.data)
#          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)