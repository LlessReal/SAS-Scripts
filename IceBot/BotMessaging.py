from config import CurrentPath, api_key, openrouterapikey
import GuiMaker, SoundFunctions, pyttsx3, IceBarFunctions, SchizoRadio, Initiation, time
from huggingface_hub import InferenceClient
from openai import OpenAI

client = InferenceClient(provider="novita", api_key=api_key)
OpenRouterClient = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=openrouterapikey)

engine = pyttsx3.init() # Initialize the engine
# Adjust speaking rate and volume, and get male voice
engine.setProperty('rate', 150); engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices'); engine.setProperty('voice', voices[0].id)

### Message Context
PhoneNumDetails = open(fr"{CurrentPath}\Details.txt","r", encoding='utf-8', errors='ignore').read()
SystemMessage = f"""You are a bot at Columbus State University meant to transfer people to the right number depending on what they ask for
You'll be transfering them from the numbers below. 
if you're going to transfer them to a number, say, '[INITIATE TRANSFER - (The Number)]' AT THE VERY END of your response, and replace (The Number) with the actual number you're transfering them to of course.
If you need more information, let them know and then say '[NEED MORE INFO]' AT THE VERY END of your response
{PhoneNumDetails}"""

def GenerateBotResponse(DetailsExplained):
    while GuiMaker.WaitBeforeRadio.get() == 1: time.sleep(1)
    SoundFunctions.playVoiceLine("PleaseWait")
    if GuiMaker.AutoChangeSongToggle.get() == 1: SchizoRadio.RadioControl("Change Song")
    SchizoRadio.RadioControl("On")
    # Generate bot's response
    MessageLogs = [
                {'role': 'system', 'content': SystemMessage},
                {'role': 'user', 'content': "A caller has said the following message: Can you give me admissions?\nRespond to the caller's message"},
                {'role': 'assistant', 'content': "Alright, you will be transferred to admissions shortly. [INITIATE TRANSFER - 6001]"},
                {'role': 'user', 'content': "A caller has said the following message: Hey, I was wondering where I would go for orientation?\nRespond to the caller's message"},
                {'role': 'assistant', 'content': "I can have the orientation department help you with that. Please hold while I transfer you. [INITIATE TRANSFER - 7065078593]"},
                {'role': 'user', 'content': "A caller has said the following message: Hey! I was calling about a hold on my account.\nRespond to the caller's message"},
                {'role': 'assistant', 'content': "What type of hold are we talking about? [NEED MORE INFO]"},
                {'role': 'user', 'content': "The caller has responded with the following message: It says I need to schedule a meeting with my advisor.\nRespond to the caller's message"},
                {'role': 'assistant', 'content': "Ah ok, to get rid of that hold, you need to schedule a meeting with your advisor. I'll transfer you to the advising department for more info. [INITIATE TRANSFER - 7065078780]"},
                {'role': 'user', 'content': DetailsExplained},
                ]
    completion = OpenRouterClient.chat.completions.create(model="meta-llama/llama-3.3-70b-instruct:free", messages=MessageLogs)
    BotsResponse = completion.choices[0].message.content # Storing
    """
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct", 
            messages=[
                {'role': 'system', 'content': SystemMessage},
                {'role': 'user', 'content': "A caller has said the following message: Can you give me admissions?\nRespond to the caller's message"},
                {'role': 'assistant', 'content': "Alright, you will be transferred to admissions shortly. [INITIATE TRANSFER - 6001]"},
                {'role': 'user', 'content': "A caller has said the following message: Hey, I was wondering where I would go for orientation?\nRespond to the caller's message"},
                {'role': 'assistant', 'content': "I can have the orientation department help you with that. Please hold while I transfer you. [INITIATE TRANSFER - 7065078593]"},
                {'role': 'user', 'content': "A caller has said the following message: Hey! I was calling about a hold on my account.\nRespond to the caller's message"},
                {'role': 'assistant', 'content': "What type of hold are we talking about? [NEED MORE INFO]"},
                {'role': 'user', 'content': "The caller has responded with the following message: It says I need to schedule a meeting with my advisor.\nRespond to the caller's message"},
                {'role': 'assistant', 'content': "Ah ok, to get rid of that hold, you need to schedule a meeting with your advisor. I'll transfer you to the advising department for more info. [INITIATE TRANSFER - 7065078780]"},
                {'role': 'user', 'content': DetailsExplained},
                ], 
            max_tokens=500,
        )
        BotsResponse = completion.choices[0].message.content
    except Exception as e: print(f"Error running bot {e}"); return
    """
    SchizoRadio.RadioControl("Off")
    print(f"Bot's Response: {BotsResponse}")
    # Says the bot's response (Without the initiate part lol) and stop the engine after
    engine.say(BotsResponse.replace(BotsResponse[BotsResponse.find("[INITIATE"):],"")); engine.runAndWait(); engine.stop() 
    # Transfers or Asks for More Info
    if "INITIATE TRANSFER" in BotsResponse: 
        IceBarFunctions.AutoTransferSubmitVersion(TransferNumber=BotsResponse[BotsResponse.find("- ") + 2:BotsResponse.find("]")],SayVoiceLine=GuiMaker.TransferLineToggle.get(),WaitBeforeGo=GuiMaker.WaitToggle.get())
    elif "[NEED MORE INFO]" in BotsResponse: Initiation.GatherCallersInfo(NeedMoreInfo=True)