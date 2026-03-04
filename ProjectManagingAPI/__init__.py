# import asyncio
# import websockets
# import json
#
# async def listen_logs():
#     uri = "ws://localhost:8080"
#     async with websockets.connect(uri) as websocket:
#         print("Node.js serverga ulandi, real-time log kutilyapti...")
#         async for message in websocket:
#             log = json.loads(message)
#             print(f"Hodim ID: {log['userId']}  | Vaqt: {log['time']}")
#
# if __name__ == "__main__":
#     asyncio.run(listen_logs())
