from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User, Reservation, Menu
from .serializers import ReservationSerializer, MenuSerializer
from .utils import get_user_from_token
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
import logging
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ReservationSerializer
from .models import User, Reservation

# 로깅 설정
logger = logging.getLogger(__name__)

# 회원가입 API
@api_view(['POST'])
def register(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')

    if not name or not email or not password:
        return Response({"error": "All fields are required"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=400)

    user = User.objects.create(
        name=name,
        email=email,
        password=make_password(password)
    )
    logger.info(f"User {name} registered successfully.")
    return Response({"message": "User registered successfully"}, status=201)


# 로그인 API
@api_view(['POST'])
@permission_classes([AllowAny])  # 로그인은 인증이 필요없도록 설정
def login(request):
    email = request.data.get('email')  # Changed from username to email
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Both email and password are required'}, status=400)
    
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'email': user.email,
                    'name': user.name
                }
            }, status=200)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=401)

@login_required
def user_reservations(request):
    reservations = Reservation.for_user(request.user)
    return render(request, 'user_reservations.html', {'reservations': reservations})

# 예약 생성 API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    date = request.data.get('date')
    time = request.data.get('time')
    
    # Check if a reservation already exists for the given date and time
    if Reservation.objects.filter(date=date, time=time).exists():
        return Response({"error": "This time slot is already booked."}, status=400)
    
    serializer = ReservationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)  # Automatically link the reservation to the logged-in user
        return Response({"message": "Reservation created successfully"}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    return Response({
        "name": user.name,
        "email": user.email
    }, status=200)

# 단일 예약 조회 API
@api_view(['GET'])
def get_reservation(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=200)
    except Reservation.DoesNotExist:
        return Response({"error": f"Reservation with id {pk} not found"}, status=404)


# 모든 예약 조회 (관리자 전용)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_get_reservations(request):
    reservations = Reservation.objects.all()
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data, status=200)


# 예약 상태 업데이트 API
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_update_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    status = request.data.get('status')

    if status:
        reservation.status = status
        reservation.save()
        return Response({"message": "Reservation status updated"}, status=200)
    return Response({"error": "Status not provided"}, status=400)


# 예약 삭제 API (관리자 전용)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    reservation.delete()
    return Response({"message": f"Reservation {id} deleted successfully"}, status=200)


# 예약 수정 API
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_reservation(request, pk):
    try:
        user = request.user
        reservation = Reservation.objects.get(pk=pk, user=user)

        data = request.data
        if 'date' in data and 'time' in data:
            # Check if a reservation already exists for the given date and time
            if Reservation.objects.filter(date=data['date'], time=data['time']).exclude(pk=pk).exists():
                return Response({"error": "This time slot is already booked."}, status=400)
            reservation.date = data['date']
            reservation.time = data['time']
        if 'guests' in data:
            reservation.guests = data['guests']

        reservation.save()
        return Response({"message": "Reservation updated successfully"}, status=200)
    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found or unauthorized"}, status=404)
    except Exception as e:
        return Response({"error": "Something went wrong", "details": str(e)}, status=500)


# 예약 취소 API
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_reservation(request, pk):
    try:
        user = get_user_from_token(request)
        reservation = Reservation.objects.get(pk=pk, user=user)

        reservation.delete()
        return Response({"message": "Reservation canceled successfully"}, status=200)
    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found or unauthorized"}, status=404)
    except Exception as e:
        return Response({"error": "Something went wrong", "details": str(e)}, status=500)

class ReservationList(APIView):
    def get(self, request):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_menu(request):
    try:
        menu_items = Menu.objects.filter(is_available=True)
        serializer = MenuSerializer(menu_items, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user)
            logger.info(f"Fetching profile for user: {user.email}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Profile fetch error: {str(e)}")
            return Response(
                {"error": "Failed to fetch profile data"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def patch(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Profile updated for user: {user.email}")
                return Response(serializer.data)
            logger.error(f"Profile update validation error: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Profile update error: {str(e)}")
            return Response(
                {"error": "Failed to update profile"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserReservationsView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            return Reservation.objects.filter(user=self.request.user).order_by('-date', '-time')
        except Exception as e:
            logger.error(f"Error in UserReservationsView: {str(e)}")
            return Reservation.objects.none()

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

# views.py
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reservations_for_date(request, date):
    try:
        reservations = Reservation.objects.filter(date=date)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
