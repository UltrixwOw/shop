import json
from channels.generic.websocket import AsyncWebsocketConsumer


class StockConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            "stock",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "stock",
            self.channel_name
        )

    async def stock_update(self, event):
        await self.send(text_data=json.dumps({
            "product_id": event["product_id"],
            "stock": event["stock"],
        }))