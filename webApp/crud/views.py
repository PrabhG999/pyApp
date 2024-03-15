from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings

from .models import Cars
from .serializers import UserSerializer, CarsSerializer


# View is the heart of the application here uses serializer to to turn sqlquery to json

class UserSignUpView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_email'] = user.email  # Store the email in the session
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class CrudViewset(APIView):
    # Handles CRUD operations for Cars model
    def get(self, request, id=None):
        # If an ID is provided in the request, fetch a specific car
        if id:
            item = Cars.objects.get(car_id=id)
            serializer = CarsSerializer(item)
            # Return the serialized car data
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        # If no ID is provided, fetch all cars
        items = Cars.objects.all()
        serializer = CarsSerializer(items, many=True)
        # Return the serialized cars data
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        # Deserialize the incoming data to a Car object
        serializer = CarsSerializer(data=request.data)
        # If the data is valid
        if serializer.is_valid():
            # Save the car to the database
            serializer.save()
            # Respond with the serialized car data
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        # If the data is not valid, return an error message
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        # ID is required for a PATCH request
        if id is None:
            return Response({"status": "error", "data": "ID is required for patching"},
                            status=status.HTTP_400_BAD_REQUEST)
        # Fetch the specific car to be updated
        item = Cars.objects.get(car_id=id)
        # Partially update the car data
        serializer = CarsSerializer(item, data=request.data, partial=True)
        # If the updated data is valid
        if serializer.is_valid():
            # Save the updated car data
            serializer.save()
            # Respond with the serialized car data
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        # If the data is not valid, return an error message
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if id is None:
            return Response({"status": "error", "data": "car_id is required for deleting"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            item = Cars.objects.get(
                car_id=id)  # Change id to car_id, which is the actual field name in your model.
            item.delete()
            return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_200_OK)
        except Cars.DoesNotExist:
            return Response({"status": "error", "data": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id=None):
        # ID is required for a PUT request to update the entire car object
        if id is None:
            return Response({"status": "error", "data": "car_id is required for updating"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            # Fetch the specific car to be updated
            item = Cars.objects.get(car_id=id)
            # Update the car data with all the data provided
            serializer = CarsSerializer(item, data=request.data)
            # If the updated data is valid
            if serializer.is_valid():
                # Save the updated car data
                serializer.save()
                # Respond with the serialized car data
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            # If the data is not valid, return an error message
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Cars.DoesNotExist:
            # If the car does not exist, return an error message
            return Response({"status": "error", "data": "Car not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def buy_car(request, car_id):
    try:
        car = Cars.objects.get(pk=car_id)
        recipient_email = request.session.get('user_email', 'default_email@example.com')

        if recipient_email == 'default_email@example.com':
            return Response({"message": "User email not found. Cannot send email."},
                            status=status.HTTP_400_BAD_REQUEST)

        send_mail(
            subject='Car Purchase Confirmation',
            message=f'You bought {car.car_name} for ${car.car_price}.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        return Response({"message": "Purchase successful. Email sent to " + recipient_email},
                        status=status.HTTP_200_OK)
    except Cars.DoesNotExist:
        return Response({"message": "Car not found"}, status=status.HTTP_404_NOT_FOUND)
