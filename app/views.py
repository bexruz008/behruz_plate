import cv2
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
import pytesseract
import os
import uuid  # UUID yaratish

from app.models import Plate

# Tesseract binarini aniqlash
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


@api_view(['POST'])
def process_plates(request):
    if request.method == 'POST':
        # Haarcascade modelini yuklab olish
        plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

        # VideoCapture obyektini yaratish
        cap = cv2.VideoCapture(0)  # 0 - birinchi kamerani ishlatish

        detected_plates = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Tasvirni qora rangga o'tkazish
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            plates = plate_cascade.detectMultiScale(gray, 1.1, 5)

            for (x, y, w, h) in plates:
                plate_img = gray[y:y+h, x:x+w]
                plate_text = pytesseract.image_to_string(plate_img,)

                # Ma'lumotlar bazasida borligini tekshirish
                existing_plate = Plate.objects.filter(plate_number=plate_text).first()

                if existing_plate is None:
                    # Ma'lumotlar bazasiga yangi ma'lumot qo'shish
                    entry_time = datetime.now()
                    new_plate = Plate.objects.create(
                        plate_number=plate_text,
                        entry_time=entry_time
                    )
                    detected_plates.append({
                        "plate_number": plate_text,
                        "entry_time": entry_time,
                        "image": f"/{plate_text}_{uuid.uuid4()}.jpg"  # Rasmlar uchun benzersiz dosya adı
                    })

                    # Raqamni rasmga yozish
                    save_plate_image(plate_img, plate_text, uuid.uuid4())

                else:
                    # Mashina chiqgan vaqtni yangilash
                    existing_plate.exit_time = datetime.now()
                    existing_plate.save()

            cv2.imshow('Frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return Response(detected_plates, status=status.HTTP_200_OK)


def save_plate_image(image, plate_text, unique_id):
    # Rasmni saqlash uchun papka
    save_directory = 'images'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Rasmni saqlash uchun fayl nomi
    file_path = os.path.join(save_directory, f'{plate_text}_{unique_id}.jpg')

    # Rasmni saqlash
    cv2.imwrite(file_path, image)

    # Yo'lning to'g'ri bo'lib bo'lmaganligini tekshirish
    if os.path.exists(file_path):
        print(f"Rasm {file_path} ga saqlandi.")
    else:
        print("Rasmni saqlashda xatolik yuz berdi.")