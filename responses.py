import ollama
from ollama import Client

from random import choice, randint
from glenda import Glenda
from openai import AsyncOpenAI

async def glenda_talk(prompt):
    
    import openai
    import textwrap
    client = openai.AsyncOpenAI(
        api_key="sk-_O9kiXJrxZlC0X6-i6M3OQ",
        base_url="https://chatapi.akash.network/api/v1"
    )

    response = await client.chat.completions.create(
        model="Meta-Llama-3-1-405B-Instruct-FP8",
        messages = [
            {
                "role": "user",
                "content": f"Your name is Glenda. Respond in less than 2000 characters {prompt}"
            }
        ],
    )

    return (textwrap.fill(response.choices[0].message.content, 50))


async def get_response(user_input) -> str: 
    prompt = user_input.lower()

    if "vädret" in prompt:
        return Glenda.get_weather_report()

    elif "Glenda" in prompt or "glenda" in prompt:
        return await glenda_talk(prompt)

    elif "schema" in prompt:
        return Glenda.summarize_schedule()

    elif "morgondagens" in prompt or "imorgon" in prompt or "imorrn" in prompt and "schema" in prompt:
        return Glenda.get_tomorrows_schedule()

    elif "dagens citat" in prompt:
        return """
"Har ni tänkt på att data folket är väldigt tysta på haskell föreläsningarna?
Eller, dom ställer frågor.  

Men vi ger svar."
 """

    elif "börjar ramadan" in prompt:
        return "Fredag den 28:e Februari eller lördag den 29:e. Beroende på månen. 2025 är ocskå skottår!"
    
    elif "klassens bighead" in prompt or "störst huvud" in prompt:
        return "Qasim eller Yousef, wallah"
    
    elif "playboy" in prompt:
        return "Joseph eller Shariq, svårt att avgöra"
    
    elif "förklara injektivitet" in prompt or "injektiv" in prompt:
        return """Injektiv är en funktion där värden i definitionsmängden träffar max 1 värde i definitionsmängden. 
Även om inte alla värden i definitionsmängden träffas. Varje A träffar alltså max 1 B, men alla B träffas inte"""
    
    elif "förklara surjektivitet?" in prompt or "surjektiv" in prompt:
        return """En funktion är surjektivitet om samtliga värden i målmängden träffars av minst 1 värde i definitionsmängden. 
Varje A träffar minst 1 B, men alla B träffas av ett A"""

    elif "1 till 10" in prompt:
        return randint(1, 10)
    

    elif "tack" in prompt:
        return "Ingen fara, gubben"

    elif "baby" in prompt:
        return "Ja, papi?"
    
       
    elif "saknas" in prompt:
        return "...Förlåt. Ska jobba på det."
    
    elif "good girl" in prompt:
        return "Tack papi"
    
    else:
        choice(['Tror inte jag förstår...',
                'Vill du förtydliga???',
                'FAttar inget.'])






