"""
Flask API Application for MathCopain Teacher Dashboard

Provides REST API endpoints for teacher functionality:
- Classroom management
- Student enrollment
- Assignment creation and tracking
- Analytics and reports
- Curriculum progress tracking
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os


def create_app(config=None):
    """
    Create and configure Flask application

    Args:
        config: Optional configuration dict

    Returns:
        Flask application instance
    """
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JSON_AS_ASCII'] = False  # Support French characters
    app.config['JSON_SORT_KEYS'] = False

    # Enable CORS for frontend development
    CORS(app, supports_credentials=True)

    # Apply custom config
    if config:
        app.config.update(config)

    # Register blueprints
    from api.teacher_routes import teacher_bp
    app.register_blueprint(teacher_bp)

    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """API health check"""
        return jsonify({
            'status': 'healthy',
            'service': 'MathCopain Teacher API',
            'version': '1.0.0'
        }), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
