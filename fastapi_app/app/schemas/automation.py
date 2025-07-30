from pydantic import BaseModel

class SignupPayload(BaseModel):
    name: str
    email: str
    password: str
    proxy_username: str
    type: str # e.g., "AMZ", "FB"

class ProfileResponse(BaseModel):
    profile_id: int
    status: str

class AutomationRequest(BaseModel):
    profile_id: int