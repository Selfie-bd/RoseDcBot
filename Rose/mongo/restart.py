from Rose.mongo import restartdb

async def start_restart_stage(chat_id: int, message_id: int):
    await restartdb.update_one(
        {"something": "something"},
        {
            "$set": {
                "chat_id": chat_id,
                "message_id": message_id,
            }
        },
        upsert=True,
    )

async def clean_restart_stage() -> dict:
    data = await restartdb.find_one({"something": "something"})
    if not data:
        return {}
    await restartdb.delete_one({"something": "something"})
    return {
        "chat_id": data["chat_id"],
        "message_id": data["message_id"],
    }