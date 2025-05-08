from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str

db: Dict[int, Item] = {}
id_counter = 1

@app.get("/items/")
def list_items():
    return db


@app.post("/items/")
def create_item(item: Item):
    global id_counter
    db[id_counter] = item
    id_counter += 1
    return {"id": id_counter - 1, **item.dict()}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]
