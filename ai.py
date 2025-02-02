# ai.py - AI Logic Module
import base64
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI as genai

def generate_recipe(image_path):
    with open(image_path, "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode("utf-8")
    
    model = genai(model="gemini-1.5-flash", max_output_tokens=2048, top_k=40, top_p=0.95, temperature=1.0, max_tokens=8192)
    
    input_message = [
        HumanMessage(
            content=[
                {"type": "text", "text": "Given this image:\n\n1. identify the recipe. then, detail the recipe to bake this item in list format. Include item names and quantities for the recipe. "},
                {"type": "image_url", "image_url": f"data:image/png;base64,{image}"},
            ]
        )
    ]
    
    response = model.invoke(input_message)
    print(response)
    return response.content 