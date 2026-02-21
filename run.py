from app import create_app
from flask_cors import CORS
import os

app = create_app()

# Enable CORS globally
CORS(app, resources={r"/*": {"origins": "*"}})

# Only used for local testing
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)