from fastapi import FastAPI, APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
from utils import fetch_email_content
from src.preprocessing import preprocess_email, bow_model
from src.predict import predict_email, load_model

# Initialize FastAPI app and Jinja2 templates
app = FastAPI(title="Email Spam Detector")
api_router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

# ======================== Models ========================
class EmailFormData(BaseModel):
    username: str
    password: str
    email_count: int

# ======================== API Endpoints ========================
@api_router.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    """
    Render the home page.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@api_router.post("/predict/", response_class=HTMLResponse)
async def post_predict(request: Request):
    """
    Fetch emails, predict spam, and render results.
    """
    try:
        form_data = await request.json()
        # Fetch emails
        emails = fetch_email_content(user=form_data.get("username"), passwd=form_data.get("password"), num_emails=form_data.get("email_count"))

        # Load Model and BOW vectorizer
        model_name = "logistic_regression_model"
        weight_dir = "weights"  # Đường dẫn model weights
        model = load_model(model_name=model_name, weights_dir=weight_dir)

        spam_data_path = "data/postprocessing/spam.txt"
        cv = bow_model(spam_data_path)

        # Predict each email
        results = {}
        for email in emails:
            lines = email.splitlines()
            subject_line = next((line for line in lines if line.startswith("Subject:")), "No Subject")
            preprocessed_email = preprocess_email(email=email, cv=cv)
            prediction = predict_email(model, preprocessed_email)
            results[subject_line] = prediction
        results = json.dumps(results, ensure_ascii=False, indent=2)
        # Render results
        return JSONResponse(content={"results": results})
    except ValueError as ve:
        return JSONResponse(content={"error": str(ve)}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Include the API router
app.include_router(api_router)