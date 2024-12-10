from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializer import TaskSerializer

# Task Management Views (Create, View, Delete tasks)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    # Ensure that the user is authenticated via `request.user`
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # Save task with the authenticated user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_tasks(request):
    tasks = Task.objects.filter(user=request.user)  # Only get tasks of the authenticated user
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, pk):
    try:
        task = Task.objects.get(id=pk, user=request.user)  # Only delete tasks belonging to the authenticated user
        task.delete()
        return Response({"message": "Task deleted"}, status=status.HTTP_204_NO_CONTENT)
    except Task.DoesNotExist:
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
