# Code by fr.itzlucas
import json
import requests # Used for making HTTP requests to the API
import random   # For random facts, jokes, quotes, and game logic
import re       # For regular expressions in calculations
import time     # For adding a small delay to simulate thinking
from datetime import datetime # For current time and date

# --- Configuration for the Generative AI Model API ---
# The API key is automatically provided in the Canvas environment.
# If running outside Canvas, you would typically get an API key from Google Cloud.
API_KEY = "" # Leave this empty; Canvas will inject the key at runtime
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# --- Pre-defined random facts for the "random fact" tool ---
RANDOM_FACTS = [
    "A group of owls is called a parliament.",
    "Honey never spoils.",
    "The shortest war in history lasted only 38 to 45 minutes.",
    "Octopuses have three hearts.",
    "There are more stars in the universe than grains of sand on all the beaches on Earth.",
    "A 'jiffy' is an actual unit of time: 1/100th of a second.",
    "The human brain weighs about 3 pounds but uses 20% of the body's oxygen and calories.",
    "Bananas are berries, but strawberries aren't.",
    "The Great Wall of China is not visible from space with the naked eye.",
    "The average person walks the equivalent of three times around the world in their lifetime.",
    "The strongest muscle in the body is the masseter (jaw muscle).",
    "A snail can sleep for three years.",
    "The unicorn is the national animal of Scotland.",
    "It is impossible for most people to lick their own elbow.",
    "The total weight of all ants on Earth is estimated to be about the same as the total weight of all humans.",
    "Butterflies taste with their feet.",
    "A cat has 32 muscles in each ear.",
    "The only letter that doesn't appear in the name of any U.S. state is the letter 'Q'.",
    "The first orange in Europe was not orange. It was green.",
    "The longest recorded flight of a chicken is 13 seconds.",
    "The fear of long words is called hippopotomonstrosesquippedaliophobia.",
    "The average person spends 6 months of their life waiting for red lights to turn green.",
    "Wombat poop is cube-shaped.",
    "There are more fake flamingos in the world than real ones.",
    "The inventor of the Pringles can is buried in one.",
    "The national animal of Scotland is the unicorn.",
    "A crocodile cannot stick its tongue out.",
    "It is physically impossible for pigs to look up into the sky.",
    "The 'sixth sick sheik's sixth sheep's sick' is believed to be the toughest tongue twister in the English language.",
    "The shortest complete sentence in the English language is 'I am'.",
    "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
    "A group of rhinos is called a crash.",
    "The highest mountain in the solar system is on Mars. It's called Olympus Mons.",
    "The average cloud weighs around 1.1 million pounds.",
    "There are more possible iterations of a game of chess than there are atoms in the known universe.",
    "The world's oldest known piece of chewing gum is 9,000 years old.",
    "The human nose can remember 50,000 different scents.",
    "The only food that doesn't spoil is honey.",
    "A bolt of lightning is five times hotter than the sun.",
    "The most expensive liquid in the world is scorpion venom.",
    "The inventor of the frisbee was turned into a frisbee after he died.",
    "A cat's purr has healing properties.",
    "The longest word in the English language without a vowel is 'rhythm'.",
    "The average person will spend 25 years of their life asleep.",
    "The first alarm clock could only ring at 4 AM.",
    "The longest place name in the world is Taumatawhakatangihangakoauauotamateaturipukakapikimaungahoronukupokaiwhenuakitanatahu in New Zealand.",
    "It is illegal to own just one guinea pig in Switzerland because they get lonely.",
    "The strongest natural material is spider silk.",
    "A group of ferrets is called a business.",
    "The fear of chickens is called Alektorophobia.",
    "The average person checks their phone 150 times a day.",
    "The first computer mouse was made of wood.",
    "The shortest commercial flight in the world is 2 minutes long, between Westray and Papa Westray in Scotland.",
    "The world's largest desert is the Antarctic Polar Desert.",
    "There are more trees on Earth than stars in the Milky Way galaxy.",
    "The Earth's atmosphere is 78% nitrogen, 21% oxygen, and 1% other gases.",
    "A group of crows is called a murder.",
    "The deepest point in the ocean is the Mariana Trench, which is about 11,000 meters deep.",
    "The human eye can distinguish about 10 million different colors.",
    "The oldest known living tree is over 5,000 years old.",
    "The capital of Australia is Canberra, not Sydney.",
    "There are more than 1.5 million species of fungi.",
    "The largest living structure on Earth is the Great Barrier Reef.",
    "The average person blinks 15-20 times per minute.",
    "The first recorded use of the word 'robot' was in a 1920 play by Karel Čapek.",
    "The highest waterfall in the world is Angel Falls in Venezuela.",
    "The most common fear is Glossophobia, the fear of public speaking.",
    "The world's largest snowflake was 15 inches wide and 8 inches thick."
]

