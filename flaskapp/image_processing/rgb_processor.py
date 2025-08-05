import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

def swap_channels(image_array, order):
    """Меняет порядок цветовых каналов"""
    if len(order) != 3 or any(c not in [0, 1, 2] for c in order):
        raise ValueError("Порядок каналов должен состоять из 3 цифр (0-2)")
    return image_array[:, :, order]


def analyze_image(image_array):
    """Анализирует изображение и возвращает графики"""
    plt.figure(figsize=(12, 10))

    # 1. Оригинальное изображение
    plt.subplot(2, 2, 1)
    plt.imshow(image_array)
    plt.title('Оригинальное изображение')
    plt.axis('off')

    # 2. Гистограмма цветов
    plt.subplot(2, 2, 2)
    colors = ('r', 'g', 'b')
    for i, color in enumerate(colors):
        hist, bins = np.histogram(image_array[:, :, i].ravel(), bins=256, range=(0, 256))
        plt.plot(bins[:-1], hist, color=color)
    plt.title('Распределение цветов')
    plt.xlim([0, 256])

    # 3. Среднее по вертикали
    plt.subplot(2, 2, 3)
    mean_vertical = np.mean(image_array, axis=0)
    for i, color in enumerate(colors):
        plt.plot(mean_vertical[:, i], color=color)
    plt.title('Среднее по вертикали')
    plt.xlabel('Ширина (пиксели)')

    # 4. Среднее по горизонтали
    plt.subplot(2, 2, 4)
    mean_horizontal = np.mean(image_array, axis=1)
    for i, color in enumerate(colors):
        plt.plot(mean_horizontal[:, i], color=color)
    plt.title('Среднее по горизонтали')
    plt.xlabel('Высота (пиксели)')

    plt.tight_layout()

    # Сохраняем график в буфер
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    return base64.b64encode(buf.getvalue()).decode('utf-8')


def process_image(filepath, channel_order):
    """Обрабатывает изображение"""
    try:
        # Проверяем порядок каналов
        channel_order = [int(c) for c in channel_order]
        if len(channel_order) != 3 or any(c > 2 for c in channel_order):
            return {'error': 'Неверный порядок каналов. Используйте 3 цифры от 0 до 2'}

        # Загружаем изображение
        img = Image.open(filepath)
        img_array = np.array(img)

        # Меняем каналы
        swapped_array = swap_channels(img_array, channel_order)
        swapped_img = Image.fromarray(swapped_array)

        # Сохраняем измененное изображение
        filename = os.path.basename(filepath)
        swapped_filename = f'swapped_{filename}'
        swapped_filepath = os.path.join(os.path.dirname(filepath), swapped_filename)
        swapped_img.save(swapped_filepath)

        # Анализируем изображение
        analysis_plot = analyze_image(img_array)

        return {
            'swapped_filename': swapped_filename,
            'analysis_plot': analysis_plot
        }

    except Exception as e:
        return {'error': f'Ошибка обработки: {str(e)}'}