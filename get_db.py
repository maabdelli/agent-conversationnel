import os

from langchain.vectorstores.chroma import Chroma
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter


from langchain.document_loaders import DirectoryLoader, TextLoader
from PyPDF2 import PdfReader
from langchain.document_loaders import DirectoryLoader

from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader 

loader = PyPDFLoader("./example_data/RP_EIE.pdf")
document = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
texts = text_splitter.split_documents(document)

embeddings = OpenAIEmbeddings(
    openai_api_key='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'


)
'''
db = Chroma(
    persist_directory='./db',
    embedding_function=embeddings
)
'''

#db.add_documents(documents=texts)


persist_directory = './db4'

vectordb = FAISS.from_documents(
    documents=texts,
    embedding=embeddings,
    persist_directory=persist_directory
)
vectordb.persist()