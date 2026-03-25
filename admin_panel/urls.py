from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ChangePasswordView,
    CreateEditorView,
    MeView,
    MyTokenObtainPairView, MainPageView, FooterView, PartnersSectionView
)

urlpatterns = [
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/me/", MeView.as_view(), name="me"),
    path("api/users/", CreateEditorView.as_view(), name="create_editor"),
    path("api/change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("api/main-page/", MainPageView.as_view()),
    path("api/footer/", FooterView.as_view(), name="footer"),
    path("api/partners/", PartnersSectionView.as_view(), name="partners-section"),
]