from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .permissions import IsEnrolled
from django.shortcuts import get_object_or_404
from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer, CourseWithContentsSerializer


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# class CourseEnrollView(APIView):
#     authentication_classes = (BasicAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, pk, format=None):
#         course = get_object_or_404(Course, pk=pk)
#         # Add the current user to the students many-to-many relationship
#         # of the course by the given pk param and raise a 404 exception
#         # if it's not found
#         course.students.add(request.user)
#         return Response({'enrolled': True})


# The read-only actions list() and retrieve() to both list objects
# or retrieves a single object
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True,  # An action to be performed on a single object
            methods=['post'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()  # Retrieve the Course object
        course.students.add(request.user)
        return Response({'enrolled': True})

    @action(detail=True,
            methods=['get'],
            serializer_class=CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
