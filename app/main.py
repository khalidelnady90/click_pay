from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, auth

# إنشاء التطبيق
app = FastAPI()

# إعدادات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontenddomain.com"],  # تحديد النطاقات المسموح بها فقط
    allow_credentials=True,
    allow_methods=["*"],  # أو تحديد الطرق المسموح بها مثل ["GET", "POST"]
    allow_headers=["*"],  # تحديد الهيدرز المسموح بها إن لزم الأمر
)

# تضمين الراوترات بعد تهيئة التطبيق لتجنب الدورة الاستيرادية
from .users import router as users_router
from .transactions import router as transactions_router

app.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
app.include_router(users_router, prefix="/users", tags=["users"])

# إنشاء الجداول في قاعدة البيانات
models.Base.metadata.create_all(bind=database.engine)

# تضمين الراوترات الخاصة بالتوثيق
from .auth import router as auth_router
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Click Pay API is running 🚀"}

