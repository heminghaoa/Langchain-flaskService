from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import VectorDBQA
from langchain.document_loaders import PyPDFLoader
import textwrap
from langchain.prompts import PromptTemplate
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
#流
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.chat_models import ChatOpenAI #导入聊天模型

def LoadPDF_demo():
    # Loading documents
    loader = PyPDFLoader('resource/PDF/law/労働安全衛生法.pdf')
    documents = loader.load()

    # Splitting documents into texts
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=650, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # Specify the directory for persistent storage
    persist_directory = 'VectorDB/ChromaVectorDB/law'
    
    # Creating and persisting the vector database
    embedding = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=persist_directory)
    vectordb.persist()

    # Running the query
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=vectordb)
    query = "残業時間は何時間からが違法ですか。"
    output_answer = qa.run(query)

    # Formatting and printing the answer
    wrapped_text = textwrap.fill(output_answer, width=100)
    print(wrapped_text)

    return wrapped_text

def lawyer_demo2(question):
    template = """Given the following extracted parts of a lengthy legal document and a question, construct a final answer with references ("SOURCES").
        If you don't know the answer, simply state that you do not know. Do not attempt to fabricate an answer.
        Regardless, always include a "SOURCES" section in your answer, you could express it like this: "この回答は、XXXX法(XX年法律第XX号)の第x編-XXXXX,第X章-XXXXX,第XX条-XXXXXを参照しています。"
        Respond in  Japanese.
        QUESTION: {question}
        =========
        {summaries}
        =========   
        FINAL ANSWER IN Japanese:"""
    # QA_PROMPT = """
    #     You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
    #     If you don't know the answer, just say you don't know. DO NOT try to make up an answer.
    #     If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
    #     {context}
    #     Question: {question}
    #     Helpful answer in markdown:"""
    embeddings = OpenAIEmbeddings()
    persist_directory = 'VectorDB/ChromaVectorDB/law'
    docsearch = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    query = question #本质是index查找相关资料，并非提示词
    docs = docsearch.similarity_search(query)
    PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])
    llm = ChatOpenAI(temperature=0,streaming=True, callbacks=[StreamingStdOutCallbackHandler()], verbose=True,model_name="gpt-3.5-turbo-16k")
    chain = load_qa_with_sources_chain(llm, chain_type="stuff",prompt=PROMPT)
    # resp = chat(chat_prompt_with_values.to_messages())
    return  chain({"input_documents": docs, "question": query}, return_only_outputs=True)


