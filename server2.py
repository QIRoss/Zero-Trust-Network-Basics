from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "This is FastAPI container 2"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, ssl_keyfile="server2.key", ssl_certfile="server2.crt", ssl_ca_certs="rootCA.crt")