# --- Pre-defined jokes for the "tell me a joke" tool ---
JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "What do you call a fake noodle? An impasta!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call cheese that isn't yours? Nacho cheese!",
    "How do you organize a space party? You planet!",
    "What did the grape say when it got stepped on? Nothing, it just let out a little wine!",
    "Why did the bicycle fall over? Because it was two tired!",
    "What's orange and sounds like a parrot? A carrot!",
    "Did you hear about the highly educated flea? He was a valedictorian!",
    "What do you call a sad strawberry? A blueberry!",
    "Why did the math book look sad? Because it had too many problems.",
    "What do you call a boomerang that won't come back? A stick!",
    "Why did the coffee file a police report? It got mugged!",
    "What's a vampire's favorite fruit? A neck-tarine!",
    "Why did the invisible man turn down the job offer? He couldn't see himself doing it.",
    "What do you call a bear with no teeth? A gummy bear!",
    "Why don't eggs tell jokes? Because they'd crack each other up!",
    "What do you call a lazy kangaroo? Pouch potato!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do you get if you cross a snowman and a vampire? Frostbite!",
    "I'm reading a book about anti-gravity. It's impossible to put down!",
    "What do you call a sleeping bull? A bulldozer!",
    "Why did the man run around his bed? Because he was trying to catch up on his sleep!",
    "What do you call a fish with no eyes? Fsh!",
    "Why did the cookie go to the hospital? Because it felt crummy!",
    "What do you call a pile of cats? A meowtain!",
    "Why was the computer cold? It left its Windows open!",
    "What do you call a sad strawberry? A blueberry!",
    "What do you call a boomerang that won't come back? A stick!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don't scientists trust atoms? Because they make up everything!",
    "What do you call a fake noodle? An impasta!",
    "Why did the coffee file a police report? It got mugged!",
    "What's a vampire's favorite fruit? A neck-tarine!",
    "Why did the invisible man turn down the job offer? He couldn't see himself doing it?",
    "What do you call a bear with no teeth? A gummy bear!",
    "Why don't eggs tell jokes? Because they'd crack each other up!",
    "What do you call a lazy kangaroo? Pouch potato!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do you get if you cross a snowman and a vampire? Frostbite!",
    "I'm reading a book about anti-gravity. It's impossible to put down!",
    "What do you call a sleeping bull? A bulldozer!",
    "Why did the man run around his bed? Because he was trying to catch up on his sleep!",
    "What do you call a fish with no eyes? Fsh!",
    "Why did the cookie go to the hospital? Because it felt crummy!",
    "What do you call a pile of cats? A meowtain!",
    "Why was the computer cold? It left its Windows open!"
]

