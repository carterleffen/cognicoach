import re
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from termcolor import colored

from pydantic import BaseModel, Field

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain.schema import BaseLanguageModel, Document
from langchain.vectorstores import FAISS

import math
import faiss

from gen_agent import GenerativeAgent

USER_NAME = "echo" # The name you want to use when interviewing the agent.
LLM = ChatOpenAI(max_tokens=1500) # Can be any LLM you want.

import math
import faiss

def relevance_score_fn(score: float) -> float:
    """Return a similarity score on a scale [0, 1]."""
    # This will differ depending on a few things:
    # - the distance / similarity metric used by the VectorStore
    # - the scale of your embeddings (OpenAI's are unit norm. Many others are not!)
    # This function converts the euclidean norm of normalized embeddings
    # (0 is most similar, sqrt(2) most dissimilar)
    # to a similarity function (0 to 1)
    return 1.0 - score / math.sqrt(2)

def create_new_memory_retriever():
    """Create a new vector store retriever unique to the agent."""
    # Define your embedding model
    embeddings_model = OpenAIEmbeddings()
    # Initialize the vectorstore as empty
    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {}, relevance_score_fn=relevance_score_fn)
    return TimeWeightedVectorStoreRetriever(vectorstore=vectorstore, other_score_keys=["importance"], k=15)    

tommie = GenerativeAgent(name="Tommie", 
              age=25,
              traits="anxious, likes design", # You can add more persistent traits here 
              status="looking for a job", # When connected to a virtual world, we can have the characters update their status
              memory_retriever=create_new_memory_retriever(),
              llm=LLM,
              daily_summaries = [
                   "Drove across state to move to a new town but doesn't have a job yet."
               ],
               reflection_threshold = 8, # we will give this a relatively low number to show how reflection works
             )

# print(tommie.get_summary()) # currently there are no memories

# # Let's add a memory
tommie.add_memory("Tommie moved to a new town and is looking for a job.")


# print(tommie.get_summary(force_refresh=True)) # now we have a memory

# #we can add more memories
tommie_memories = [
    "Tommie is looking for a job.",
    "Tommie exercises every day.",
    "Tommie's favorite food is pizza.",
    "Tommie likes to play video games with friends.",
    "Tommie is a good friend.",

]

for memory in tommie_memories:
    tommie.add_memory(memory)

# print(tommie.get_summary(force_refresh=True)) # now we have more memories

def interview_agent(agent: GenerativeAgent, message: str) -> str:
    """Help the notebook user interact with the agent."""
    new_message = f"{USER_NAME} says {message}"
    return agent.generate_dialogue_response(new_message)[1]

# # we can interview the character
# while True:
#     message = input("You say: ")
#     response = interview_agent(tommie, message)
#     print(f"{tommie.name} says: {response}")

# # Let's have Tommie start going through a day in the life.
observations = [
    "Tommie wakes up to the sound of a noisy construction site outside his window.",
    "Tommie gets out of bed and heads to the kitchen to make himself some coffee.",
    "Tommie realizes he forgot to buy coffee filters and starts rummaging through his moving boxes to find some.",
    "Tommie finally finds the filters and makes himself a cup of coffee.",
    "The coffee tastes bitter, and Tommie regrets not buying a better brand.",
    "Tommie checks his email and sees that he has no job offers yet.",
    "Tommie spends some time updating his resume and cover letter.",
    "Tommie heads out to explore the city and look for job openings.",
    "Tommie sees a sign for a job fair and decides to attend.",
    "The line to get in is long, and Tommie has to wait for an hour.",
    "Tommie meets several potential employers at the job fair but doesn't receive any offers.",
    "Tommie leaves the job fair feeling disappointed.",
    "Tommie stops by a local diner to grab some lunch.",
    "The service is slow, and Tommie has to wait for 30 minutes to get his food.",
    "Tommie overhears a conversation at the next table about a job opening.",
    "Tommie asks the diners about the job opening and gets some information about the company.",
    "Tommie decides to apply for the job and sends his resume and cover letter.",
    "Tommie continues his search for job openings and drops off his resume at several local businesses.",
    "Tommie takes a break from his job search to go for a walk in a nearby park.",
    "A dog approaches and licks Tommie's feet, and he pets it for a few minutes.",
    "Tommie sees a group of people playing frisbee and decides to join in.",
    "Tommie has fun playing frisbee but gets hit in the face with the frisbee and hurts his nose.",
    "Tommie goes back to his apartment to rest for a bit.",
    "A raccoon tore open the trash bag outside his apartment, and the garbage is all over the floor.",
    "Tommie starts to feel frustrated with his job search.",
    "Tommie calls his best friend to vent about his struggles.",
    "Tommie's friend offers some words of encouragement and tells him to keep trying.",
    "Tommie feels slightly better after talking to his friend.",
]

