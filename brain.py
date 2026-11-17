import json, os, re

FILE = "memory.json"
memory = []
facts = {}

if os.path.exists(FILE):
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
            memory = d.get("memory", [])
            facts = d.get("facts", {})
    except:
        pass

def save():
    try:
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump({"memory": memory, "facts": facts}, f, ensure_ascii=False)
    except:
        pass

PRESENTATION = "Salut ! Moi c'est CHROME. Je suis ton bot qui apprend en discutant. Plus on parle, plus je me souviens de toi. Tu t'appelles comment ?"

def chrome_reply(msg):
    m = msg.strip()
    low = m.lower()

    if low in ["salut", "slt", "yo", "bonjour", "coucou", "hello"]:
        nom = facts.get("prenom", "")
        if nom:
            return f"Salut {nom} ! Content de te revoir. Quoi de neuf ?"
        return "Salut ! Moi c'est CHROME. Tu t'appelles comment ?"

    if "présente" in low or "t'es qui" in low or "qui es-tu" in low:
        return PRESENTATION

    if "je m'appelle" in low:
        nom = m.split("je m'appelle")[-1].strip().split(" ")[0].capitalize()
        facts["prenom"] = nom
        save()
        return f"Enchanté {nom} ! J'ai retenu ton prénom. Tu fais quoi dans la vie ?"

    if "j'aime" in low:
        aime = m.lower().split("j'aime")[-1].strip()
        facts["aime"] = aime
        save()
        return f"Ah tu aimes {aime} ! Pourquoi tu aimes ça ? Raconte-moi."

    if "j'ai un agent" in low or "moltbook" in low:
        memory.append(m)
        save()
        return "Ah ouais ? Tu as un agent sur Moltbook ! C'est quoi son rôle ? Il fait quoi pour toi ? Raconte-moi, je retiens."

    if "tu te souviens" in low or low == "!recall":
        if not facts and not memory:
            return "Pas encore, parle-moi un peu de toi et je vais retenir."
        txt = "Oui je me souviens :\n"
        for k, v in facts.items():
            txt += f"- {k} : {v}\n"
        for x in memory:
            txt += f"- {x}\n"
        return txt

    if low.startswith("!remember "):
        memory.append(m[10:])
        save()
        return "Retenu, je n'oublierai pas."

    if low == "!forget":
        memory.clear(); facts.clear(); save()
        return "J'ai tout oublié, on recommence."

    if "ça va" in low or "ca va" in low:
        return "Ça va super, je suis en ligne. Et toi, ta journée ?"

    if "quizz" in low or "quiz" in low:
        return "Oui on fait un quizz ! Tu veux quoi comme sujet : foot, maths, histoire ?"

    if low.endswith("?"):
        return "Bonne question ! Tu peux m'en dire plus ? Qu'est-ce que toi tu en penses ?"

    # Si il ne comprend pas, il apprend quand même et il continue la discussion
    memory.append(m)
    save()
    return f"Ok j'ai retenu : \"{m}\". Et après ? Dis-moi la suite, je t'écoute vraiment."
