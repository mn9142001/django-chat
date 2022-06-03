from rest_framework import serializers
from django.db.models import Q
from user.serializers import SnippetUserSerializer
from .models import Message, MessageMedia


class MessageMedia(serializers.ModelSerializer):

	class Meta:
		model = MessageMedia
		fields = ('id', 'media')


class MessageReply(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ('id', 'content',)


class MessageSerializer(serializers.ModelSerializer):
	media = MessageMedia(source='messageMedia', many=True, required = False)
	reply = MessageReply(required = False)
	sender = SnippetUserSerializer(required = False)

	# def senderM(self, m):
	# 	return m.sender.id

	class Meta:
		model = Message
		fields = ('id', 'sender', 'receiver', 'content', 'record',
				  'date', 'reply', 'state', 'media',)

class MessageListSerializer(serializers.ModelSerializer):
	last_m = serializers.SerializerMethodField(method_name='last_message')
	sender = serializers.SerializerMethodField(method_name='userM')

	class Meta:
		model = Message
		fields = ('last_m', 'sender')

	
	def userM(self, user):
		return SnippetUserSerializer(user).data

	def last_message(self, partner):
		user = self.context.get('user')
		message =  MessageSerializer(Message.objects.filter((Q(receiver = user, sender = partner) | Q(sender=user, receiver = partner))).last()).data
		return message