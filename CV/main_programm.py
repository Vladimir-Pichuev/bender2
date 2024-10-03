import cv2
import numpy as np
import os

from screen_info import get_screen_resolution
from find_color_circle_2 import open_filename
from find_direction import find_green_circles_centroids

# Загрузка изображения
file_path = os.path.join('CV', 'qr_circle_rotate.jpg')
if os.path.exists(file_path):
    print(f"Файл с изображением в папке '{file_path}' существует.")
# os.chdir(file_path)
#image = cv2.imread(file_path)


if file_path is None:
    print("Не удалось загрузить изображение.")
else:
    # Находим центроиды зелёных кругов
    centroids = find_green_circles_centroids(file_path)
    print (f'количество зелёных кругов {len(centroids)}')

    # Проверяем, нашли ли мы три зелёных круга
    if len(centroids) == 3:
        # Сортируем центры зелёных кругов по порядку
        centroids.sort(key=lambda x: x[0] + x[1])

        src_points = np.array([centroids[0], centroids[1], centroids[2]], dtype=np.float32)

        # Вычисляем ширину и высоту на основе расстояний между точками
        width = np.linalg.norm(src_points[0] - src_points[1])
        height = np.linalg.norm(src_points[1] - src_points[2])

        # Определяем новые точки для горизонтального выравнивания
        dst_points = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1]
        ], dtype=np.float32)

        # Вычисляем матрицу аффинного преобразования
        matrix = cv2.getAffineTransform(src_points[:3], dst_points)

        # Получение разрешения экрана
        screen_width, screen_height = get_screen_resolution()

        # Применяем аффинное преобразование и обрезаем изображение
        image = cv2.imread(file_path)
        aligned_image = cv2.warpAffine(image, matrix, (int(width), int(height)))
        # Сохраняем выровненное и обрезанное изображение
        cv2.imwrite('aligned_cropped_image.jpg', aligned_image)

        # Поворачиваем изображение на 90 градусов по часовой стрелке
        (h, w) = aligned_image.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D((cX, cY), 90, 1.0)
        rotated_image = cv2.warpAffine(aligned_image, M, (w, h))

        # Сохраняем повернутое изображение
        cv2.imwrite('qr_circle_rotate_cut.png', rotated_image)
    else:
        print("Не удалось найти три зелёных круга для выравнивания.")

    if 'aligned_image' in locals():
        # Определяем имя нового файла с припиской _cut
        output_filename = 'CV/new_files/qr_circle_rotate_cut.png'

        # Сохраняем обрезанное изображение
        cv2.imwrite(output_filename, rotated_image)
        print(f"Обрезанное изображение сохранено как {output_filename}")

        # Изменение размера изображения для соответствия разрешению экрана
        resized_image = cv2.resize(rotated_image, (screen_width//2, screen_height//2))

        # Вызов функции open_filename только один раз
        # open_filename(resized_image)
    else:
        print(
            "Переменная aligned_image не определена,"
            "изображение не может быть сохранено."
        )
