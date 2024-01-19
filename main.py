# main.py

from flask_login import LoginManager
from models import User, app
from routes import configure_routes



login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    print(f"Loading user with ID: {user_id}")
    try:
        user = User.query.get(int(user_id))
        print(f"Loaded user: {user}")
        return user
    except Exception as e:
        print(f"Error loading user: {e}")
        return None


if __name__ == '__main__':
    with app.app_context():
        configure_routes(app)
    app.run(debug=True)
