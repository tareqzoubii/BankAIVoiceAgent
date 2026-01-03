from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI()

# هيكلية البيانات المطورة
class Account(BaseModel):
    name: str
    phone: str          # تم التغيير لنص لضمان الصفر البادئ
    national_id: str    # تم التغيير لنص للتوافق مع الـ Agent
    account_type: str 
    balance: Optional[str] = "150 JOD" # رصيد افتراضي للتجربة
    status: Optional[str] = "نشط" 

# قاعدة بيانات وهمية تحتوي على بيانات أولية للتست
db: Dict[str, dict] = {
    "9901012345": {
        "name": "أحمد علي الروابدة",
        "phone": "0791234567",
        "national_id": "9901012345",
        "account_type": "توفير",
        "balance": "1250 JOD",
        "status": "نشط"
    },
    "9952028899": {
        "name": "ليلى محمود القضاة",
        "phone": "0777987654",
        "national_id": "9952028899",
        "account_type": "جاري",
        "balance": "430 JOD",
        "status": "نشط"
    }
}

@app.get("/")
async def root():
    return {
    "message": "Bank AI Voice System is Running",
    "total_accounts": len(db),
    "accounts": db
}

# 1. إنشاء حساب
@app.post("/bank/account/create")
async def create(account: Account):
    db[account.national_id] = account.dict()
    return {"status": "success", "message": f"تم إنشاء حسابك بنجاح يا {account.name}"}

# 2. استعلام عن حساب (Read)
# التعديل الجديد للـ Read لضمان عمل الرابط بسهولة
@app.get("/bank/account/details") # حذفنا /{national_id} من هنا
async def read(national_id: str): # سيبقى كما هو هنا
    if national_id in db:
        return db[national_id]
    raise HTTPException(status_code=404, detail="الحساب غير موجود not found")

# 3. تحديث البيانات (Update)
@app.patch("/bank/account/update")
async def update(national_id: str, field: str, value: str):
    if national_id in db:
        if field in db[national_id]:
            db[national_id][field] = value
            return {"status": "success", "message": f"تم تحديث {field} بنجاح"}
        raise HTTPException(status_code=400, detail="الحقل المطلوب غير موجود")
    raise HTTPException(status_code=404, detail="الحساب غير موجود")

# 4. إغلاق الحساب (Delete)
@app.delete("/bank/account/close")
async def delete(national_id: str):
    if national_id in db:
        del db[national_id]
        return {"status": "success", "message": "تم إغلاق الحساب نهائياً"}
    raise HTTPException(status_code=404, detail="الحساب غير موجود")
