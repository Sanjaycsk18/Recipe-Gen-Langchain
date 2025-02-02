import json
import base64
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI as genai

def generate_recipe(image_path):
    
    with open(image_path, "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode("utf-8")
    
    
    image_url = f"data:image/png;base64,{image}"
    
   
    model = genai(model="gemini-1.5-flash", max_output_tokens=2048, top_k=40, top_p=0.95, temperature=1.0, max_tokens=8192)

    prompt = """
        Please provide the recipe as a structured JSON object. The JSON should include the following keys:
        - 'name': the name of the recipe
        - 'description': a brief description of the dish
        - 'ingredients': a list of ingredients
        - 'instructions': a step-by-step guide on how to prepare the dish
        Return the recipe in the form of a JSON object only not extra strings.
    """
    
    
    input_message = [
        HumanMessage(
            content=[
                {"type": "text", "text": f"Given this image:\n\n1. Identify the recipe. Then, {prompt}"},
                {"type": "image_url", "image_url": image_url},
            ]
        )
    ]
    
    response = model.invoke(input_message)
    
    
    processed_response = response.content.replace("json","").replace('```',"")
    print(f"From Model: \n{processed_response}")
    
    try:
        
        structured_response = json.loads(processed_response)
        print(f"Structured Recipe: \n{structured_response}")
        
        return structured_response
    except json.JSONDecodeError:
        print("Failed to parse the response into JSON.")
        return None
        
