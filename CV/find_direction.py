import cv2
import numpy as np
import traceback


# Функция для поиска кругов с зеленым цветом
# и определения границы изображения
def find_green_circles_centroids(image):
    if image is None or image.size == 0:
        raise ValueError('Image cannot be empty.')

    # Конвертация изображения в HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Определение диапазона зеленого цвета в HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])

    # Применение порога к HSV изображению, чтобы получить только зеленые цвета
    mask = cv2.inRange(hsv, lower_green, upper_green)

    try:
        # Поиск контуров
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Фильтрация контуров, чтобы оставить только приблизительно круглые
        circles = [
            cnt for cnt in contours if cv2.contourArea(cnt) > 100 and
            4 * np.pi * (cv2.contourArea(cnt) / cv2.arcLength(cnt, True)**2)
            > 0.2
        ]

        # Расчет центроидов окружностей
        centroids = []
        for circ in circles:
            M = cv2.moments(circ)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                centroids.append((cx, cy))

        # print(centroids)
        return centroids
    except Exception as e:
        print(f"An error occurred while processing image: {image} {e}")
        traceback.print_exc()
        return []
