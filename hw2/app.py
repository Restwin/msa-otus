from flask import Flask, jsonify

# Создаем экземпляр приложения Flask
app = Flask(__name__)

# Определяем маршрут для GET /health/
@app.route('/health/', methods=['GET'])
def health_check():
    # Возвращаем JSON-ответ
    response_data = {"status": "OK"}
    return jsonify(response_data), 200

# Запускаем сервер, если скрипт выполняется напрямую
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
