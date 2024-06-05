# fastapi dev yt-history-api.py

from fastapi import FastAPI

from sentence_transformers import SentenceTransformer
from FlagEmbedding import FlagReranker

import pandas as pd
import chromadb

app = FastAPI()

@app.get("/")
async def search(q: str='LLM with RAG', limit: int=15):

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cuda')
    number_of_results = limit
    chroma_client = chromadb.PersistentClient(path="chroma")
    collection = chroma_client.get_or_create_collection(name='yt-history')
    query = q
    print('Encoding query...')
    qembeddings = [model.encode(query).astype('float').tolist()]
    print('Getting results...')
    results = collection.query(
        query_embeddings=qembeddings, 
        n_results=number_of_results*10 # 10x more results in order to re-rank them
    )
    res_dicts = results['metadatas'][0]
    df = pd.DataFrame(res_dicts).drop_duplicates(subset='video_id')
    df.drop('datetime', axis=1, inplace=True)

    reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True, device='cuda')
    pairs = [[query, doc] for doc in results['documents'][0]]
    print('Re-ranking results...')
    scores = reranker.compute_score(pairs, normalize=False)
    sorted_results = sorted(
        zip(
            results['ids'][0], 
            scores
            ), 
            key=lambda x: x[1], reverse=True
        )
    sorted_ids = [row[0] for row in sorted_results]
    res_ids = results['ids'][0] # chromadb results ids
    doc_list = results['documents'][0] # chromadb results documents
    res_meta_dicts = results['metadatas'][0] # chromadb results metadatas
    df_meta = pd.DataFrame(res_meta_dicts) # create dataframe from metadatas
    df_meta.drop('datetime', axis=1, inplace=True) # drop datetime
    df_meta.insert(len(df_meta.columns), 'paragraph', doc_list)
    df_meta.insert(0, 'id', res_ids) # add ids as first column in the dataframe
    df_meta.set_index('id', inplace=True) # create index from ids
    df_meta = df_meta.reindex(sorted_ids) # reindex dataframe with the sorted ids
    df_meta = df_meta.drop_duplicates(subset='video_id') # drop duplicate videos
    df_meta.reset_index(drop=True, inplace=True)
    df_meta = df_meta.head(number_of_results) # keep only the first 15 videos

    print(df_meta)
    return df_meta[['title', 'titleUrl', 'paragraph']].to_dict('records')

