from .serializers import CustomTokenObtainPairSerializer, SnippetUserSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
class Logs(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignUp(CreateAPIView):
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request):
        ser = self.serializer_class(data= request.data)
        if ser.is_valid():
            user = ser.save()
            return Response(SnippetUserSerializer(user).data)
        return Response(ser.errors)