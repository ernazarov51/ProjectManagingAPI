import json

from channels.generic.websocket import AsyncWebsocketConsumer

from apps.models import AssignHistory
from apps.serializers import AssignHistoryModelSerializer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            print("connected!")
            self.room_group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            # last_five_assign=AssignHistory.objects.filter(new_worker=self.user)[-5:]
            # serializer=AssignHistoryModelSerializer(last_five_assign,many=True)
            await self.send(text_data=json.dumps({"username":self.user.username}))

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            print("disconnect")
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def send_notification(self, event):
        print(json.dumps(event["data"]))
        await self.send(text_data=json.dumps(event["data"]))