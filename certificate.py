from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
import arabic_reshaper
import jdatetime
import io
from PIL import Image

def reshape_text(text):
    return get_display(arabic_reshaper.reshape(text))

def create_medical_certificate(first_name, last_name, sick_days, signature_data):
    # ثبت فونت فارسی
    pdfmetrics.registerFont(TTFont('IRANSans', 'IRANSans.ttf'))
    
    # ایجاد نام فایل
    file_name = f'{first_name}_{last_name}_certificate.pdf'
    
    # تنظیمات صفحه
    c = canvas.Canvas(file_name, pagesize=A3)
    width, height = A3
    
    # حاشیه
    margin = 50
    
    # رسم حاشیه
    c.setLineWidth(3)
    c.rect(margin, margin, width - 2*margin, height - 2*margin)
    
    # تنظیم فونت
    c.setFont('IRANSans', 16)
    
    # عنوان
    title = reshape_text("گواهی استعلاجی")
    c.drawCentredString(width / 2, height - margin - 30, title)
    
    # اطلاعات شخصی
    first_name_text = reshape_text(f"نام: {first_name}")
    last_name_text = reshape_text(f"نام خانوادگی: {last_name}")
    date_text = reshape_text(f"تاریخ: {jdatetime.date.today().strftime('%Y/%m/%d')}")
    sick_days_text = reshape_text(f"تعداد روزهای استعلاجی: {sick_days}")
    doctor_text = reshape_text("نام پزشک: دکتر احمدی")
    stamp_text = reshape_text("مهر:")
    additional_info = reshape_text("این گواهی جهت تایید مرخصی استعلاجی صادر شده است.")
    
    # چاپ از راست به چپ
    text_objects = [
        first_name_text, last_name_text, date_text,
        sick_days_text, additional_info,
        doctor_text, stamp_text
    ]
    
    y_positions = [
        height - margin - 70, height - margin - 100, height - margin - 130,
        height - margin - 160, height - margin - 200,
        height - margin - 240, height - margin - 270
    ]
    
    for text, y in zip(text_objects, y_positions):
        text_width = c.stringWidth(text, 'IRANSans', 16)
        c.drawString(width - text_width - margin - 10, y, text)
    
    # اضافه کردن امضا
    with Image.open(io.BytesIO(signature_data)) as img:
        temp_path = "temp_signature.jpg"
        img.save(temp_path)
        # محاسبه موقعیت برای قرار دادن امضا در وسط
        signature_width = 150
        signature_height = 50
        signature_x = (width - signature_width) / 2
        signature_y = height - margin - 350  # تنظیم ارتفاع برای بالاتر بردن امضا
        c.drawImage(temp_path, signature_x, signature_y, width=signature_width, height=signature_height)

    # پایان و ذخیره فایل
    c.save()
    print(f"فایل {file_name} با موفقیت ایجاد شد.")

# داده باینری تصویر امضا
signature_data = b'\xff\xd8\xff...'  # داده باینری تصویر امضا را اینجا قرار دهید

# مثال استفاده
create_medical_certificate("علی", "رضایی", 3, signature_data)