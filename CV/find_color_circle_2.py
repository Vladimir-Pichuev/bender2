import cv2
import numpy as np

def open_filename(resized_image):
    # Преобразовать изображение в HSV
    hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

    # Определить область интереса в левом нижнем углу
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

    # Применить маску к изображению
    red_only = cv2.bitwise_and(resized_image, resized_image, mask=mask)

    # Преобразовать в оттенки серого для обнаружения кругов
    gray_image = cv2.cvtColor(red_only, cv2.COLOR_BGR2GRAY)

    # Обнаружение краев с помощью канни
    edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)

    # Найти контуры краев
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Фильтровать контуры для поиска кругов
    circles = []
    for cnt in contours:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        if radius > 0:  # Убедиться, что радиус положительный
            circles.append((center, radius))

    print(f"Найдено кругов: {len(circles)}")

    for center, radius in circles:
        print(f"Круг: (x={center[0]}, y={center[1]}), радиус={radius}")

        # Определить область 10x10 вокруг центра круга
        x_start = max(0, center[0] - 5)
        x_end = min(resized_image.shape[1], center[0] + 5)
        y_start = max(0, center[1] - 5)
        y_end = min(resized_image.shape[0], center[1] + 5)

        # Выбрать область 10x10
        roi = resized_image[y_start:y_end, x_start:x_end]

        # Вычислить среднюю яркость в этой области
        brightness = np.mean(roi)
        # Вычислить относительную яркость в этой области
        relative_brightness = brightness / roi_brightness
        print(f"Яркость в области 10x10 вокруг центра круга: {brightness}, Относительная яркость: {relative_brightness}")

        # Нарисовать круги на изображении
        cv2.circle(resized_image, center, radius, (0, 255, 0), 2)

    # Показать изображение с обнаруженными кругами
    cv2.imshow("Обнаруженные круги", resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

"""
# Пример использования функции
resized_image = cv2.imread('CV/new_files/qr_circle_rotate_cut.png')
if resized_image is not None:
    open_filename(resized_image)
else:
    print("Не удалось загрузить изображение.")
"""