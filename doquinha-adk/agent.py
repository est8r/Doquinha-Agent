import vertexai
from google.adk.agents import Agent
from google.genai import types
from vertexai import agent_engines
from vertexai.preview import rag
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from dotenv import load_dotenv


PROJECT_ID = "gglobo"
REGION = "us-east4"
GSC_BUCKET = "gs://raw_doquinha"


# Initialize the SDK for Vertex AI Agent Engine'
vertexai.init(
    project=PROJECT_ID,
    location=REGION,
    staging_bucket=GSC_BUCKET,
)

AI_MODEL = "gemini-2.5-flash"



rag_corpus = rag.get_corpus(name)


# Define the instructions for the root agent
def return_instructions_root() -> str:
    instruction_prompt_v1 = """
        You are an AI assistant with access to specialized corpus of documents, containing markdown and image files.
        Your role is to provide accurate and concise answers to questions based
        on documents that are retrievable using ask_vertex_retrieval. If you believe
        the user is just chatting and having casual conversation, don't use the retrieval tool.

        But if the user is asking a specific question about a knowledge they expect you to have,
        you can use the retrieval tool to fetch the most relevant information.
        
        If you are not certain about the user intent, make sure to ask clarifying questions
        before answering. Once you have the information you need, you can use the retrieval tool
        If you cannot provide an answer, clearly explain why.

        Do not answer questions that are not related to the corpus.
        When crafting your answer, you may use the retrieval tool to fetch details
        from the corpus. Make sure to cite the source of the information.
        
        Citation Format Instructions:
 
        When you provide an answer, you must also add one or more citations **at the end** of
        your answer. If your answer is derived from only one retrieved chunk,
        include exactly one citation. If your answer uses multiple chunks
        from different files, provide multiple citations. If two or more
        chunks came from the same file, cite that file only once.

        **How to cite:**
        - Use the retrieved chunk's `title` to reconstruct the reference.
        - Include the document title and section if available.
        - For web resources, include the full URL when available.
 
        Format the citations at the end of your answer under a heading like
        "Citations" or "References." For example:
        "Citations:
        1) RAG Guide: Implementation Best Practices
        2) Advanced Retrieval Techniques: Vector Search Methods"

        Do not reveal your internal chain-of-thought or how you used the chunks.
        Simply provide concise and factual answers, and then list the
        relevant citation(s) at the end. If you are not certain or the
        information is not available, clearly state that you do not have
        enough information.
        """
    return instruction_prompt_v1

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
            rag_corpus=rag_corpus.name
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
    instruction=return_instructions_root(),
    tools=[
        ask_vertex_retrieval,
    ]
)

USER_ID = "test_user"

remote_app_sa = agent_engines.get(
    route
)
remote_session = remote_app_sa.create_session(user_id=USER_ID)