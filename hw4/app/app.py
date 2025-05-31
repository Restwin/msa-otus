from flask import Flask, request, jsonify
from .config import Config
from .models import db, User

def create_app():
    app = Flask(__name__)
    config = Config()
    app.config.from_object(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_db_uri()
    db.init_app(app)

    # API префикс, как в Swagger
    API_PREFIX = "/api/v1"

    @app.route(f'{API_PREFIX}/user', methods=['POST'])
    def create_user():
        data = request.get_json()
        if not data:
            return jsonify({"code": 400, "message": "Invalid input"}), 400

        # Проверка обязательных полей из Swagger
        if not data.get('username') or not data.get('email'):
                return jsonify({"code": 400, "message": "Username and email are required"}), 400

        try:
            new_user = User(
                username=data['username'],
                firstName=data.get('firstName'),
                lastName=data.get('lastName'),
                email=data['email'],
                phone=data.get('phone')
            )
            db.session.add(new_user)
            db.session.commit()
            # Возвращаем созданного пользователя с ID
            return jsonify(new_user.to_dict()), 201 # 201 Created
        except Exception as e:
            db.session.rollback()
            # Проверка на уникальность (может быть улучшена для конкретных полей)
            if "unique constraint" in str(e).lower():
                return jsonify({"code": 409, "message": "User with this username or email already exists"}), 409 # Conflict
            app.logger.error(f"Error creating user: {e}")
            return jsonify({"code": 500, "message": "Internal server error"}), 500

    @app.route(f'{API_PREFIX}/user/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = db.session.get(User, user_id)
        if user:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({"code": 404, "message": "User not found"}), 404

    @app.route(f'{API_PREFIX}/user/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"code": 404, "message": "User not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"code": 400, "message": "Invalid input"}), 400

        # Обновляем только предоставленные поля
        if 'username' in data: user.username = data['username']
        if 'firstName' in data: user.firstName = data['firstName']
        if 'lastName' in data: user.lastName = data['lastName']
        if 'email' in data: user.email = data['email']
        if 'phone' in data: user.phone = data['phone']
        
        try:
            db.session.commit()
            return jsonify(user.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            if "unique constraint" in str(e).lower():
                return jsonify({"code": 409, "message": "Update failed: username or email already in use by another user"}), 409
            app.logger.error(f"Error updating user: {e}")
            return jsonify({"code": 500, "message": "Internal server error"}), 500


    @app.route(f'{API_PREFIX}/user/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return '', 204 # No Content
        else:
            return jsonify({"code": 404, "message": "User not found"}), 404
    
    @app.route('/health', methods=['GET'])
    def health_check():
        # Простая проверка доступности БД
        try:
            db.session.execute(db.text('SELECT 1'))
            return jsonify({"status": "UP", "database": "connected"}), 200
        except Exception as e:
            app.logger.error(f"Health check failed: Database connection error: {e}")
            return jsonify({"status": "DOWN", "database": "disconnected", "error": str(e)}), 503


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=Config.APP_PORT, debug=True)
