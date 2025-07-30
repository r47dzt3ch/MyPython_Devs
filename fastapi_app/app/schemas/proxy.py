from pydantic import BaseModel

class ResidentialProxyRequest(BaseModel):
    country: str
    region: str
    city: str
    isp: str
    type: str # e.g., "AMZ", "FB"