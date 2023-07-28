import gradio as gr
from fastapi import FastAPI
from conversation import create_conversation
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from os import listdir
import lancedb
from langchain.vectorstores import LanceDB

app=FastAPI()



qa = create_conversation(persist_directory = '../lancedb')



@app.get("/")
def root():
    db = lancedb.connect('../lancedb')
    tbl = db.open_table("my_table")

    return {tbl.to_pandas().loc[700,'text']}





def add_text(history, text):
    history = history + [(text, None)]
    return history, ""


def bot(history):
    res = qa(
        {
            'question': history[-1][0],
            'chat_history': history[:-1]
        }
    )
    history[-1][1] = res['answer']
    return history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot([], elem_id="chatbot",
                         label='Document GPT')
    with gr.Row():
        with gr.Column(scale=0.80):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter",
                #style={"container":False}
            )
        with gr.Column(scale=0.10):
            submit_btn = gr.Button(
                'Submit',
                variant='primary'
            )
        with gr.Column(scale=0.10):
            clear_btn = gr.Button(
                'Clear',
                variant='stop'
            )

    txt.submit(add_text, [chatbot, txt], [chatbot, txt]).then(
        bot, chatbot, chatbot
    )

    submit_btn.click(add_text, [chatbot, txt], [chatbot, txt]).then(
        bot, chatbot, chatbot
    )

    clear_btn.click(lambda: None, None, chatbot, queue=False)



app = gr.mount_gradio_app(app, demo, path="/chatbot")

'''
if __name__ == '__main__':
    demo.queue(concurrency_count=3)
    demo.launch()
'''
