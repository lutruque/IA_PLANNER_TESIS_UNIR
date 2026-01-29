from fastapi import APIRouter
from app.schemas import PlanRequest, PlanAndEmailRequest
from app.services.itinerary_service import build_itinerary
from app.mail.mailer import send_itinerary_email

router = APIRouter()

@router.post("/plan_v3")
def plan_v3(req: PlanRequest):
    return build_itinerary(req)

@router.post("/plan_and_email")
def plan_and_email(req: PlanAndEmailRequest):
    itinerary = build_itinerary(req)
    send_itinerary_email(req.to_email, req.subject, itinerary)
    return {"ok": True, "sent_to": req.to_email}
