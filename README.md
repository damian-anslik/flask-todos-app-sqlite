# 🚀 Getting Started

1. Clone this repository

2. Create a new virtual environment

    `python -m venv venv`

3. Restore project dependencies using: 

    `pip install -r requirements.txt`

4. Create a .env file in the root of the project, this should contain:

    ```
    SECRET_KEY = "the-secret-key-for-the-app"
    SQLALCHEMY_DATABASE_URI = "sqlite:///path/to/your/db"
    MAIL_SERVER = "the email server: e.g. smtp.google.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "email-client-username"
    MAIL_PASSWORD = "email-client-password"
    ```

    The MAIL_PASSWORD for the mail client can be retrieved from Gmail by following [this article](https://support.google.com/accounts/answer/185833?hl=en).

## 💃 About Styling

This project uses the open-source CSS framework Bulma. For documentation see [here](https://bulma.io/documentation/columns/sizes/).

## 💫 Icons

This project uses free FontAwesome icons. For a list of icons see [here](https://fontawesome.com/icons).