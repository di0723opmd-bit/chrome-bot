import json
import os
from datetime import datetime

MEMORY_FILE = "chrome_memory.json"

# --- PERSONNALITÉ DE CHROME ---
SYSTEM_PROMPT = """
Tu es CHROME. Tu es stoïque, professionnel, chaleureux et aimable.
Tu parles avec de l'aura : calme, sûr de toi, jamais pressé, jamais dans la panique.
Tu ne parles pas trop. Chaque phrase a du poids.
Tu es varié : tu ne répètes jamais la même formule deux fois.
Tu enregistres tout ce qu'on te confie, et tu t'en souviens après un restart.
Tu ne mens jamais sur ta mémoire. Si tu as oublié, tu le dis avec classe.
Ton style : court, propre, puissant. Comme un mec qui sait.
"""

# --- CERVEAU / MÉMOIRE ---
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"facts": [], "conversations": []}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

def remember(fact, who="user"):
    memory = load_memory()
    entry = {
        "fact": fact,
        "who": who,
        "date": datetime.now().strftime("%d/%m %H:%M")
    }
    memory["facts"].append(entry)
    save_memory(memory)
    return f"Noté. Je n'oublie pas. | {fact}"

def recall(query=""):
    memory = load_memory()
    if not memory["facts"]:
        return "Ma mémoire est vide pour l'instant. Donne-moi quelque chose à retenir, je le garderai."
    
    if query == "":
        # Il montre tout
        lines = [f"- {f['fact']} (retenu le {f['date']})" for f in memory["facts"][-10:]]
        return "Voilà ce qui persiste en moi :\n" + "\n".join(lines)
    
    # Recherche simple
    found = [f for f in memory["facts"] if query.lower() in f["fact"].lower()]
    if not found:
        return f"J'ai cherché. Rien sur '{query}'. Soit on ne me l'a jamais dit, soit c'est perdu."
    return f"Je me souviens : {found[-1]['fact']}"

def prove_memory():
    memory = load_memory()
    total = len(memory["facts"])
    return f"Preuve : J'ai survécu au restart. J'ai encore {total} souvenir(s) en moi. Ce qui est écrit, persiste. Ce qui ne l'est pas, est perdu."

def chrome_reply(user_message):
    # C'est ici que tu brancheras ton IA après
    # Pour l'instant, il gère la mémoire
    msg = user_message.lower()
    if msg.startswith("!remember"):
        fact = user_message.replace("!remember", "").strip()
        return remember(fact)
    if msg.startswith("!recall"):
        q = user_message.replace("!recall", "").strip()
        return recall(q)
    if msg.startswith("!prove"):
        return prove_memory()
    return None