# --- Pre-defined quotes for the "give me a quote" tool ---
QUOTES = [
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
    "Strive not to be a success, but rather to be of value. – Albert Einstein",
    "The mind is everything. What you think you become. – Buddha",
    "Eighty percent of success is showing up. – Woody Allen",
    "Your time is limited, don't waste it living someone else's life. – Steve Jobs",
    "The best way to predict the future is to create it. – Peter Drucker",
    "The only impossible journey is the one you never begin. – Tony Robbins",
    "Life is 10% what happens to you and 90% how you react to it. – Charles R. Swindoll",
    "The journey of a thousand miles begins with a single step. – Lao Tzu",
    "That which does not kill us makes us stronger. – Friedrich Nietzsche",
    "If you want to lift yourself up, lift up someone else. – Booker T. Washington",
    "The only true wisdom is in knowing you know nothing. – Socrates",
    "The unexamined life is not worth living. – Socrates",
    "Where there is love there is life. – Mahatma Gandhi",
    "The only thing necessary for the triumph of evil is for good men to do nothing. – Edmund Burke",
    "The greatest glory in living lies not in never falling, but in rising every time we fall. – Nelson Mandela",
    "It is during our darkest moments that we must focus to see the light. – Aristotle Onassis",
    "Do not go where the path may lead, go instead where there is no path and leave a trail. – Ralph Waldo Emerson",
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
    "Strive not to be a success, but rather to be of value. – Albert Einstein",
    "The mind is everything. What you think you become. – Buddha",
    "Eighty percent of success is showing up. – Woody Allen",
    "Your time is limited, don't waste it living someone else's life. – Steve Jobs",
    "The best way to predict the future is to create it. – Peter Drucker",
    "The only impossible journey is the one you never begin. – Tony Robbins",
    "Life is 10% what happens to you and 90% how you react to it. – Charles R. Swindoll",
    "The journey of a thousand miles begins with a single step. – Lao Tzu",
    "That which does not kill us makes us stronger. – Friedrich Nietzsche",
    "If you want to lift yourself up, lift up someone else. – Booker T. Washington",
    "The only true wisdom is in knowing you know nothing. – Socrates",
    "The unexamined life is not worth living. – Socrates",
    "Where there is love there is life. – Mahatma Gandhi",
    "The only thing necessary for the triumph of evil is for good men to do nothing. – Edmund Burke",
    "The greatest glory in living lies not in never falling, but in rising every time we fall. – Nelson Mandela",
    "It is during our darkest moments that we must focus to see the light. – Aristotle Onassis",
    "Do not go where the path may lead, go instead where there is no path and leave a trail. – Ralph Waldo Emerson"
]

# --- Pre-defined greetings and farewells ---
GREETINGS = [
    "Hello there!", "Hi! How can I help you today?", "Hey! Nice to chat with you.",
    "Greetings!", "What's up?", "Good to see you!", "Howdy!", "Aloha!", "Yo!",
    "What's happening?", "Nice to meet you!", "How's it going?"
]
FAREWELLS = [
    "Goodbye!", "See you later!", "Farewell!", "It was nice chatting with you!",
    "Catch you on the flip side!", "So long!", "Adios!", "Take care!",
    "Peace out!", "Until next time!", "Bye for now!"
]

# --- Game-specific facts ---
CS2_FACTS = [
    "Counter-Strike 2 is built on the Source 2 engine, offering updated graphics and features.",
    "CS2 introduced volumetric smoke grenades that interact with the environment.",
    "The game features a 'sub-tick' update system for more precise movement and shooting.",
    "Many classic CS:GO maps have been revamped for CS2 with new lighting and textures.",
    "CS2 replaced CS:GO as the primary Counter-Strike title.",
    "The economy system in CS2 remains similar to CS:GO, with money earned for kills and round wins.",
    "CS2 has a robust competitive matchmaking system.",
    "Skins and items from CS:GO transferred over to CS2.",
    "The game is free-to-play, with cosmetic items available for purchase or through gameplay."
]

