import cv2
import numpy as np

def find_green_circles_centroids(image_path):
    # Считываем изображение
    image = cv2.imread(image_path)

    # Конвертируем изображение в цветовое пространство HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Определяем диапазон зеленого цвета в HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    # Пороговая обработка изображения для выделения только зеленых пикселей
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Применяем морфологические операции для удаления шума и заполнения отверстий
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Ищем контуры зеленых фигур
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Создаем список для хранения центров эллипсов
    centroids = []

    # Перебираем контуры и находим центры эллипсов
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w)/h
        if area > 100 and aspect_ratio > 0.5 and aspect_ratio < 2:  # фильтрация маленьких и неэллиптических фигур
            (x, y), radius = cv2.minEnclosingCircle(contour)
            centroids.append((int(x), int(y)))  # храним центр эллипса

    # Обрезаем изображение так, чтобы центры эллипсов были в углах
    if len(centroids) > 0:
        min_x = min(centroid[0] for centroid in centroids) - radius
        min_y = min(centroid[1] for centroid in centroids) - radius
        max_x = max(centroid[0] for centroid in centroids) + radius
        max_y = max(centroid[1] for centroid in centroids) + radius

        # Проверяем, что координаты углов эллипсов не выходят за пределы изображения
        if min_x < 0 or min_y < 0 or max_x > image.shape[1] or max_y > image.shape[0]:
            print("Координаты углов эллипсов выходят за пределы изображения")
            return None

        # Вычисляем ширину и высоту обрезанного изображения
        width = max_x - min_x
        height = max_y - min_y

        # Обрезаем изображение до желаемой прямоугольной формы
        cropped_image = image[int(min_y):int(max_y), int(min_x):int(max_x)]

        # Отображаем результат
        cv2.namedWindow('Output', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Output', 360, 240)
        cv2.imshow('Output', cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return centroids
