import cv2
import traceback
import numpy as np


def open_filename():
    # Загрузить изображение
    image = cv2.imread('CV/circle.jpg', cv2.COLOR_BGR2HSV)
    if image is None:
        raise ValueError('Не удалось загрузить изображение.')

    # Изолировать красный цвет
    # Установить нижние и верхние границы красного цвета
    lower_red1 = np.array([0, 0, 0])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 0, 0])
    upper_red2 = np.array([179, 255, 255])

    # Создать маску для красного цвета в HSV
    mask1 = cv2.inRange(image, lower_red1, upper_red1)
    mask2 = cv2.inRange(image, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Найти контуры в маске
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Нарисовать контуры на изображении
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

    # Показать полученное изображение
    cv2.imshow('Контур красного цвета', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    try:
        open_filename()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
