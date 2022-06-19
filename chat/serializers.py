from rest_framework import serializers
from django.db.models import Q
from media.serializers import MessageFileSerializer
from user.serializers import SnippetUserSerializer
from .models import Message
from media.models import MessageFile
from .signals import afterMessage

class BaseMessageSerializer(serializers.ModelSerializer):
	media = MessageFileSerializer(source="message_files",required=False, many=True)
	sender = SnippetUserSerializer(default=serializers.CurrentUserDefault(),required = False)

	class Meta:
		model = Message
		abstract = True
		fields = ('id', 'content', 'date', 'record', 'reply', 'media', 'sender', 'receiver')

	@property
	def request(self):
		return self.context.get('request')



class MessageReply(BaseMessageSerializer):
	class Meta(BaseMessageSerializer.Meta):
		model = Message
		fields = BaseMessageSerializer.Meta.fields


class MessageSerializer(BaseMessageSerializer):
	reply = MessageReply(required = False)

	class Meta(BaseMessageSerializer.Meta):
		fields = BaseMessageSerializer.Meta.fields + ('media', )

	def validate(self, validated_data):
		if not (validated_data.get('content'), self.request.files.get('media')):
			return serializers.ValidationError("you cannot make blank messages.")
		return validated_data

	def create(self, data):
		_files = self.request.FILES.getlist('media')
		obj = super().create(data)
		if _files:
			MessageFile.objects.bulk_create([MessageFile(img = file, message=obj) for file in _files])

		afterMessage(MessageSerializer(obj).data)
		return obj

class ChatSerializer(serializers.Serializer):
	messages = serializers.SerializerMethodField(method_name='get_messages')
	partner = serializers.SerializerMethodField(method_name='get_partner')

	def get_partner(self, partner):
		return SnippetUserSerializer(partner).data

	def get_messages(self, partner):
		messages = Message.objects.filter((Q(receiver = self.context.get('request').user, sender = partner) | Q(sender=self.context.get('request').user, receiver = partner)))
		return MessageSerializer(messages, many=True).data

	class Meta:
		fields = ('messages', 'partner',)

class MessageListSerializer(BaseMessageSerializer):
	last_m = serializers.SerializerMethodField(method_name='last_message')
	reply = MessageReply(required = False)

	class Meta(BaseMessageSerializer.Meta):
		fields = BaseMessageSerializer.Meta.fields + ('last_m',)


	def last_message(self, partner):
		user = self.request.user
		message =  MessageSerializer(Message.objects.filter((Q(receiver = user, sender = partner) | Q(sender=user, receiver = partner))).last()).data
		return message
