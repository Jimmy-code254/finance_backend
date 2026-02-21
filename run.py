# run.py
import os
from app import create_app
from flask_cors import CORS

app = create_app()

# Apply CORS to the app
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    # Use Render's PORT env variable, default to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)