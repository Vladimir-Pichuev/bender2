import cv2
import numpy as np

def open_filename(resized_image):
    # Конвертация изображения в HSV
    hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

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
        # Нарисовать круги на изображении
        for i in circles[0, :]:
            # Обвести внешний круг зелёным цветом
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
