# استخدم صورة رسمية من Python
FROM python:3.10-slim

# تعيين مسار العمل داخل الحاوية
WORKDIR /app

# نسخ الملفات إلى الحاوية
COPY . .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# فتح البورت الذي سيعمل عليه FastAPI
EXPOSE 8080

# الأمر لتشغيل التطبيق
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
