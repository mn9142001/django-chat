from user.models import User
from django.shortcuts import get_object_or_404
from .serializers import MessageSerializer, MessageListSerializer
from rest_framework import response, permissions, viewsets, status
from .models import Message, MessageMedia
from django.db.models import Q
from user.serializers import SnippetUserSerializer
from .signals import afterMessage
# Create your views here.

class MessagesView(viewsets.ViewSet):
	serializer_class = MessageSerializer
	def list(self, request):
		sliders = request.user.chatted_with.all()
		return response.Response(MessageListSerializer(sliders, many=True, context = {'user': request.user}).data, status=status.HTTP_200_OK)

	def retrieve(self, request, pk):
		partner = get_object_or_404(User, pk=pk)
		sliders = request.user.chatted_with.all()
		
		messages = list(Message.objects.filter((Q(receiver = request.user, sender = partner) | Q(sender=request.user, receiver = partner))).order_by('-date') )[:20]

		return response.Response({'slidem':MessageListSerializer(sliders, many=True, context = {'user': request.user}).data,'partner': SnippetUserSerializer(partner).data, 'messages': reversed(self.serializer_class(messages, many=True).data)}, status=status.HTTP_200_OK)
	
	def create(self, request):
		ser = self.serializer_class(data=request.data)
		if ser.is_valid():
			obj = ser.save(sender=request.user)
			if request.data.get('media') and int(request.data.get('media')) > 0:
				MessageMedia.objects.bulk_create([MessageMedia(media=request.data.get(f"img_{str(x)}"), message = obj) for x in range(request.data.get('media'))])
			afterMessage(obj)
			return response.Response({'message': "wait"}, status = status.HTTP_200_OK)

		return response.Response(ser.errors)

	def destroy(self, request, pk):
		message = get_object_or_404(Message, pk=pk)
		if request.user == message.sender:
			message.delete()			
			return response.Response(True, status=status.HTTP_200_OK)
		return response.Response(False, status = status.HTTP_403_FORBIDDEN)
