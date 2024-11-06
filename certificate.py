from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
import arabic_reshaper
import jdatetime
import io
from PIL import Image

from create_binary_of_image import binary_generator

def reshape_text(text):
    return get_display(arabic_reshaper.reshape(text))

def create_medical_certificate(first_name, last_name, sick_days, sick_name,):
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
    sick = reshape_text(f' نام بیماری:{sick_name}')
    doctor_text = reshape_text("نام پزشک: دکتر شبانی شهرضا")
    stamp_text = reshape_text("مهر:")
    additional_info = reshape_text("این گواهی جهت تایید استعلاجی نام برده صادر شده و تا 24 ساعت از صدور اعتبار دارد.")
    certificate = reshape_text('ویزیت آنلاین مدوگرام')
    link = reshape_text('medogram.ir')
    # چاپ از راست به چپ
    text_objects = [
        first_name_text, last_name_text, date_text,
        sick, sick_days_text, additional_info,
        doctor_text, stamp_text, certificate ,
          link
    ]
    
    y_positions = [
        height - margin - 70, height - margin - 100, height - margin - 130,
        height - margin - 160, height - margin - 200,
        height - margin - 240, height - margin - 270, height - margin - 300 , height - margin - 330,
    ]
    
    for text, y in zip(text_objects, y_positions):
        text_width = c.stringWidth(text, 'IRANSans', 16)
        c.drawString(width - text_width - margin - 10, y, text)
    
    signature_data = binary_generator()

    with Image.open(io.BytesIO(signature_data)) as img:
        temp_path = "temp_signature.png"
        img.save(temp_path)
        signature_width = 150
        signature_height = 50
        signature_x = (width - signature_width) / 2
        signature_y = height - margin - 350  
        c.drawImage(temp_path, signature_x, signature_y, width=signature_width, height=signature_height)

    
    c.save()
    print(f"فایل {file_name} با موفقیت ایجاد شد.")


create_medical_certificate("علی", "رضایی", 3, 'سرما خوردگی')