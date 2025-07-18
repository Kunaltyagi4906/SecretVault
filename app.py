# app.py or main.py

import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app  # make sure your 'app' folder has __init__.py

app = create_app()

# Hugging Face expects this:
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7860)), debug=False)

# Optional Debug
print("✅ USE_SQLITE =", os.environ.get("USE_SQLITE"))
