from langchain_core.tools import tool
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.runnables import chain
from pydantic import BaseModel, Field

from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

###################################################
# wikipedia search tool
###################################################
@chain
def wikipedia_search(input_dict: dict) -> dict:
    """사용자 query에 대한 정보를 위키백과사전에서 k개 문서를 검색하는 Runnable."""

    query = input_dict['query'] #검색어
    max_results = input_dict.get("max_results", 2) # 조회문서 최대 개수. default: 2

    wiki_loader = WikipediaLoader(query=query, load_max_docs=max_results, lang="ko")
    search_result = wiki_loader.load() # list[Document]
    if search_result: #검색결과가 있다면  # Document -> dictionary
        result_list = []
        for doc in search_result:
            result_list.append({"content":doc.page_content, 
                                "url":doc.metadata['source'], 
                                "title":doc.metadata['title']})
        return {"result": result_list}
    else:
        return {"result":"검색 결과가 없습니다."}
    

class SearchWikiArgsSchema(BaseModel):
    query: str = Field(..., description='위키백과사전에서 검색할 키워드, 검색어')
    max_results: int = Field(default=2, description="검색할 문서의 최대개수")

search_wiki = wikipedia_search.as_tool(
    name="search_wiki", # 툴 이름.
    description=("위키 백과사전에서 정보를 검색할 때 사용하는 tool.\n"
                 "사용자의 질문과 관련된 위키백과사전의 문서를 지정한 개수만큼 검색해서 반환합니다.\n"
                 "일반적인 지식이나 배경 정보가 필요한 경우 유용하게 사용할 수있는 tool입니다."),
    args_schema=SearchWikiArgsSchema # 파라미터(argument)에대한 설계 -> pydantic 모델 정의
)



###################################################
# menu search tool
###################################################
COLLECTION_NAME = "restaurant_menu"
VECTOR_SIZE = 1536  # OpenAIEmbeddings의 벡터 크기

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

client = QdrantClient(host="localhost", port=6333)

vectorstore = QdrantVectorStore(
    client=client,
    embedding=embeddings,
    collection_name=COLLECTION_NAME
)


retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}  # 검색할 결과 개수
)

## Tool 정의
@tool
def search_menu(query:str) -> dict:
    """
    VectorStore(Vector Database)에 저장된 **Restaurants menu 의 내용을 검색**하는 Tool이다.
    이 도구는 Restaurants menu 관련 쿼리에서 사용합니다.
    
    Args:
        query (str): 메뉴 검색 관련된 query
    Return:
        str: 검색된 메뉴정보를 json string으로 반환한다. 포함항목: content: 메뉴 설명, title: 메뉴이름, url: 메뉴 소스파일경로    
    """
    
    result_docs = retriever.invoke(query)
    result = []
    for doc in result_docs:
        result.append({"content":doc.page_content, "title":doc.metadata["menu_name"], "url":doc.metadata["source"]})

    if not result: # 비었으면
        result = "검색된 정보가 없습니다."
    

    return {"result":result}