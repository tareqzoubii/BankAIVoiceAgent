from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# هيكلية البيانات (Schema) لضمان جودة الـ JSON [cite: 48]
class Account(BaseModel):
    name: str
    phone: str
    national_id: str
    account_type: str
    balance: Optional[str] = "0 JOD"
    status: Optional[str] = "نشط"

# قاعدة بيانات وهمية
db = {}

# 1. [Create] - إنشاء حساب [cite: 4, 6]
@app.post("/bank/account/create")
async def create(account: Account):
    db[account.national_id] = account.dict()
    return {"status": "success", "message": "Account created for " + account.name}

# 2. [Read] - استعلام [cite: 103, 138]
@app.get("/bank/account/details/{national_id}")
async def read(national_id: str):
    if national_id in db:
        return db[national_id]
    raise HTTPException(status_code=404, detail="Account not found")

# 3. [Update] - تحديث [cite: 39, 159]
@app.patch("/bank/account/update")
async def update(national_id: str, field: str, value: str):
    if national_id in db:
        db[national_id][field] = value
        return {"status": "success", "updated": field}
    raise HTTPException(status_code=404, detail="Not found")

# 4. [Delete] - إغلاق الحساب [cite: 39, 170]
@app.delete("/bank/account/close")
async def delete(national_id: str):
    if national_id in db:
        del db[national_id]
        return {"status": "success", "message": "Account closed"}
    raise HTTPException(status_code=404, detail="Not found")
