from django.shortcuts import get_object_or_404
from user.models import User
from django.db.models import Q
from .serializers import MessageSerializer, MessageListSerializer
from rest_framework import response, viewsets
from .models import Message
# Create your views here.
from project.permissions import SnippetUpdateDeletePermission


class MessagesView(viewsets.ModelViewSet):
	serializer_class = MessageSerializer
	permission_classes = (SnippetUpdateDeletePermission, )
	queryset = Message.objects.all()

	def list(self, request):
		sliders = request.user.chatted_with.all()
		return response.Response(MessageListSerializer(sliders, many=True, context = {'request': request}).data, status=200)

	def retrieve(self, request, pk):
		partner = get_object_or_404(User, pk=pk)
		self.queryset = Message.objects.filter((Q(receiver = request.user, sender = partner) | Q(sender=request.user, receiver = partner)))
		return super().list(request, pk)
