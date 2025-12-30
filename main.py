from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# هيكلية البيانات لضمان جودة الـ JSON [cite: 48]
class Account(BaseModel):
    name: str
    phone: int  
    national_id: int 
    account_type: str 
    balance: Optional[str] = "0 JOD"
    status: Optional[str] = "نشط" 

# قاعدة بيانات وهمية في الذاكرة
db = {}

# --- الـ Endpoint الرئيسية لإظهار كل الداتا ---
@app.get("/")
async def get_all_accounts():
    """تظهر جميع الحسابات التي تم إنشاؤها خلال الجلسة"""
    return {
        "total_accounts": len(db),
        "all_data": db
    }

# 1. [Create] - إنشاء حساب [cite: 4, 6]
@app.post("/bank/account/create")
async def create(account: Account):
    # نستخدم الرقم الوطني كمفتاح فريد في قاعدة البيانات [cite: 103, 138]
    db[str(account.national_id)] = account.dict()
    return {"status": "success", "message": f"Account created for {account.name}"}

# 2. [Read] - استعلام عن حساب معين [cite: 103, 138]
@app.get("/bank/account/details/{national_id}")
async def read(national_id: int): # تم التغيير لـ int للبحث
    n_id_str = str(national_id)
    if n_id_str in db:
        return db[n_id_str]
    raise HTTPException(status_code=404, detail="Account not found")

# 3. [Update] - تحديث بيانات [cite: 39, 159]
@app.patch("/bank/account/update")
async def update(national_id: int, field: str, value: str):
    n_id_str = str(national_id)
    if n_id_str in db:
        if field in db[n_id_str]:
            # إذا كان الحقل المراد تحديثه هو الهاتف أو الرقم الوطني، نحوله لـ int
            if field in ["phone", "national_id"]:
                db[n_id_str][field] = int(value)
            else:
                db[n_id_str][field] = value
            return {"status": "success", "updated_field": field, "new_value": value}
        raise HTTPException(status_code=400, detail="Field name is incorrect")
    raise HTTPException(status_code=404, detail="Account not found")

# 4. [Delete] - إغلاق الحساب [cite: 39, 170]
@app.delete("/bank/account/close")
async def delete(national_id: int): # تم التغيير لـ int
    n_id_str = str(national_id)
    if n_id_str in db:
        del db[n_id_str]
        return {"status": "success", "message": "Account closed permanently"}
    raise HTTPException(status_code=404, detail="Account not found")
