from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough

from backend.utils.logging_utils import setup_logger

logger = setup_logger(__name__)

def get_qa_chain(retriever, model_name: str = "gemini-2.5-flash", temperature: float = 0.0):
    """
    Creates a question-answering chain using the specified retriever and model.
    
    Args:
        retriever: The retriever to use for fetching relevant documents.
        model_name (str): The name of the model to use for generating answers.
        temperature (float): The temperature for the model's responses.
        
    Returns:
        RetrievalQA: The question-answering chain.
    """
    logger.info(f"🔄 Creating QA chain with model: {model_name} (temperature={temperature})")

    llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
    
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
            You are an expert in ML interpretability. Given the following context from academic papers, answer the question.

            Context:
            {context}

            Question:
            {question}

            Answer:""",
    )

    logger.debug(f"📝 Prompt template:\n{prompt.template.strip()}")

    chain = (
        {'context': retriever, 'question': RunnablePassthrough()}
        | prompt
        | llm
    )

    logger.info(f"✅ QA chain created using {llm.__class__.__name__}")
    return chain