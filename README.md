### YouTube History Semantic Search

You will need first to download your YouTube History using [Google Takeout](https://takeout.google.com/)  

get-history-data.ipynb  
Pre-process the history data, gets video transcripts, saves to disk.  

create-embeddings.ipynb  
Further data processing, calculating embeddings, save locally to ChromaDB.  

query-chroma.ipynb  
Code to query the database and get relevant results with reranking.  

yt-history-api.py  
Creates an API for searching the database.  
The search part of the code is basically the same as in query-chroma.ipynb, but this is a purely Python file.  
Run with:  
fastapi dev yt-history-api.py  

test-yt-history-search-api.ipynb  
test-yt-history-search-api.py  
Same code in both files.  
This is a Gradio UI for calling the API and display the results.  
Run after starting the API.  

For more information, here is the Medium article.  
https://medium.com/@eltarny/youtube-history-semantic-search-6cd9f20922a8
