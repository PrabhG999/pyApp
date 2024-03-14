from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers



class CrudViewset(APIView):
    # The get method retrieves either a list of all Cars or a single Car by ID.
    def get(self, request, id=None):  # parameter have id , if it provided id return the logic if not return all cars
        if id:
            # Retrieves a single Car by ID and serializes the data.
            item = models.Cars.objects.get(id=id)
            serializer = serializers.CarsSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        # If no ID is provided, it retrieves all Cars and serializes the data.
        items = models.Cars.objects.all()
        serializer = serializers.CarsSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    # The post method is for creating a new Car instance.
    def post(self, request):
        # Deserializes the input data and validates it.
        serializer = serializers.CarsSerializer(data=request.data)
        if serializer.is_valid():
            # Saves the valid data to the database.
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            # Returns an error response if the data is invalid.
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # The patch method is for partially updating a Car instance.
    def patch(self, request, id=None):
        if id is None:  # try catch block how it used to be in sb controller for exception
            return Response({"status": "error", "data": "ID is required for patching"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieves the Car instance by ID.
            item = models.Cars.objects.get(id=id)
        except models.Cars.DoesNotExist:
            # If the Car instance is not found, it returns an error response.
            return Response({"status": "error", "data": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

        # Partially updates the Car instance with the provided data.
        serializer = serializers.CarsSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            # Saves the valid updated data to the database.
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            # Returns an error response if the updated data is invalid.
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # The delete method is for deleting a Car instance by ID.
    def delete(self, request, id=None):
        if id is None:
            return Response({"status": "error", "data": "ID is required for deleting"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Filters the Car instance by ID.
            item = models.Cars.objects.get(id=id)
        except models.Cars.DoesNotExist:
            # If the Car instance is not found, it returns an error response.
            return Response({"status": "error", "data": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

        # Deletes the Car instance from the database.
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_200_OK)
