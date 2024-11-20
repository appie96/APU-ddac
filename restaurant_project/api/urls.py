from django.urls import path
from . import views
from .views import (
    register,
    login,
    create_reservation,
    get_reservation,
    admin_get_reservations,
    admin_update_reservation,
    admin_delete_reservation,
    update_reservation,
    cancel_reservation,
    ReservationList,
    UserProfileView,
    UserReservationsView,
    ReservationDetailView,
)

urlpatterns = [
    # 회원가입
    path('register', register, name='register'),

    # 로그인
    path('login', views.login, name='login'),

    # 예약 생성
    path('reservation', create_reservation, name='create_reservation'),

    # 단일 예약 조회
    path('reservation/<int:pk>/', get_reservation, name='get_reservation'),

    # 모든 예약 조회 (관리자)
    path('admin/reservations/', admin_get_reservations, name='admin_get_reservations'),

    # 예약 상태 업데이트 (관리자)
    path('admin/reservations/<int:id>/', admin_update_reservation, name='admin_update_reservation'),

    # 예약 삭제 (관리자)
    path('admin/reservations/<int:id>/delete/', admin_delete_reservation, name='admin_delete_reservation'),

    # 예약 수정 (사용자)
    path('reservation/<int:pk>/update/', update_reservation, name='update_reservation'),

    # 예약 취소 (사용자)
    path('reservation/<int:pk>/cancel/', cancel_reservation, name='cancel_reservation'),
    
    path('my-reservations/', views.user_reservations, name='user_reservations'),

    path('reservations/', ReservationList.as_view(), name='reservation-list'),
    
    path('user-info', views.user_info, name='user_info'),

    path('menu/', views.get_menu, name='get_menu'),
    
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
    
    path('reservations/my/', UserReservationsView.as_view(), name='user-reservations'),
    
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),

    path('reservations/date/<str:date>/', views.get_reservations_for_date, name='reservations-for-date'),
]
