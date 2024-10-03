'''
    """
    Эта функция принимает путь к изображению в качестве входного параметра, читает изображение и находит центры зеленых кругов в изображении.
    
    Параметры:
    image_path (str): Путь к файлу изображения.
    
    Возвращает:
    centroids (list): Список кортежей, где каждый кортеж представляет собой координаты (x, y) центра зеленого круга.
    """
    
    # Читаем изображение из указанного пути
    
    # Отображаем оригинальное изображение
    cv2.namedWindow('Оригинальное изображение', cv2.WINDOW_NORMAL)  # Создаем окно с нормальным размером
    cv2.resizeWindow('Оригинальное изображение', 720, 480)  # Изменяем размер окна до 720x480 пикселей
    cv2.imshow('Оригинальное изображение', image)  # Отображаем изображение в окне
    cv2.waitKey(0)  # Ждем нажатия клавиши
    
    # Конвертируем изображение в цветовое пространство HSV (цвет, насыщенность, значение)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Отображаем изображение в цветовом пространстве HSV
    cv2.namedWindow('Изображение в HSV', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Изображение в HSV', 720, 480)
    cv2.imshow('Изображение в HSV', hsv)
    cv2.waitKey(0)
    
    # Определяем диапазон зеленого цвета в HSV
    lower_green = np.array([30, 100, 100])  # Нижняя граница зеленого цвета
    upper_green = np.array([90, 255, 255])  # Верхняя граница зеленого цвета
    
    # Применяем пороговое значение для выделения зеленых пикселей
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Отображаем пороговое изображение
    cv2.namedWindow('Пороговое изображение', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Пороговое изображение', 720, 480)
    cv2.imshow('Пороговое изображение', mask)
    cv2.waitKey(0)
    
    # Применяем морфологические операции для улучшения качества маски
    kernel = np.ones((5, 5), np.uint8)  # Создаем ядро 5x5 для эрозии и дилатации
    mask = cv2.erode(mask, kernel, iterations=1)  # Эрозия маски для удаления шума
    mask = cv2.dilate(mask, kernel, iterations=1)  # Дилатация маски для заполнения пробелов
    
    # Отображаем морфологически обработанное изображение
    cv2.namedWindow('Морфологически обработанное изображение', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Морфологически обработанное изображение', 720, 480)
    cv2.imshow('Морфологически обработанное изображение', mask)
    cv2.waitKey(0)
    
    # Применяем медианный фильтр для улучшения качества изображения
    gray = cv2.medianBlur(mask, 5)
    
    # Отображаем отфильтрованное изображение
    cv2.namedWindow('Отфильтрованное изображение', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Отфильтрованное изображение', 720, 480)
    cv2.imshow('Отфильтрованное изображение', gray)
    cv2.waitKey(0)
    
    # Обнаруживаем круги с помощью преобразования Хафа
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=400, param2=300, minRadius=0, maxRadius=0)
    print (f'Колличество кругов {circles}')
    
    # Инициализируем список центров
    centroids = []
    
    # Проверяем, обнаружены ли круги
    if circles is not None:
        circles = np.uint16(np.around(circles))  # Конвертируем координаты кругов в целые числа
        for i in circles[0, :]:
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)  # Draw a green circle around the centroid
            cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)  # Draw a red circle at the centroid
            centroids.append((i[0], i[1]))  # Add the centroid to the list
'''
