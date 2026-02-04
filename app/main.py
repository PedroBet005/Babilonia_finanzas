from fastapi import FastAPI

app = FastAPI(
    title="Babilonia Finanzas",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"status": "Babilonia Finanzas API funcionando"}
