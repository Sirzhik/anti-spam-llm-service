import openai


class OpenAISPAMCheck:
    def __init__(self, token, model="gpt-4o-mini"):
        self.client = openai.OpenAI(api_key=token)
        self.model = model
        self.spam_system_prompt = {"role": "system", "content": """You are working as anti-spam filter. Definitions of SPAM:
                Ads, promotions, SCAMs (prize lotteries, fake opportunities, etc.), phishing links, courses, etc. If the message contains any of these - it is SPAM.
                Most of the time, job offers are not SPAM..
                If text written in another language than English - translate it to english first, then check if it contains any SPAM content.
                In CONTEXT users puts additional info about data which he want to recive even if this is SPAM. If thats allowed kind of SPAM - set spam percentege to 0%."""}

    def spam_check(self, mail_text: str, additional_context: str = None) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=[
                self.spam_system_prompt,
                {"role": "user", "content": f"""
                ### CONTEXT:
                {additional_context}

                ### MAIL:
                {mail_text}
                You need to check if the message contains any spam content. If it does - send ONLY percentage of chance that the message is spam in int format and the kind of spam (e.g., "Ads", "Promotion", "SCAM", "Phishing", ""(None is null string)).
                """},
                
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "spam_percentage",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "percentage_chance": {"type": "integer"},
                            "spam_kind": {"type": "string"}
                        },
                        "required": ["percentage_chance", "spam_kind"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
            
        )
        return response.output[0].content[0].text
    
    def spam_stream_describe(self, mail_text: str,):
        stream = self.client.responses.create(
            model=self.model,
            input=[
                self.spam_system_prompt,
                {'role': "system", 'content': 'You must let user short answers.'},
                {"role": "user", "content": f"""
                ### MAIL:
                {mail_text}
                You need to explain the nature of the message and its potential spam characteristics for user.
                """},
            ],
            stream = True
        )
        

        for event in stream:
            yield event
