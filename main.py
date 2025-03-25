from supabase import create_client, Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# https://docs.render.com/deploy-fastapi

url: str = "https://hgbpcydzkwbaktcighhr.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhnYnBjeWR6a3diYWt0Y2lnaGhyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE4Mzk1MzMsImV4cCI6MjA1NzQxNTUzM30.5ui9tN-Yt9yIvma_t12dY4byCM9BdySkDEiCjplscvA"

supabase: Client = create_client(url, key)

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.post("/items/")
def create_item(item: Item):
    data = supabase.table("tasks").insert(item.dict()).execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=400, detail="Item could not be created")
    

@app.get("/items/")
def read_items():
    data = supabase.table("tasks").select("*").execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=404, detail="Items not found")
    

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    data = supabase.table("tasks").update(item.dict()).eq("id", item_id).execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    data = supabase.table("tasks").delete().eq("id", item_id).execute()
    if data.data:
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
