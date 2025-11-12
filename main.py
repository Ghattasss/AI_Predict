from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# إعداد Google API
GOOGLE_API_KEY = "AIzaSyAeaRCWyUSndTSU3KpC4onaB_uZUMNChpo"
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# إنشاء تطبيق FastAPI
app = FastAPI()

# التصنيفات المتوقعة
labels = ["نعم", "لا", "بمساعدة"]

# نموذج البيانات المدخلة
class InputText(BaseModel):
    text: str

# دالة لاستخدام Gemini لتحديد الإجابة الصحيحة
def ask_gemini(user_answer):
    try:
        prompt = f"""
نحن نقوم بجمع إجابات من المستخدم على مجموعة من الأسئلة مثل:
هل يستطيع الطفل التعرف على الانفعال؟ هل يقدر يفهم شعور الآخر؟ وهكذا (عددها 28 سؤال تقريبًا).

الإجابات المتوقعة فقط هي واحدة من ثلاث خيارات:
1. نعم
2. لا
3. بمساعدة

الإجابة التي أدخلها المستخدم هي: "{user_answer}"

مهمتك هي تحديد أي من هذه الخيارات الثلاثة (نعم، لا، بمساعدة) تمثل هذه الإجابة بشكل أدق.
إذا كانت الإجابة غير واضحة أو لا تنتمي لأي من هذه الخيارات، قل فقط:
"الرجاء إدخال إجابة واضحة مثل: نعم، لا، بمساعدة."
"""
        response = gemini_model.generate_content(prompt)
        reply = response.text.strip()

        # استخراج التصنيف الصحيح من الرد
        for label in labels:
            if label in reply:
                return label

        return "الرجاء إدخال إجابة واضحة مثل: نعم، لا، بمساعدة"
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال بـ Gemini: {str(e)}"

# مسار التنبؤ
@app.post("/predict")
def predict(input: InputText):
    gemini_result = ask_gemini(input.text)
    return {
        "prediction": gemini_result,
        "model": "Gemini"
    }
