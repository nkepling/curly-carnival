from langchain.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os



if os.path.exists(".env"):
    load_dotenv()
else:
    print("No .env file found")

model_path = os.environ.get("PATH_TO_LLAMA_Chat_7b")

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path = model_path,
    temperature = 0.0,
    top_p = 1,
    n_ctx = 6000,
    callback_manager = callback_manager,
    verbose=False
)

while True:
    user_input = input("You (or type exit): ")
    if user_input=='exit':
        break

    answer = llm(user_input)
    print("\n")






# if __name__ == "__main__":
#     # if os.path.exists(".env"):
#     #     load_dotenv()
#     # else:
#     #     print("No .env file found")

#     # my_variable_value = os.environ.get("PATH_TO_QUANTIZED_LAMMA")
#     # print(my_variable_value)
#     pass