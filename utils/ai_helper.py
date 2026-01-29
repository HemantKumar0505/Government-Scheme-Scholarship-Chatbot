# from transformers import pipeline

# text_generator = pipeline(
#     "text2text-generation",
#     model="google/flan-t5-base"
# )

# def generate_ai_response(prompt):
#     """
#     Generates a controlled, non-repetitive AI response.
#     """
#     result = text_generator(
#         prompt,
#         max_new_tokens=120,
#         do_sample=False,
#         repetition_penalty=1.2
#     )
#     return result[0]["generated_text"].strip()



from transformers import pipeline

text_generator = pipeline(
    "text-generation",  
    model="google/flan-t5-small"  
)

def generate_ai_response(prompt):
    result = text_generator(
        prompt,
        max_new_tokens=120,
        do_sample=False
    )
    return result[0]["generated_text"].strip()
