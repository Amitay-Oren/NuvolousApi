from website.web_app import WebApp
from website import create_app

app = create_app()
web_app = WebApp()

if __name__ == '__main__':
    app.run(debug=True)
