import os

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import lancedb
from langchain.vectorstores import LanceDB

def create_conversation(persist_directory) -> ConversationalRetrievalChain:   
    

    embeddings = OpenAIEmbeddings(
        openai_api_key='s'
    )

    db = lancedb.connect(persist_directory)
    tbl = db.open_table("my_table")
    vectorstore = LanceDB(tbl, embeddings)
    
    '''db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )'''

    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=False
    )

    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(openai_api_key='sk-'),
        chain_type='stuff',
        retriever=vectorstore.as_retriever(),
        memory=memory,
        get_chat_history=lambda h: h,
        verbose=True
    )

    return qa
