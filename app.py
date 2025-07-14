import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=7860)
print("🔁 USE_SQLITE =", os.environ.get("USE_SQLITE"))
