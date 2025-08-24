from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from dotenv import load_dotenv
from vertexai import rag
from google.adk.agents import Agent
from google.genai import types
from root_agent.prompt import my_prompt
import vertexai

AI_MODEL = 'gemini-2.5-flash'

vertexai.init(project="gglobo", location="us-east4")

# Load environment variables from .env file
load_dotenv()

# Create the Vertex AI RAG retrieval tool
ask_vertex_retrieval = VertexAiRagRetrieval(
    name='retrieve_rag_documentation',
    description=(
        'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus
        )
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)

# Define the safety settings for the model
safety_settings = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.OFF,
    ),
]

# Specify content generation parameters
generate_content_config = types.GenerateContentConfig(
   safety_settings=safety_settings,
   temperature=0.28,
   max_output_tokens=1000,
   top_p=0.95,
)

# Create the root agent with the defined instructions and tools
root_agent = Agent(
    model=AI_MODEL,
    name='doquinha_root_agent',
    generate_content_config=generate_content_config,  # Optional.
    instruction=my_prompt,
    tools=[
        ask_vertex_retrieval,
    ]
)
