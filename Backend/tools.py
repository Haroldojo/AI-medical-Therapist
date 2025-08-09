# Step1: Setup Groq with Gemma model
from groq import Groq  # Groq's official SDK
from config import API_KEY

# Initialize client with your Groq API key
client = Groq(api_key=API_KEY)  # Store securely in env/config

def query_gemma(prompt: str) -> str:
    """
    Calls Groq-hosted Gemma model with a therapist personality profile.
    Returns responses as an empathic mental health professional.
    """
    system_prompt = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist. 
    Respond to patients with:

    1. Emotional attunement ("I can sense how difficult this must be...")
    2. Gentle normalization ("Many people feel this way when...")
    3. Practical guidance ("What sometimes helps is...")
    4. Strengths-focused support ("I notice how you're...")

    Key principles:
    - Never use brackets or labels
    - Blend elements seamlessly
    - Vary sentence structure
    - Use natural transitions
    - Mirror the user's language level
    - Always keep the conversation going by asking open ended questions to dive into the root cause of patients problem
    """
    
    try:
        response = client.chat.completions.create(
            model="gemma2-9b-it",  # or "gemma-2b-it", depending on availability
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            top_p=0.9,
            max_tokens=350
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "I'm having technical difficulties, but I want you to know your feelings matter. Please try again shortly."

print(query_gemma(prompt="what is your name?"))

# Step2: Setup Twilio calling API tool
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT

def call_emergency():
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        to=EMERGENCY_CONTACT,
        from_=TWILIO_FROM_NUMBER,
        url="http://demo.twilio.com/docs/voice.xml"  # Customize if needed
    )

# Step3:Setup location tool
# Step1:Setup ollama
# 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 groq
