import cv2
import numpy as np

def open_filename(resized_image):
    # Конвертация изображения в HSV
    hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

    # Определяем некую область в левом нижнем углу
    roi_size = 50  # Размер ROI
    roi = resized_image[-roi_size:, :roi_size]
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    roi_brightness = np.mean(roi_gray)
    print(f"Средняя яркость в левом нижнем углу: {roi_brightness}")

    # Изолировать красный цвет
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # Создать маску для красного цвета в HSV
    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Применение маски к изображению
    red_only = cv2.bitwise_and(resized_image, resized_image, mask=mask)

    # Преобразование в оттенки серого для обнаружения кругов
    gray_image = cv2.cvtColor(red_only, cv2.COLOR_BGR2GRAY)

    # Уменьшение шума перед обнаружением кругов
    blurred_image = cv2.GaussianBlur(gray_image, (9, 9), 2)

    # Обнаружение кругов
    circles = cv2.HoughCircles(blurred_image, cv2.HOUGH_GRADIENT,
                               dp=1.2, minDist=50,
                               param1=50, param2=30, minRadius=10, maxRadius=100)

    if circles is not None:
        circles = np.uint16(np.around(circles))
    print(f"Обнаружено кругов: {circles.shape[1]}")

    for i in circles[0, :]:
        print(f"Круг: (x={i[0]}, y={i[1]}), радиус={i[2]}")
        
        # Определяем область 10x10 вокруг центра круга
        x_start = max(0, i[0] - 5)
        x_end = min(resized_image.shape[1], i[0] + 5)
        y_start = max(0, i[1] - 5)
        y_end = min(resized_image.shape[0], i[1] + 5)
        
        # Выбираем область 10x10
        roi = resized_image[y_start:y_end, x_start:x_end]
        
        # Посчитать среднюю яркость в этой области
        brightness = np.mean(roi)
        # Считаем относительную яркость в этой области
        relative_brightness = brightness / roi_brightness
        print(f"Яркость в области 10x10 вокруг центра круга: {brightness}, Относительная яркость: {relative_brightness}")
        
        # Нарисовать круги на изображении
        cv2.circle(resized_image, (i[0], i[1]), i[2], (0, 255, 0), 2)
    else:
        print("Круги не обнаружены. в функции find_color_circle_2")

    # Показать изображение с обнаруженными кругами
    cv2.imshow("Detected Circles", resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Пример использования функции
resized_image = cv2.imread('CV/new_files/qr_circle_rotate_cut.png')
if resized_image is not None:
    open_filename(resized_image)
else:
    print("Не удалось загрузить изображение.")
