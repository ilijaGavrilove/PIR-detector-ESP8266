from aiohttp.abc import HTTPException
from fastapi import FastAPI
from bot.bot import bot
from database.db_requests import find_user_by_detector_id, find_name_by_detector_id, get_last_detector_id

from api.validation import AlertRequest

app = FastAPI()

@app.post("/motion")
async def user_alert(alert: AlertRequest):
    try:
        user_id = find_user_by_detector_id(alert.id)
        name = find_name_by_detector_id(alert.id)
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        await bot.send_message(chat_id=user_id, text=f"Обнаружено движение на датчике {name}!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

