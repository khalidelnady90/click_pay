from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# الاتصال بقاعدة بيانات SQLite (ممكن تغيرها لأي قاعدة تانية)
SQLALCHEMY_DATABASE_URL = "sqlite:///./clickpay.db"

# إعداد المحرك (engine)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# إعداد الجلسة
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# إعداد قاعدة النماذج
Base = declarative_base()

# دالة get_db
def get_db():
    db = SessionLocal()  # إنشاء جلسة جديدة
    try:
        yield db  # إرجاع الجلسة لاستخدامها في المكان الذي تحتاجه
    finally:
        db.close()  # بعد الانتهاء من الجلسة، إغلاق الاتصال بالقاعدة
