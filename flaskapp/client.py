import os
import requests
import base64
import unittest
from pathlib import Path


class FlaskAppTests(unittest.TestCase):
    BASE_URL = 'http://localhost:5000'
    TEST_IMAGE = Path('./static/image0008.jpg')

    @classmethod
    def setUpClass(cls):
        """Выполняется один раз перед всеми тестами"""
        if not cls.TEST_IMAGE.exists():
            raise FileNotFoundError(f"Test image not found at {cls.TEST_IMAGE}")

    def setUp(self):
        """Выполняется перед каждым тестом"""
        self.test_files_to_close = []

    def tearDown(self):
        """Выполняется после каждого теста"""
        for file in self.test_files_to_close:
            file.close()

    def _get_test_image_base64(self):
        """Возвращает base64-кодированное тестовое изображение"""
        with open(self.TEST_IMAGE, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def test_root_endpoint(self):
        response = requests.get(f"{self.BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello World!", response.text)

    def test_apixml_endpoint(self):
        response = requests.get(f"{self.BASE_URL}/apixml")
        self.assertEqual(response.status_code, 200)
        self.assertIn("html", response.text.lower())

    def test_data_to_endpoint(self):
        response = requests.get(f"{self.BASE_URL}/data_to")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello", response.text)

    def test_apinet_endpoint(self):
        jsondata = {'imagebin': self._get_test_image_base64()}
        response = requests.post(f"{self.BASE_URL}/apinet", json=jsondata)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_net_endpoint_get(self):
        response = requests.get(f"{self.BASE_URL}/net")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Load image", response.text)

    def test_rgb_endpoint_get(self):
        response = requests.get(f"{self.BASE_URL}/rgb")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Выберите изображение", response.text)

    def test_rgb_endpoint_post(self):
        # Используем менеджер контекста для автоматического закрытия файла
        with open(self.TEST_IMAGE, 'rb') as f:
            files = {'file': f}
            data = {'channel_order': '012'}
            response = requests.post(f"{self.BASE_URL}/rgb", files=files, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("RGB Processing Result", response.text)


if __name__ == '__main__':
    unittest.main()