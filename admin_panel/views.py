from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import MainPage, Footer, PartnersSection, Request, ProductCategory, Product
from .serializers import MainPageSerializer, RequestSerializer
from .permissions import IsSuperAdmin
from .serializers import (
    ChangePasswordSerializer,
    CreateEditorSerializer,
    MyTokenObtainPairSerializer,
    UserReadSerializer, FooterSerializer,PartnersSectionSerializer, ProductCategorySerializer, ProductCategorySimpleSerializer, ProductSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsSuperAdmin

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserReadSerializer(request.user).data)


class CreateEditorView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request):
        serializer = CreateEditorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserReadSerializer(user).data, status=status.HTTP_201_CREATED)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
    


class MainPageView(APIView):
    def get_permissions(self):
        """
        Разделяем permissions по методу:
        - GET → AllowAny()
        - Остальные → IsAuthenticated + IsSuperAdmin
        """
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsSuperAdmin()]

    def get_object(self):
        obj, _ = MainPage.objects.get_or_create(id=1)
        return obj

    def handle_update(self, request, partial=False, status_code=status.HTTP_200_OK):
        page = self.get_object()
        serializer = MainPageSerializer(page, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status_code)

    # GET
    def get(self, request):
        page = self.get_object()
        serializer = MainPageSerializer(page)
        return Response(serializer.data)

    def post(self, request):
        return self.handle_update(request, partial=False, status_code=status.HTTP_201_CREATED)

    def put(self, request):
        return self.handle_update(request, partial=False)

    def patch(self, request):
        return self.handle_update(request, partial=True)

    def delete(self, request):
        page = self.get_object()
        page.delete()
        return Response({"detail": "Main page deleted"}, status=status.HTTP_204_NO_CONTENT)
    

class FooterView(APIView):
    """
    Footer API:
    GET -> public
    POST / PUT / PATCH / DELETE -> only Super Admin
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self):
        obj, _ = Footer.objects.get_or_create(pk=1)
        return obj

    def serialize(self, instance):
        return FooterSerializer(instance).data

    def update_footer(self, request, partial=False, created_status=False):
        footer = self.get_object()
        serializer = FooterSerializer(footer, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created_status else status.HTTP_200_OK,
        )

    def get(self, request):
        footer = self.get_object()
        return Response(self.serialize(footer), status=status.HTTP_200_OK)

    def post(self, request):
        return self.update_footer(request, partial=False, created_status=True)

    def put(self, request):
        return self.update_footer(request, partial=False, created_status=False)

    def patch(self, request):
        return self.update_footer(request, partial=True, created_status=False)

    def delete(self, request):
        footer = self.get_object()
        footer.delete()
        return Response(
            {"detail": "Footer deleted"},
            status=status.HTTP_204_NO_CONTENT
        )
    

class PartnersSectionView(APIView):
    """
    GET    -> public
    POST   -> Super Admin
    PUT    -> Super Admin
    PATCH  -> Super Admin
    DELETE -> Super Admin
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsSuperAdmin()]

    def get_object(self):
        obj, _ = PartnersSection.objects.get_or_create(pk=1)
        return obj

    def get(self, request):
        section = self.get_object()
        serializer = PartnersSectionSerializer(section, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        section = self.get_object()
        serializer = PartnersSectionSerializer(
            section,
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        section = self.get_object()
        serializer = PartnersSectionSerializer(
            section,
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        section = self.get_object()
        serializer = PartnersSectionSerializer(
            section,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        section = self.get_object()
        section.delete()
        return Response(
            {"detail": "Partners section deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
    


class RequestView(APIView):
    """
    POST   -> public (без токена)
    GET    -> admin only
    PUT    -> admin only
    PATCH  -> admin only
    """

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        queryset = Request.objects.all()
        serializer = RequestSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        obj = Request.objects.get(pk=pk)
        serializer = RequestSerializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        obj = Request.objects.get(pk=pk)
        serializer = RequestSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    


# ------------------------------
# ProductCategory API
# ------------------------------
class ProductCategoryView(APIView):
    """GET -> public, POST/PUT/PATCH/DELETE -> admin"""

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return ProductCategory.objects.prefetch_related("products").all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = ProductCategorySerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductCategoryDetailView(APIView):
    """GET -> public, PUT/PATCH/DELETE -> admin"""

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        return ProductCategory.objects.prefetch_related("products").get(pk=pk)

    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = ProductCategorySerializer(obj, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = ProductCategorySerializer(obj, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        serializer = ProductCategorySerializer(obj, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response({"detail": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)


class ProductCategorySimpleView(APIView):
    """GET -> публичный список категорий без продуктов"""
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = ProductCategory.objects.all()
        serializer = ProductCategorySimpleSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


# ------------------------------
# Product API
# ------------------------------
class ProductView(APIView):
    """GET -> public, POST/PUT/PATCH/DELETE -> admin"""

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return Product.objects.select_related("category").all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        obj = Product.objects.get(pk=pk)
        serializer = ProductSerializer(obj, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        obj = Product.objects.get(pk=pk)
        serializer = ProductSerializer(obj, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        obj = Product.objects.get(pk=pk)
        obj.delete()
        return Response({"detail": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)