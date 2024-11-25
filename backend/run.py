# backend/run.py
print("Importing create_app")
from app import create_app

print("Running run.py")
app = create_app()
if __name__ == '__main__':
    print("Starting app")
    app.run(debug=True)