from src.rag.llm import LLM
def test():
        llm = LLM()

        user_prompt = "What is a 10-K filing?" 
        system_prompt = "You are a helpful financial analyst."

        response1 =llm.generate(system_prompt, user_prompt)
        response2 = llm.generate(system_prompt, user_prompt, 0.7)
        response3 = llm.generate(system_prompt, user_prompt, 0.0)

        print(f" default temp :  {response1}")
        print(f" temp 0.7 :  {response2}")
        print(f" temp 0.0:  {response3}")



if __name__ == "__main__":
                test()