# # Let's send Tommie on their way. We'll check in on their summary every few observations to watch it evolve
# for i, observation in enumerate(observations):
#     _, reaction = tommie.generate_reaction(observation)
#     print(colored(observation, "green"), reaction)
#     if ((i+1) % 5) == 0:
#         print('*'*40)
#         print(colored(f"After {i+1} observations, Tommie's summary is:\n{tommie.get_summary(force_refresh=True)}", "blue"))
#         print('*'*40)

# # we can interview the character
# while True:
#     message = input("You say: ")
#     response = interview_agent(tommie, message)
#     print(f"{tommie.name} says: {response}")

eve = GenerativeAgent(name="Eve", 
              age=34, 
              traits="curious, helpful", # You can add more persistent traits here 
              status="N/A", # When connected to a virtual world, we can have the characters update their status
              memory_retriever=create_new_memory_retriever(),
              llm=LLM,
              daily_summaries = [
                  ("Eve started her new job as a career counselor last week and received her first assignment, a client named Tommie.")
              ],
                reflection_threshold = 5,
             )

yesterday = (datetime.now() - timedelta(days=1)).strftime("%A %B %d")
eve_memories = [
    "Eve overhears her colleague say something about a new client being hard to work with",
    "Eve wakes up and hear's the alarm",
    "Eve eats a boal of porridge",
    "Eve helps a coworker on a task",
    "Eve plays tennis with her friend Xu before going to work",
    "Eve overhears her colleague say something about Tommie being hard to work with",
    
]
for memory in eve_memories:
    eve.add_memory(memory)

# print(eve.get_summary())

# # we can interview the character
# while True:
#     message = input("You say: ")
#     response = interview_agent(eve, message)
#     print(f"{tommie.name} says: {response}")

def run_conversation(agents: List[GenerativeAgent], initial_observation: str) -> None:
    """Runs a conversation between agents."""
    _, observation = agents[1].generate_reaction(initial_observation)
    print(observation)
    turns = 0
    while True:
        break_dialogue = False
        for agent in agents:
            stay_in_dialogue, observation = agent.generate_dialogue_response(observation)
            print(observation)
            # observation = f"{agent.name} said {reaction}"
            if not stay_in_dialogue:
                break_dialogue = True   
        if break_dialogue:
            break
        turns += 1

agents = [tommie, eve]
run_conversation(agents, "Tommie said: Hi, Eve. Thanks for agreeing to share your story with me and give me advice. I have a bunch of questions.")

# # We can see a current "Summary" of a character based on their own perception of self has changed
# # print(tommie.get_summary(force_refresh=True))
# # print(eve.get_summary(force_refresh=True))

# # we can interview the character
# while True:
#     character = input("Which character do you want to interview? ").lower()
#     if character == "tommie":
#         character = tommie
#     elif character == "eve":
#         character = eve
#     message = input("You say: ")
#     response = interview_agent(character, message)
#     print(f"{character.name} says: {response}")