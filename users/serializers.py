from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

from users.models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects)]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = 'username', 'email', 'password', 'password2', 'nickname'

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('password', 'Password fields didn\'t match.')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        profile = Profile(user=user, nickname=validated_data['nickname'])
        profile.save()

        token = Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user:
            token = Token.objects.create(user=user)
            return token
        raise serializers.ValidationError('error', 'Invalid credentials.')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = 'nickname', 'image'


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = 'id', 'username', 'email', 'profile', 'password'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'nickname': instance.profile.nickname,
            'image': str(instance.profile.image)
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(**profile_data, id=user.id)
        user.set_password(validated_data['password'])
        return

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        print(validated_data)
        if profile_data:
            instance.profile.nickname = validated_data['nickname']
            instance.profile.image = validated_data['image']
            instance.profile.save()
        return super().update(instance, validated_data)
