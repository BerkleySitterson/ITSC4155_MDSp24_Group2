from llama_cpp import Llama
from pathlib import Path

llm = Llama(model_path=str(Path.home()) + "/LLM_Llama/codellama-7b.Q4_0.gguf",
            chat_format="chatml")

output = llm("Q: Name an artist. A: ",
             max_tokens=32,
             stop=["Q: ", "\n"],
             echo=True)

print(output)
