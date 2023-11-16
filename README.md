README (English)

Flask API with Encryption\
This Flask API provides endpoints for token generation, text encryption, text decryption, and log management using the Fernet encryption algorithm.

Getting Started\
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites\
Python 3.x\
Flask\
Flask-RESTful\
cryptography\
Installation


Clone the repository:

```bash
git clone https://github.com/your-username/flask-encryption-api.git
```

Change into the project directory:

```bash
cd flask-encryption-api
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Usage

Run the Flask application:

```bash
python run.py
```
Access the API endpoints:

Token Generation: http://localhost:5000/token \
Text Encryption: http://localhost:5000/encrypt \
Text Decryption: http://localhost:5000/decrypt 

API Endpoints\
/token: Generate a new encryption token.\
/encrypt: Encrypt a text using the provided token.\
/decrypt: Decrypt a text using the provided token.\

Contributing\
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

License\
This project is licensed under the MIT License - see the LICENSE.md file for details.

README (Russian)

Flask API с шифрованием\
Этот Flask API предоставляет конечные точки для генерации токенов, шифрования и дешифрования текста, а также управления журналом с использованием алгоритма шифрования Fernet.

Начало работы\
Эти инструкции помогут вам создать копию проекта и запустить его на вашем локальном компьютере в целях разработки и тестирования.

Требования\
Python 3.x\
Flask\
Flask-RESTful\
cryptography

Установка\
Клонируйте репозиторий:

```bash
git clone https://github.com/your-username/flask-encryption-api.git
```
Перейдите в каталог проекта:

```bash
cd flask-encryption-api
```
Установите необходимые зависимости:

```bash
pip install -r requirements.txt
```
Использование

Запустите приложение Flask:

```bash
python run.py
```
Обратитесь к конечным точкам API:

Генерация токена: http://localhost:5000/token \
Шифрование текста: http://localhost:5000/encrypt \
Дешифрование текста: http://localhost:5000/decrypt \

Конечные точки API

/token: Генерация нового шифровального токена.\
/encrypt: Зашифровка текста с использованием предоставленного токена.\
/decrypt: Расшифровка текста с использованием предоставленного токена.\

Участие в разработке

Пожалуйста, прочитайте CONTRIBUTING.md для получения дополнительной информации о нашем коде поведения и процессе отправки запросов на включение изменений.

Лицензия

Этот проект лицензирован по лицензии MIT - см. файл LICENSE.md для получения дополнительной информации.