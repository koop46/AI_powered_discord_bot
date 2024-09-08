from random import choice, randint
from glenda import Glenda



def get_response(user_input) -> str:
    prompt = user_input.lower()

    if "tack" in prompt:
        return "Ingen fara, gubben"
    
    elif "vädret" in prompt:
        return Glenda.get_weather_report()

    elif "börjar ramadan" in prompt:
        return "Fredag den 28:e Februari eller lördag den 29:e. Beroende på månen. 2025 är ocskå skottår!"
    
    elif "störst huve" in prompt:
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
    
    elif "schema" in prompt:
        return Glenda.summarize_todays_schedule()

    elif "baby" in prompt:
        return "Ja, papi?"
    
    else:
        choice(['Tror inte jag förstår...',
                'Vill du förtydliga???',
                'FAttar inget.'])






