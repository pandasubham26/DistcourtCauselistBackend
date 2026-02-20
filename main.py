import os
from app import create_app

# Load environment or default to development
config_name = os.getenv('FLASK_ENV', 'development')

# Create Flask app instance
app = create_app(config_name)


if __name__ == '__main__':
    debug = app.config.get('DEBUG', config_name == 'development')
    app.run(host='0.0.0.0', port=2000, debug=debug)
