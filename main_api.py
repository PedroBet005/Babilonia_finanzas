from fastapi import FastAPI

app = FastAPI(title="Babilonia Finanzas API")

@app.get("/health")
def health():
    return {"status": "ok"}