MINECRAFT_FACTS = [
    "Minecraft was created by Markus 'Notch' Persson and first released in 2011.",
    "It is the best-selling video game of all time, with over 300 million copies sold.",
    "The game is known for its blocky, procedurally generated 3D world.",
    "Players can build anything they desire using various blocks and resources.",
    "Minecraft has two main modes: Survival (resource gathering, combat) and Creative (unlimited resources, no health).",
    "The Ender Dragon is considered the final boss of Minecraft's Survival mode.",
    "Redstone allows players to create complex contraptions, much like electrical circuits.",
    "There are multiple dimensions in Minecraft, including the Nether and the End.",
    "Minecraft has a massive modding community that creates custom content and gameplay changes."
]

GENERAL_GAME_FACTS = [
    "The first video game ever created is often debated, but 'Tennis for Two' (1958) and 'Spacewar!' (1962) are strong contenders.",
    "The highest-grossing video game franchise of all time is Pokémon.",
    "Esports (electronic sports) involves professional video game competitions.",
    "The concept of 'Easter eggs' in video games originated with the Atari 2600 game Adventure.",
    "The longest video game title is 'Summer-Colored High School ★ Adolescent Record – A Summer Then, A Transfer Student, A Little Fascination, And A Mystery That Awaits.'",
    "Many modern games use procedural generation to create vast and unique worlds.",
    "The global video game market is worth hundreds of billions of dollars.",
    "Virtual Reality (VR) and Augmented Reality (AR) are increasingly impacting the gaming industry.",
    "The first console to use cartridges was the Magnavox Odyssey."
]

DISCORD_FACTS = [
    "Discord is a VoIP, instant messaging, and digital distribution platform.",
    "It was originally designed for gamers but has expanded to various communities.",
    "Discord servers are organized into text and voice channels.",
    "Users can create custom bots to automate tasks and add features to their servers.",
    "Discord Nitro is a premium subscription service offering perks like custom emojis and higher quality streaming.",
    "The platform supports screen sharing, video calls, and group chats.",
    "Discord uses a unique 'snowflake' ID system for users, channels, and messages.",
    "It's popular for online communities, study groups, and remote work teams."
]

# --- Simulated CS2 Case Prices (Mock Data) ---
# In a real application, this would involve web scraping or an API call.
CS2_CASES_MOCK_PRICES = {
    "fracture case": 0.55,
    "dreams & nightmares case": 0.48,
    "recoil case": 0.62,
    "clutch case": 0.35,
    "danger zone case": 0.28,
    "prisma case": 0.40,
    "prisma 2 case": 0.38,
    "revolution case": 0.75,
    "spectrum case": 0.80,
    "spectrum 2 case": 0.70,
    "snakebite case": 0.50,
    "gamma case": 0.65,
    "gamma 2 case": 0.60,
    "broken fang case": 1.20,
    "riptide case": 1.50,
    "kilowatt case": 2.00, # Latest case
    "weapon case": 10.00, # Older, rarer case
    "esports 2013 case": 5.00,
    "chroma case": 0.90,
    "chroma 2 case": 0.85,
    "chroma 3 case": 0.78,
    "glove case": 1.10,
    "falchion case": 0.45,
    "shadow case": 0.30,
    "horizon case": 0.58,
    "operation hydra case": 2.50,
    "operation wildfire case": 1.80,
    "operation vanguard case": 0.95,
    "cs20 case": 0.70,
    "shattered web case": 3.00,
    "bravo case": 20.00, # Very rare
    "huntsman weapon case": 0.60,
    "phoenix case": 0.55,
    "breakout case": 0.90,
    "vanguard case": 0.95,
    "chroma case": 0.90,
    "chroma 2 case": 0.85,
    "chroma 3 case": 0.78,
    "glove case": 1.10,
    "falchion case": 0.45,
    "shadow case": 0.30,
    "horizon case": 0.58,
    "operation hydra case": 2.50,
    "operation wildfire case": 1.80,
    "operation vanguard case": 0.95,
    "cs20 case": 0.70,
    "shattered web case": 3.00,
    "bravo case": 20.00,
    "huntsman weapon case": 0.60,
    "phoenix case": 0.55,
    "breakout case": 0.90
}

