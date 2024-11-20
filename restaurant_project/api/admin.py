from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Reservation

# 커스텀 UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('name',)}),  # 추가 필드
    )
    list_display = (
        'id',
        'username',
        'email',
        'name',
        'is_staff',
        'is_superuser',
        'date_joined',
    )  # 사용자 목록에 표시될 필드
    search_fields = ('username', 'email', 'name')  # 검색 가능 필드
    ordering = ('-date_joined',)  # 최신 가입자 우선 정렬


# 예약(Reservation) 모델 관리
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'date',
        'time',
        'guests',
        'status',
        'created_at',
    )  # 관리자 페이지에서 표시할 필드
    search_fields = ('name', 'email')  # 검색 가능한 필드
    list_filter = ('date', 'time', 'status')  # 필터링 옵션
    actions = ['mark_as_confirmed', 'mark_as_cancelled']  # 커스텀 액션 추가

    # 예약 상태를 'confirmed'로 변경하는 액션
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(
            request, f"{updated} reservations have been marked as confirmed."
        )

    mark_as_confirmed.short_description = "Mark selected reservations as confirmed"

    # 예약 상태를 'cancelled'로 변경하는 액션
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(
            request, f"{updated} reservations have been marked as cancelled."
        )

    mark_as_cancelled.short_description = "Mark selected reservations as cancelled"


    # 로그인한 사용자에 맞춰 예약을 필터링하는 메서드
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # 관리자라면 모든 예약을 보여줌
        return queryset.filter(user=request.user)  # 일반 사용자는 자신의 예약만 볼 수 있음
