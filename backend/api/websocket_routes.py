from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime
import asyncio

from services.system_state import latest_state



router = APIRouter()


clients=[]



async def broadcast(data):

    disconnected=[]


    for client in clients:

        try:

            await client.send_json(data)


        except:

            disconnected.append(client)



    for client in disconnected:

        clients.remove(client)




@router.websocket("/ws/dashboard")
async def websocket_dashboard(
    websocket: WebSocket
):


    await websocket.accept()


    clients.append(websocket)



    try:


        while True:


            realtime = {


                "timestamp":

                datetime.now()
                .isoformat(),



                "status":

                latest_state["status"],



                "pipeline":

                latest_state["pipeline"],



                "quality_score":

                latest_state["quality_score"],



                "anomalies":

                latest_state["anomalies"],



                "repairs":

                latest_state["repairs"],



                "file":

                latest_state["last_file"]


            }



            await websocket.send_json(
                realtime
            )


            await asyncio.sleep(3)



    except WebSocketDisconnect:


        if websocket in clients:

            clients.remove(websocket)