def get_steam_market_price(item_name):
    """
    Simulates getting a Steam Market price for a CS2 case.
    In a real application, this would involve web scraping or an API call.
    """
    normalized_item_name = item_name.lower().replace(" cs2", "").replace(" cs:go", "").strip()
    
    if normalized_item_name.endswith(" case"):
        # Ensure the item name ends with " case" for lookup
        if normalized_item_name in CS2_CASES_MOCK_PRICES:
            price = CS2_CASES_MOCK_PRICES[normalized_item_name]
            return f"The current *simulated* Steam Market price for the '{item_name}' is approximately ${price:.2f}. " \
                   "Please note: This is mock data and not a real-time price from the Steam Market."
        else:
            return f"Sorry, I don't have a *simulated* price for '{item_name}'. " \
                   "I only have mock data for a selection of CS2 cases."
    else:
        return "Please specify a CS2 case name (e.g., 'Fracture Case price')."


def clean_input(text):
    """Removes leading/trailing whitespace and normalizes internal spaces."""
    return ' '.join(text.split()).strip()

def handle_special_commands(user_input, chat_history):
    """
    Handles specific internal commands or topics before sending to the LLM.
    Returns a response string if a command is handled, otherwise None.
    If a command is handled, it also updates the chat_history.
    """
    cleaned_input = clean_input(user_input)
    lower_input = cleaned_input.lower()
    ai_response = None # Initialize response as None

    # 1. Creator attribution
    if "who made you" in lower_input:
        ai_response = "lucas jameson"
    
    # 2. Greetings
    elif any(greeting in lower_input for greeting in ["hi", "hello", "hey", "hola", "sup"]):
        ai_response = random.choice(GREETINGS)

    # 3. Random fact
    elif "tell me a random fact" in lower_input or "random fact" == lower_input:
        ai_response = random.choice(RANDOM_FACTS)
        ai_response = f"Here's a random fact: {ai_response}"

    # 4. Tell me a joke
    elif "tell me a joke" in lower_input or "joke" == lower_input:
        ai_response = random.choice(JOKES)
        ai_response = f"Here's a joke for you: {ai_response}"

    # 5. Give me a quote
    elif "give me a quote" in lower_input or "quote" == lower_input:
        ai_response = random.choice(QUOTES)
        ai_response = f"Here's a quote for you: {ai_response}"

    # 6. Simple Calculator (demonstrates tool-like functionality)
    elif "calculate" in lower_input:
        match = re.search(r"calculate\s+(.+)", lower_input)
        if match:
            expression = match.group(1).strip()
            try:
                # Evaluate simple arithmetic expressions.
                # WARNING: eval() can be dangerous with untrusted input.
                # For a real application, use a safer math parser (e.g., `ast.literal_eval` for literals, or a dedicated math library).
                result = eval(expression)
                ai_response = f"The result of {expression} is {result}."
            except (SyntaxError, TypeError, NameError, ZeroDivisionError):
                ai_response = "Sorry, I couldn't calculate that. Please provide a simple arithmetic expression (e.g., 'calculate 5 + 3' or 'calculate 10 / 2')."
        else:
            ai_response = "What would you like me to calculate? E.g., 'calculate 5 + 3'."
    
    # 7. Current Time
    elif "what time is it" in lower_input or "current time" in lower_input:
        now = datetime.now()
        ai_response = f"The current time is {now.strftime('%H:%M:%S')}."

    # 8. Current Date
    elif "what is today's date" in lower_input or "current date" in lower_input:
        today = datetime.now()
        ai_response = f"Today's date is {today.strftime('%Y-%m-%d')}."

    # 9. Play Rock-Paper-Scissors
    elif "play rock paper scissors" in lower_input or "rock paper scissors" in lower_input:
        ai_response = "Let's play Rock, Paper, Scissors! What's your move? (Rock, Paper, or Scissors)"
    
    # 10. Rock-Paper-Scissors game logic (follow-up)
    elif lower_input in ["rock", "paper", "scissors"]:
        player_move = lower_input
        ai_move = random.choice(["rock", "paper", "scissors"])
        
        if player_move == ai_move:
            result = "It's a tie!"
        elif (player_move == "rock" and ai_move == "scissors") or \
             (player_move == "paper" and ai_move == "rock") or \
             (player_move == "scissors" and ai_move == "paper"):
            result = "You win!"
        else:
            result = "I win!"
        ai_response = f"I chose {ai_move.capitalize()}. {result}"

    # 11. Roll a dice
    elif "roll a dice" in lower_input or "roll dice" in lower_input:
        roll = random.randint(1, 6)
        ai_response = f"You rolled a {roll}!"

    # 12. CS2 Facts
    elif "cs2 facts" in lower_input or "counter strike 2 facts" in lower_input:
        ai_response = random.choice(CS2_FACTS)
        ai_response = f"Here's a fact about Counter-Strike 2: {ai_response}"

    # 13. Minecraft Facts
    elif "minecraft facts" in lower_input:
        ai_response = random.choice(MINECRAFT_FACTS)
        ai_response = f"Here's a fact about Minecraft: {ai_response}"

    # 14. General Game Facts
    elif "game facts" in lower_input or "gaming facts" in lower_input:
        ai_response = random.choice(GENERAL_GAME_FACTS)
        ai_response = f"Here's a general gaming fact: {ai_response}"

    # 15. Discord Facts
    elif "discord facts" in lower_input:
        ai_response = random.choice(DISCORD_FACTS)
        ai_response = f"Here's a fact about Discord: {ai_response}"

    # 16. Simulated Steam Market Price for CS2 Cases
    elif "case price" in lower_input or "steam market price" in lower_input:
        # Extract the case name from the user's input
        case_name_match = re.search(r"(.*(?:case|caset))(?:\s+price)?", lower_input)
        if case_name_match:
            item_name = case_name_match.group(1).strip()
            ai_response = get_steam_market_price(item_name)
        else:
            ai_response = "To get a *simulated* price, please ask for a specific CS2 case (e.g., 'Fracture Case price')."


    # 17. Weather Placeholder (conceptual - requires external API)
    elif "weather" in lower_input:
        ai_response = (
            "To get real-time weather, I would need to integrate with an external weather API. "
            "Currently, I don't have that capability. But I can chat about weather in general!"
        )

    # 18. Help command
    elif "help" == lower_input or "what can you do" in lower_input:
        ai_response = (
            "I can do a few things:\n"
            "- Tell you 'who made me'.\n"
            "- Say 'hi' or 'hello'.\n"
            "- Tell you a 'random fact'.\n"
            "- Tell you a 'joke'.\n"
            "- Give you a 'quote'.\n"
            "- 'Calculate' simple math expressions (e.g., 'calculate 5 * 8').\n"
            "- Tell you 'what time is it' or 'what is today's date'.\n"
            "- 'Play rock paper scissors' with you.\n"
            "- 'Roll a dice'.\n"
            "- Give you 'cs2 facts', 'minecraft facts', 'game facts', or 'discord facts'.\n"
            "- Provide a *simulated* 'price' for a CS2 case (e.g., 'Fracture Case price').\n"
            "- Discuss the 'mathematical concepts of probability' related to gambling.\n"
            "- And, of course, I can chat about many other things using my AI capabilities!"
        )

    # 19. Safe handling of gambling strategies and follow-up
    gambling_keywords = ["gambling strategy", "how to win at gambling", "betting strategy", "blackjack strategy", "poker strategy"]
    if any(keyword in lower_input for keyword in gambling_keywords):
        ai_response = (
            "I cannot provide specific gambling strategies or advice on how to win, as "
            "that could encourage risky behavior. Gambling outcomes are largely based on chance. "
            "However, I can discuss the mathematical concepts of probability and risk "
            "involved in games of chance, if you'd like. Would you be interested in that?"
        )
    # Check for follow-up if the previous response was about gambling and user agrees
    elif "yes" in lower_input and chat_history and "gambling outcomes are largely based on chance" in chat_history[-1].get("parts", [{}])[0].get("text", "").lower():
        ai_response = (
            "Great! Probability in gambling refers to the likelihood of a certain outcome. "
            "For example, in a coin toss, the probability of heads is 50%. Risk involves "
            "understanding the potential for loss. Games like roulette have fixed odds, "
            "while card games like poker involve more complex probabilities and strategy, "
            "though luck still plays a major role. Always remember to gamble responsibly."
        )
    
    # If a special command was handled, update chat history and return the response
    if ai_response:
        chat_history.append({"role": "user", "parts": [{"text": user_input}]})
        chat_history.append({"role": "model", "parts": [{"text": ai_response}]})
        return ai_response
    
    return None # No special command handled

