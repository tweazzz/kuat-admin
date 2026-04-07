from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import MainPage, Footer, PartnersSection, Partner, Request, Product, ProductCategory

User = get_user_model()


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "role")


class CreateEditorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.role = User.Role.EDITOR
        user.set_password(password)
        user.save()

        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")

        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Allows login by either username or email.
    Input stays the same:
    {
        "username": "editor1@mail.com",
        "password": "888kaz888"
    }
    or
    {
        "username": "editor1",
        "password": "888kaz888"
    }
    """

    def validate(self, attrs):
        identifier = attrs.get(self.username_field)
        password = attrs.get("password")

        if not identifier or not password:
            raise serializers.ValidationError(
                {"detail": "Both username/email and password are required."}
            )

        try:
            user = User.objects.get(
                Q(username__iexact=identifier) | Q(email__iexact=identifier)
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "No active account found with the given credentials."}
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                {"detail": "No active account found with the given credentials."}
            )

        attrs[self.username_field] = user.username

        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "role": self.user.role,
        }

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["username"] = user.username
        token["email"] = user.email
        return token
    


class MainPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPage
        fields = "__all__"



class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = "__all__"


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ("id", "name", "url", "logo")


class PartnersSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnersSection
        fields = ("id", "title", "subtitle")



class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"
        read_only_fields = ("id", "created_at")




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "category", "name", "description", "image")


class ProductCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = ProductCategory
        fields = ("id", "name", "description", "image", "products")


class ProductCategorySimpleSerializer(serializers.ModelSerializer):
    """Публичный список категорий без продуктов"""
    class Meta:
        model = ProductCategory
        fields = ("id", "name", "description", "image")