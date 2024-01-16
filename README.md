
## Project Setup

- First install Python version 3.11.4 and make sure to install PIP
- Then create an virtual environment 
  - For Windows

    ```bash
      py -m venv myenv
    ```
  - For Unix/MacOS

    ```bash
      python -m venv myenv
    ```

- Then activate the virtual environment

  - Windows

    ```bash
      myenv\Scripts\activate.bat
    ```
  - Unix/MacOS

    ```bash
      source myenv/bin/activate
    ```

- Now Clone the project

  ```bash
    git clone https://github.com/AlAmin008/GENText_backend.git
  ```

- Go to the project directory

  ```bash
    cd gentext_bn_2
  ```

- Install following dependencies

  - Install Django (Version 4.2.4)

    ```bash
      pip install Django
    ```
  - Install Django REST Framework

    ```bash
      pip install djangorestframework
    ```
  - Install SimpleJWT

    ```bash
      pip install djangorestframework-simplejwt
    ```
  - Install core headers

    ```bash
      pip install django-cors-headers
    ```
  - Install mysqlclient

    ```bash
      pip install mysqlclient
    ```
  - Install opencv

    ```bash
      pip install opencv-python
    ```
  - Install PyMuPDF

    ```bash
      pip install PyMuPDF
    ```
  - Install tesseract OCR
    - For Windows
      - Download and install tesseract https://github.com/UB-Mannheim/tesseract/wiki
      - Go to gentext_bn_2/settings.py and add tesseract path in here : pytesseract.pytesseract.tesseract_cmd = '{your_path}/tesseract.exe'
      - To enable bangla OCR first go to your installed tesseract folder and go to tessdata folder
      - Download ben.tessdata from https://github.com/tesseract-ocr/tessdata 
    - For Unix/MacOS
      - Install tesseract OCR

        ```bash
          sudo apt install tesseract-ocr -y
        ```
      - Enable bangla OCR

        ```bash
          sudo apt install tesseract-ocr-ben
        ```
      - Go to gentext_bn_2/settings.py and comment out or remove this line : pytesseract.pytesseract.tesseract_cmd = '{your_path}/tesseract.exe'
  - Install pytesseract

    ```bash
      pip install pytesseract
    ```
## Database Configuration
- Go to gentext_bn_2/settings.py and adjust the variables:
  ```
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'gentext',
          'HOST': 'localhost',
          'PORT':3306,
          "USER": 'root',
          'PASSWORD': ''
      }
  }
  ```
- start your xampp server
- create a new database named 'gentext' and select 'utf8_unicode_ci' collation
- Go to the project directory and apply migrations to set up the database schema

```bash
    python manage.py migrate
  ```
## Run Project
- Activate the virtual environment
- start xampp server
- Go to the project directory
- Within the project directory open cmd and enter 

    ```bash
      python manage.py runserver
    ```
