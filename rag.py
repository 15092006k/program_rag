import ollama
import re

# -----------------------------------
# 1. LOAD COLLEGE INFORMATION
# -----------------------------------

with open("college.txt", "r", encoding="utf-8") as file:
    text = file.read()

print("College information loaded successfully!")


# -----------------------------------
# 2. SPLIT TEXT INTO CHUNKS
# -----------------------------------

chunks = re.split(r"\n\s*\n", text)

chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

print("Number of chunks:", len(chunks))


# -----------------------------------
# 3. SIMPLE RETRIEVAL FUNCTION
# -----------------------------------

def retrieve(question):
    question_words = set(
        word.lower()
        for word in re.findall(r"\b\w+\b", question)
        if len(word) > 2
    )

    scores = []

    for chunk in chunks:
        chunk_words = set(
            word.lower()
            for word in re.findall(r"\b\w+\b", chunk)
        )

        score = len(question_words.intersection(chunk_words))

        scores.append((score, chunk))

    scores.sort(reverse=True, key=lambda x: x[0])

    # Get the best 3 chunks
    best_chunks = [chunk for score, chunk in scores[:3]]

    return "\n\n".join(best_chunks)


# -----------------------------------
# 4. ASK QUESTION
# -----------------------------------

while True:

    question = input("\nAsk a question about the college (type 'exit' to stop): ")

    if question.lower() == "exit":
        print("Thank you!")
        break

    # -----------------------------------
    # 5. RETRIEVE RELEVANT INFORMATION
    # -----------------------------------

    context = retrieve(question)

    print("\nRelevant information found...")


    # -----------------------------------
    # 6. CREATE PROMPT
    # -----------------------------------

    prompt = f"""
You are a college information assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer is not available in the context,
say: "I could not find this information in the college document."

Context:
{context}

Question:
{question}

Give a simple and clear answer.
"""


    # -----------------------------------
    # 7. SEND TO OLLAMA
    # -----------------------------------

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    # -----------------------------------
    # 8. DISPLAY ANSWER
    # -----------------------------------

    print("\nAI Answer:")
    print(response["message"]["content"])