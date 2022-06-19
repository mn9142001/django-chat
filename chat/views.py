from user.models import User
from django.shortcuts import get_object_or_404
from .serializers import MessageSerializer, MessageListSerializer
from rest_framework import response, viewsets
from .models import Message
from django.db.models import Q
from user.serializers import SnippetUserSerializer
from project.permissions import SnippetUpdateDeletePermission


class MessagesView(viewsets.ModelViewSet):
	serializer_class = MessageSerializer
	permission_classes = (SnippetUpdateDeletePermission, )
	queryset = Message.objects.all()

	def list(self, request):
		sliders = request.user.chatted_with.all()
		return response.Response(MessageListSerializer(sliders, many=True, context = {'user': request.user}).data, status=200)

	def retrieve(self, request, pk):
		partner = get_object_or_404(User, pk=pk)
		sliders = request.user.chatted_with.all()
		messages = Message.objects.filter((Q(receiver = request.user, sender = partner) | Q(sender=request.user, receiver = partner))).order_by('-date')[:20]
		return response.Response({'slidem':MessageListSerializer(sliders, many=True, context = {'user': request.user}).data,'partner': SnippetUserSerializer(partner).data, 'messages': reversed(self.serializer_class(messages, many=True).data)}, status=200)
