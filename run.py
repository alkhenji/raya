from dotenv import load_dotenv
load_dotenv()

from app.controllers.main_controller import app

if __name__ == '__main__':
    app.run(debug=True)

