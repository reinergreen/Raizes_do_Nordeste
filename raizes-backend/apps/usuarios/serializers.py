from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'nome', 'email', 'perfil', 'telefone',
            'consentimento_fidelidade', 'data_consentimento_fidelidade'
        ]
        read_only_fields = ['id', 'data_consentimento_fidelidade']


class UsuarioCreateSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'senha', 'telefone', 'perfil', 'consentimento_fidelidade']
        read_only_fields = ['id']

    def validate_perfil(self, value):
        request = self.context.get('request')
        if value != Usuario.Perfil.CLIENTE and not (request and request.user.is_authenticated and request.user.perfil in ['ADMIN', 'GERENTE']):
            raise serializers.ValidationError('Somente gerente/admin pode criar usuário com perfil interno.')
        return value

    def create(self, validated_data):
        senha = validated_data.pop('senha')
        return Usuario.objects.create_user(password=senha, **validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        data = super().validate(attrs)
        data['tokenType'] = 'Bearer'
        data['expiresIn'] = 3600
        data['user'] = UsuarioSerializer(self.user).data
        return data
