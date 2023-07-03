from langchain.vectorstores import  Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
import nltk
import os
import pinecone
from decouple import config
import textwrap
from langchain.prompts import PromptTemplate
#流
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.chat_models import ChatOpenAI #导入聊天模型

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import VectorDBQA


def takumi_demo():
    # os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')
    embeddings = OpenAIEmbeddings(openai_api_key= config('OPENAI_API_KEY'))

    # 初始化 pinecone
    pinecone.init(
    api_key= config('PINECONE_API_KEY'),
    environment="us-west4-gcp-free"
    )
    index_name="chattest"
    # 持久化数据
    #docsearch = Pinecone.from_documents(split_docs, embeddings, index_name=index_name)

    # 加载数据
    docsearch = Pinecone.from_existing_index(index_name,embeddings)

    query = "貫通部の防火区画の処理方法は？" #本质是index查找相关资料，并非提示词
    docs = docsearch.similarity_search(query)

    llm = OpenAI(model_name="gpt-3.5-turbo",temperature=0)#llm = OpenAI(model_name="text-davinci-003",max_tokens=1024) 选择OpenAI模型，调参数
    chain = load_qa_chain(llm, chain_type="stuff", verbose=True)
    output_answer = chain.run(input_documents=docs, question=query)
    wrapped_text = textwrap.fill(output_answer, width=100)
    print(wrapped_text)
    return wrapped_text


def takumi_demo2():
    template = """Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
        If you don't know the answer, just say that you don't know. Don't try to make up an answer.
        ALWAYS return a "SOURCES" part in your answer.
        Respond in  CHINESE.
        QUESTION: {question}
        =========
        {summaries}
        =========
        FINAL ANSWER IN CHINESE:"""
    # QA_PROMPT = """
    #     You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
    #     If you don't know the answer, just say you don't know. DO NOT try to make up an answer.
    #     If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
    #     {context}
    #     Question: {question}
    #     Helpful answer in markdown:"""
    embeddings = OpenAIEmbeddings()

    # 初始化 pinecone
    pinecone.init(
    api_key= config('PINECONE_API_KEY'),
    environment="us-west4-gcp-free"
    )
    index_name="chattest"
    # 加载数据
    docsearch = Pinecone.from_existing_index(index_name,embeddings)

    query = "貫通部の防火区画の処理方法は？" #本质是index查找相关资料，并非提示词
    docs = docsearch.similarity_search(query)
    PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])
    llm = ChatOpenAI(temperature=0,streaming=True, callbacks=[StreamingStdOutCallbackHandler()], verbose=True,model_name="gpt-3.5-turbo-16k")
    chain = load_qa_with_sources_chain(llm, chain_type="stuff",prompt=PROMPT)
    # resp = chat(chat_prompt_with_values.to_messages())
    return  chain({"input_documents": docs, "question": query}, return_only_outputs=True)


def LoadPDF_demo(pdf_path):
    # Splitting documents into texts
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=650, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # Specify the directory for persistent storage
    persist_directory = 'VectorDB/ChromaVectorDB/takumi'
    
      # Loading documents
    loader = PyPDFLoader(pdf_path,persist_directory)
    documents = loader.load()

    # Creating and persisting the vector database
    embedding = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=persist_directory)
    vectordb.persist()

    # Running the query
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=vectordb)
    query = "給水配管には吸排気弁必要ですか。"
    output_answer = qa.run(query)

    # Formatting and printing the answer
    wrapped_text = textwrap.fill(output_answer, width=100)
    print(wrapped_text)

    return wrapped_text
    
    
def takumi_demo3(question):
        template = """Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
        If you don't know the answer, just say that you don't know. Don't try to make up an answer.
        ALWAYS return a "SOURCES" part in your answer.
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
        persist_directory = 'VectorDB/ChromaVectorDB/takumi'
        docsearch = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

        query = question #本质是index查找相关资料，并非提示词
        docs = docsearch.similarity_search(query)
        PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])
        llm = ChatOpenAI(temperature=0,streaming=True, callbacks=[StreamingStdOutCallbackHandler()], verbose=True,model_name="gpt-3.5-turbo-16k")
        chain = load_qa_with_sources_chain(llm, chain_type="stuff",prompt=PROMPT)
        # resp = chat(chat_prompt_with_values.to_messages())
        return  chain({"input_documents": docs, "question": query}, return_only_outputs=True)
