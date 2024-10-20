from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "This is FastAPI container 1"}

@app.get("/call_container2")
async def call_container2():
    url = "https://fastapi2:8001/"
    try:
        response = httpx.get(url, verify="/app/rootCA.crt")
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="server1.key", ssl_certfile="server1.crt", ssl_ca_certs="rootCA.crt")
