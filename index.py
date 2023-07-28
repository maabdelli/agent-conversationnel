import os

from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter


from langchain.document_loaders import DirectoryLoader, TextLoader
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader

load_dotenv()

def create_index(file_path: str) -> None:

    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

    with open('output.txt', 'w') as file:
        file.write(text)

    #loader = DirectoryLoader(
       # './',
    #    glob='**/*.txt',
     #   loader_cls=TextLoader
   # )
    loader = DirectoryLoader("./example_data/")



    documents = loader.load()
    print(documents)
    text_splitter = RecursiveCharacterTextSplitter(
        
        chunk_size=1024,
        chunk_overlap=200
    )

    texts = text_splitter.split_documents(documents)
    print('texts                         ',texts)
    embeddings = OpenAIEmbeddings(
        openai_api_key='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'
    )

    persist_directory = 'db'

    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
 
    vectordb.persist()

create_index('Cours.pdf')
