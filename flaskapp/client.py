import os
import requests
from io import BytesIO
import base64
import unittest


class FlaskAppTests(unittest.TestCase):
    BASE_URL = 'http://localhost:5000'

    def setUp(self):
        # Убедимся, что тестовое изображение существует
        self.test_image_path = os.path.join('./static', 'image0008.jpg')
        if not os.path.exists(self.test_image_path):
            raise FileNotFoundError(f"Test image not found at {self.test_image_path}")

    def test_root_endpoint(self):
        """Тестирование корневого эндпоинта /"""
        response = requests.get(f"{self.BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello World!", response.text)

    def test_apixml_endpoint(self):
     """Тестирование эндпоинта /apixml"""
     response = requests.get(f"{self.BASE_URL}/apixml")
     self.assertEqual(response.status_code, 200)
     # Проверяем, что это HTML
     self.assertIn("<html>", response.text.lower())

    def test_data_to_endpoint(self):
        """Тестирование эндпоинта /data_to"""
        response = requests.get(f"{self.BASE_URL}/data_to")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello my dear friends!", response.text)

    def test_apinet_endpoint(self):
        """Тестирование JSON API эндпоинта /apinet"""
        # Читаем тестовое изображение и кодируем в base64
        with open(self.test_image_path, 'rb') as fh:
            img_data = fh.read()
            b64 = base64.b64encode(img_data)

        # Создаем JSON данные для отправки
        jsondata = {'imagebin': b64.decode('utf-8')}

        # Отправляем POST запрос
        response = requests.post(f"{self.BASE_URL}/apinet", json=jsondata)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что ответ содержит JSON с результатами
        result = response.json()
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result) > 0)

    def test_net_endpoint_get(self):
        """Тестирование GET запроса к /net"""
        response = requests.get(f"{self.BASE_URL}/net")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Load image", response.text)

    def test_rgb_endpoint_get(self):
        """Тестирование GET запроса к /rgb"""
        response = requests.get(f"{self.BASE_URL}/rgb")
        self.assertEqual(response.status_code, 200)
        self.assertIn("RGB Channel Processor", response.text)

    def test_rgb_endpoint_post(self):
        """Тестирование POST запроса к /rgb с изображением"""
        # Подготовка тестового файла для загрузки
        files = {'file': open(self.test_image_path, 'rb')}
        data = {'channel_order': '012'}

        # Отправка POST запроса
        response = requests.post(f"{self.BASE_URL}/rgb", files=files, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("RGB Processing Result", response.text)


if __name__ == '__main__':
    unittest.main()