from fastapi import Request

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
    except:
        data = {}

    print("DATA RECIBIDA:", data)

    return {"status": "ok"}