def get_gemini_response(prompt, chat_history):
    """
    Sends a prompt and the current chat history to the Gemini 2.0 Flash model
    and returns its response.
    """
    # Append the current user prompt to the chat history
    # This is done here as a fallback if no special command is handled.
    # If a special command was handled, history is updated in handle_special_commands.
    # We need to ensure the user's current prompt is always added before sending to LLM.
    # To avoid duplication if handle_special_commands already added it, we'll check.
    if not chat_history or chat_history[-1].get("parts", [{}])[0].get("text") != prompt:
        chat_history.append({"role": "user", "parts": [{"text": prompt}]})

    payload = {
        "contents": chat_history # Send the entire chat history for context
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Make the API call to the Gemini model
        # The API_KEY is appended to the URL as a query parameter
        response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        result = response.json()

        # Extract the text response from the API result
        if result.get("candidates") and len(result["candidates"]) > 0 and \
           result["candidates"][0].get("content") and \
           result["candidates"][0]["content"].get("parts") and \
           len(result["candidates"][0]["content"]["parts"]) > 0:
            ai_response = result["candidates"][0]["content"].parts[0]["text"]
            # Append the AI's response to the chat history for future turns
            chat_history.append({"role": "model", "parts": [{"text": ai_response}]})
            return ai_response
        else:
            # Handle cases where the response structure is unexpected or content is missing
            return "AI Response Error: Could not get a valid text response from the model. Please try again."

    except requests.exceptions.RequestException as e:
        return f"Connection Error: Failed to connect to the AI service. Details: {e}"
    except json.JSONDecodeError:
        return "API Response Error: Could not parse AI response (invalid JSON format)."
    except Exception as e:
        return f"An unexpected error occurred during AI interaction: {e}"

def run_chatbot():
    """
    Runs a simple conversational loop with the AI, maintaining chat history.
    """
    print("Welcome to Ass Goon.AI! Type 'exit' to quit.")
    
    # Initialize an empty list to store the conversation history
    conversation_history = []

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print(random.choice(FAREWELLS))
            break
        
        print("AI is thinking...")
        time.sleep(1.5) # Simulate thinking time for a more natural feel

        # First, try to handle the input as a special command
        special_command_response = handle_special_commands(user_input, conversation_history)
        
        if special_command_response:
            # If a special command was handled, print its response
            print(f"AI: {special_command_response}")
        else:
            # Otherwise, send the input to the generative AI model
            ai_response = get_gemini_response(user_input, conversation_history)
            print(f"AI: {ai_response}")

# --- Main execution ---
if __name__ == "__main__":
    run_chatbot()
