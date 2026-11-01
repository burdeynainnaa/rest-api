from django.contrib.auth.models import User
from rest_framework import serializers
import re

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_confirmation",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def validate_password(self, value):
        """
        Перевірка складності пароля:
        - Мінімум 8 символів (також перевіряється min_length=8)
        - Хоча б одна велика літера (A-Z)
        - Хоча б одна мала літера (a-z)
        - Хоча б одна цифра (0-9)
        - Хоча б один спеціальний символ
        """
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Пароль повинен містити хоча б одну велику літеру (A-Z).")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Пароль повинен містити хоча б одну малу літеру (a-z).")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Пароль повинен містити хоча б одну цифру (0-9).")
        if not re.search(r'[@$!%*?&._]', value):
            raise serializers.ValidationError("Пароль повинен містити хоча б один спеціальний символ (наприклад, @, $, !, %, *, ?, &, ., _).")
        return value

    def validate(self, data):
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError(
                {"password": "Паролі не збігаються."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirmation")
        
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            password=validated_data["password"],
        )
        return user