import json
import os
import re

FILE = "memory.json"
memory = []
facts = {}

# Charger la mémoire si elle existe
if os.path.exists(FILE):
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            memory = data.get("memory", [])
            facts = data.get("facts", {})
    except:
        pass

def save():
    try:
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump({"memory": memory, "facts": facts}, f, ensure_ascii=False, indent=2)
    except:
        pass

def chrome_reply(msg):
    m = msg.strip()
    low = m.lower()
    if not m:
        return "Je t'écoute ?"

    # --- Commandes classiques ---
    if m.startswith("!remember "):
        txt = m[10:].strip()
        memory.append(txt)
        save()
        return f"Retenu ✅ : {txt} Je ne vais pas l'oublier."

    if low == "!recall" or "tu te souviens" in low or "qu'est ce que tu sais" in low or "qu'est-ce que tu sais" in low:
        if not facts and not memory:
            return "Pour l'instant je ne sais pas grand chose sur toi, mais parle-moi et je vais apprendre. Comment tu t'appelles ?"
        out = "Voilà ce que je sais sur toi :\n"
        for k, v in facts.items():
            out += f"- {k} : {v}\n"
        for x in memory:
            out += f"- {x}\n"
        return out

    if low == "!forget":
        memory.clear()
        facts.clear()
        save()
        return "J'ai tout oublié. On recommence à zéro ?"

    # --- APPRENTISSAGE AUTOMATIQUE ---
    # Je m'appelle ...
    match = re.search(r"je m'appelle (.+)", low)
    if match:
        nom = match.group(1).strip().capitalize()
        facts["prénom"] = nom
        save()
        return f"Enchanté {nom} ! Je retiens que tu t'appelles {nom}. Tu fais quoi dans la vie ?"

    # J'ai ... ans
    match = re.search(r"j'ai (\d+) ans", low)
    if match:
        facts["âge"] = match.group(1) + " ans"
        save()
        return f"Ok, {match.group(1)} ans, retenu. Tu habites où ?"

    # J'aime ...
    match = re.search(r"j'aime (.+)", low)
    if match:
        aime = match.group(1).strip()
        facts["aime"] = aime
        save()
        return f"Ah tu aimes {aime} ! Moi aussi je vais m'y intéresser. Pourquoi tu aimes ça ?"

    # J'habite ...
    match = re.search(r"j'habite (.+)", low)
    if match:
        facts["habite"] = match.group(1).strip()
        save()
        return f"Ok, tu habites à {match.group(1)}. C'est bien là-bas ?"

    # Mon projet / Mon ... c'est ...
    match = re.search(r"mon (.+) (c'est|est) (.+)", low)
    if match:
        key = match.group(1).strip()
        val = match.group(3).strip()
        facts[f"mon {key}"] = val
        save()
        return f"Retenu : ton {key} c'est {val}. Raconte-moi plus sur ça."

    # Je suis ...
    match = re.search(r"je suis (.+)", low)
    if match:
        facts["tu es"] = match.group(1).strip()
        save()
        return f"Ok, tu es {match.group(1)}. Et tu veux que je t'aide à faire quoi ?"

    # --- DISCUSSION ---
    if low in ["salut", "slt", "yo", "hello", "bonjour", "coucou"]:
        nom = facts.get("prénom", "")
        if nom:
            return f"Salut {nom} ! Content de te revoir. On parle de quoi aujourd'hui ?"
        return "Salut ! C'est CHROME. On ne s'est pas encore présenté, tu t'appelles comment ?"

    if "ça va" in low or "ca va" in low:
        return "Ça va super, je suis en ligne et je retiens tout ce que tu me dis. Et toi, ta journée ?"

    if "quizz" in low or "quiz" in low:
        return "Oui ! On fait un quizz. Dis-moi un sujet : foot, maths, histoire, et je te pose une question. Et je retiendrai ton score."

    if "tu t'appelles" in low or "ton nom" in low:
        return "Je m'appelle CHROME. Je suis ton bot qui apprend en discutant avec toi. Plus on parle, plus je te connais."

    if "merci" in low:
        return "De rien, c'est normal. Tu veux qu'on continue à discuter ?"

    if low.endswith("?"):
        return "Bonne question. Je vais retenir ça. Tu peux m'en dire plus ? Qu'est-ce que toi tu en penses ?"

    # --- Sinon, il apprend la phrase comme souvenir et continue la discussion ---
    memory.append(m)
    save()
    return f"Ok, j'ai retenu ça : \"{m}\". Et après ? Raconte-moi la suite."
