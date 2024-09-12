import cv2
import numpy as np

from screen_info import get_screen_resolution
from find_color_circle_2 import open_filename
from find_direction import find_green_circles_centroids

# Загрузка изображения
image = cv2.imread('CV/qr_circle_rotate.png')

if image is None:
    print("Не удалось загрузить изображение.")
else:
    # Находим центроиды зелёных кругов
    centroids = find_green_circles_centroids(image)

    # Проверяем, нашли ли мы три зелёных круга
    if len(centroids) == 3:
        # Определение исходных точек (x, y)
        src_points = np.array(centroids, dtype=np.float32)

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
        aligned_image = cv2.warpAffine(image, matrix, (int(width), int(height)))

        # Сохраняем выровненное и обрезанное изображение
        cv2.imwrite('aligned_cropped_image.jpg', aligned_image)
    else:
        print("Не удалось найти три зелёных круга для выравнивания.")



    if 'aligned_image' in locals():
        # Определяем имя нового файла с припиской _cut
        output_filename = 'CV/new_files/qr_circle_rotate_cut.png'

        # Сохраняем обрезанное изображение
        cv2.imwrite(output_filename, aligned_image)
        print(f"Обрезанное изображение сохранено как {output_filename}")

        # Изменение размера изображения для соответствия разрешению экрана
        resized_image = cv2.resize(aligned_image, (screen_width//2, screen_height//2))

        # Вызов функции open_filename только один раз
        # open_filename(resized_image)
    else:
        print(
            "Переменная aligned_image не определена,"
            "изображение не может быть сохранено."
        )
