from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_community.document_loaders import PyPDFLoader

import yaml
from dotenv import load_dotenv

load_dotenv()

class SummarizerHandler():
    def __init__(self, document: str) -> None:
        self.model = ChatGoogleGenerativeAI(model = "gemini-pro")
    
        with open("./prompts/gemini-pro.yml", 'r') as readfile:
            prompts = yaml.safe_load(readfile)
            self.map_prompt: str = prompts["map-document-summarize-prompt"]
            self.reduce_prompt: str = prompts["reduce-document-summarize-prompt"]
          
        loader = PyPDFLoader(document)
        self.docs = loader.load()

    def summarizer(self):

        map_prompt = PromptTemplate.from_template(self.map_prompt)
        reduce_prompt = PromptTemplate.from_template(self.reduce_prompt)

        map_chain = LLMChain(llm = self.model, prompt = map_prompt)
        reduce_chain = LLMChain(llm=self.model, prompt=reduce_prompt)
        
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="docs"
        )

        reduce_documents_chain = ReduceDocumentsChain(
            combine_documents_chain=combine_documents_chain,
            collapse_documents_chain=combine_documents_chain,
            token_max=4000,
        )

        map_reduce_chain = MapReduceDocumentsChain(
            llm_chain=map_chain,
            reduce_documents_chain=reduce_documents_chain,
            document_variable_name="docs",
            return_intermediate_steps=False,
        )

        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=0
        )
        split_docs = text_splitter.split_documents(self.docs)
        response = map_reduce_chain.invoke(split_docs)
        
        return response['output_text']

    
# if __name__== "__main__":

#     document = "../documents/Chicken_Keypoint_Estimation.pdf"
#     summarizer = SummarizerHandler(document = document)
#     summarizer.summarizer()