from langchain.vectorstores import  Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import nltk
import os
import pinecone
from decouple import config
import textwrap


def takumi_demo():
    CONDENSE_PROMPT = """
        Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:"""

    QA_PROMPT = """
        You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say you don't know. DO NOT try to make up an answer.
        If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
        {context}
        Question: {question}
        Helpful answer in markdown:"""
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