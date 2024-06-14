import cv2
import numpy as np
import traceback


# Функция для поиска кругов с зеленым цветом
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
            > 0.7
        ]

        # Расчет центроидов окружностей
        centroids = []
        for circ in circles:
            M = cv2.moments(circ)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                centroids.append((cx, cy))

        return centroids
    except Exception as e:
        print(f"An error occurred while processing image: {image} {e}")
        traceback.print_exc()
        return []


# Загрузка изображения
image = cv2.imread('CV/qr_circle.png')
# Находим центроиды зелёных кругов
centroids = find_green_circles_centroids(image)

# Проверяем, нашли ли мы три зелёных круга
if len(centroids) == 3:
    # Определение исходных точек (x, y)
    src_points = np.array(centroids, dtype=np.float32)

    # Определение новых точек для выравнивания
    dst_points = np.array(
        [[0, image.shape[0]], [0, 0], [image.shape[1], 0]], dtype=np.float32
    )

    # Вычисление матрицы аффинного преобразования
    matrix = cv2.getAffineTransform(src_points, dst_points)

    # Применение аффинного преобразования
    aligned_image = cv2.warpAffine(
        image, matrix, (image.shape[1], image.shape[0])
    )

    # Сохранение выровненного изображения
    cv2.imwrite('aligned_image.jpg', aligned_image)
else:
    print("Не удалось найти три зелёных круга для выравнивания.")

if centroids:
    for c in centroids:
        cv2.circle(image, c, 5, (0, 0, 255), -1)

    # Отображение изображения
    cv2.imshow('Detected Green Circles', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Зеленые круги не найдены.")
