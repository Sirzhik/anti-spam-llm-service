import pydantic

class SpamCheckRequest(pydantic.BaseModel):
    mail_text: str
    title_text: str = None
    additional_context: str = None
    sender_email: str = None
