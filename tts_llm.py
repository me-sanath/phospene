from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_KEY"))

def cues_generate(obstacle,navigation_cue):
    chat_completion = client.chat.completions.create(
        
        messages=[
            {
                "role": "system",
                "content": "You are a assistant for an AR Navigation System. You'll be given direction or obstacle as input. Convert it to audio cues for blinds. let the cues concise"
            },
            {
                "role": "user",
                "content": f"Obstacle detected is {obstacle},what to do to avoid :{navigation_cue}",
            }
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )
    return chat_completion.choices[0].message.content



# Test Line
print(cues_generate(input("Enter the obstacle"),input("Enter the navigation cue")))