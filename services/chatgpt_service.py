import os
import openai
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API key from environment variable
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_itinerary(destination: str, styles: list[str], days: int) -> dict:
    """
    Calls OpenAI API to get a 3-day itinerary for the given destination and styles.
    Returns a dictionary like:
    {
      "Day 1": ["Activity1", "Activity2"],
      "Day 2": ["Activity1", "Activity2"],
      "Day 3": ["Activity1", "Activity2"]
    }
    """

    style = ", ".join(styles) if styles else "any style"

    prompt = (
        f"Generate a {days} day travel plan for {destination} with the style of{style}."
        "Return ONLY JSON in this format:\n"
        "{ \"Day 1\": [\"activity1\",\"activity2\"], \"Day 2\": [...], \"Day 3\": [...] }"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )

    content = response.choices[0].message.content.strip()

    try:
        # Handle responses wrapped in markdown code blocks
        if content.startswith('```json'):
            # Remove the opening ```json and closing ```
            content = content.replace('```json', '').replace('```', '').strip()
        elif content.startswith('```'):
            # Remove any markdown code blocks
            content = content.replace('```', '').strip()
        
        # GPT might use single quotes → replace with double quotes
        json_str = content.replace("'", '"')
        itinerary = json.loads(json_str)
        return itinerary
    except Exception as e:
        print("⚠️ Error parsing GPT response:", e)
        print("Raw response was:", content)
        # Fallback placeholder
        return {
            "Day 1": ["Could not parse response"],
            "Day 2": [],
            "Day 3": []
        } 