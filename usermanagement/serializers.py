from rest_framework import serializers
from .models import UserAccount
from django.contrib.auth.hashers import make_password


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'
        read_only_fields = ['uid']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            hashed_password = make_password(password)
            instance.password = hashed_password
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # Hide password from serialized output
    password = serializers.CharField(write_only=True)

    class Meta:
        extra_kwargs = {
            'password': {'write_only': True}
        }

        def validate(self, attrs):
            # Accessing context data
            request = self.context.get('request')
            user = self.context.get('user')
            print(user)

        # You can now use request and user as needed for validation logic
        # For example, validating based on user permissions or request metadata
            if user and not user.is_authenticated:
                raise serializers.ValidationError(
                    "User must be authenticated.")

            return attrs



class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}