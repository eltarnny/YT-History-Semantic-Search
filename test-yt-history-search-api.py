import requests
import json
import gradio as gr

url = 'http://127.0.0.1:8000/'
query = 'RAG vector DB PDF'

def search(query, limit):
    if query == '':
        query = 'RAG vector DB PDF'

    r_list = []
    n_res = 15
    n_elements = 4
    out_list = [gr.HTML(visible=False) for _ in range(n_res*n_elements)]

    params = {
    'q': query,
    'limit': limit
    }
    response = requests.get(url, params=params)
    r_list = json.loads(response.text)

    for i in range(len(r_list)):
        title = r_list[i]['title']
        titleUrl = r_list[i]['titleUrl']
        paragraph = r_list[i]['paragraph']

        w = 420
        h = 300

        v_embed = f'''<iframe width="{w}" height="{h}" 
        src="https://www.youtube.com/embed/{titleUrl.split('=')[-1]}" 
        title="YouTube video player" 
        frameborder="0" allow="accelerometer; autoplay; 
        clipboard-write; encrypted-media; gyroscope; picture-in-picture; 
        web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'''

        v_link = f'<a href="{titleUrl}">{title}</a>'
        paragraph = f'<p><span style="font-weight: bold;">Transcript Excerpt: </span><br>{paragraph}</p>'

        gr_v_link = gr.HTML(v_link, elem_classes='title', visible=True)
        gr_v_embed = gr.HTML(v_embed, visible=True)
        gr_paragraph = gr.HTML(paragraph, elem_classes='paragraph', visible=True)
        line_sep = gr.HTML('<hr>', visible=True)

        for j in range(n_elements):
            out_list[i*n_elements:(i+1)*n_elements] = [gr_v_embed, gr_v_link, gr_paragraph, line_sep]

    return out_list

res_list = []
css = '''
.title {
    font-size: 18px !important;
}
.paragraph {
    font-size: 16px !important;
}
'''
with gr.Blocks(css=css) as demo:
    gr.Markdown("# YouTube History Search")

    with gr.Row():
        qtext = gr.Textbox(placeholder="What are you looking for?", label="Query", scale=3)
        lim = gr.Slider(minimum=1, maximum=15, value=5, step=1, label="Number of results")
        btn = gr.Button("Search")
        btn.click(fn=search, inputs=[qtext, lim], outputs=res_list)
          
    for i in range(15):
        with gr.Row():
            with gr.Column():
                with gr.Row():
                    res_list.append(gr.HTML(visible=False))
                with gr.Row():
                    res_list.append(gr.HTML(elem_classes='title', visible=False))
            with gr.Column():
                with gr.Row():
                    res_list.append(gr.HTML(elem_classes='paragraph', visible=False))
        with gr.Row():
            res_list.append(gr.HTML('<hr>', visible=False))



    qtext.submit(fn=search, inputs=[qtext, lim], outputs=res_list)

demo.launch()