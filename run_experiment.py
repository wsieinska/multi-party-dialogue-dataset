#import openai  # for local models
from openai import OpenAI  # for OpenAI models

#---------------------------------------------------
# OpenAI API models

client = OpenAI(api_key="blah")

MODEL = "gpt-3.5-turbo"
#MODEL = "gpt-4-turbo"
#MODEL = "gpt-4o"

#---------------------------------------------------
# Local models on a local server (you must have them installed)

#openai.api_key = "EMPTY"
#openai.api_base = "http://localhost:8000/v1"

#MODEL = "llama-2-13b-chat-hf-16k"
#MODEL = "vicuna-13b-v1.5-16k"

#---------------------------------------------------
# Dialogues used as training examples

EXAMPLES = ["01", "11", "21"]


def predict(prompt):
    #prediction = openai.ChatCompletion.create(  # for local models
    prediction = client.chat.completions.create(  # for OpenAI models
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return prediction.choices[0].message.content


def process(prompt, dialogue_number):
    # Read dialogues
    dialogue_path = f"dialogues-with-blanks/dialogue_{dialogue_number}.txt"
    dialogue_file = open(dialogue_path, "r")
    dialogue = dialogue_file.read().rstrip()

    # Predict
    prompt = prompt.replace("{dialogue_with_blanks}", dialogue)
    prediction = predict(prompt)

    # Write predictions
    prediction_path = f"predictions/{MODEL}/prediction_{dialogue_number}.txt"
    prediction_file = open(prediction_path, "w")
    prediction_file.writelines(prediction)
    prediction_file.close()


def main():
    # Print server, model, and numbers of dialogues used for training
    #print(f"Server: {openai.api_base}")  # for local models
    print(f"Model: {MODEL}")
    print(f"Dialogues used for training: {EXAMPLES}")
    print("Processing...")

    # Read prompt
    prompt_file = open("prompt.txt", "r")
    prompt = prompt_file.read().rstrip()

    # Read examples
    examples = []
    for example_number in EXAMPLES:
        example_path = f"dialogues-preprocessed/dialogue_{example_number}.txt"
        example_file = open(example_path, "r")
        example = example_file.read().rstrip()
        examples.append(example)

    # Write examples into prompt
    prompt = prompt.replace("{example_dialogue_1}", examples[0])
    prompt = prompt.replace("{example_dialogue_2}", examples[1])
    prompt = prompt.replace("{example_dialogue_3}", examples[2])

    # Process each dialogue
    for dialogue_number in range(1, 36):
        if dialogue_number < 10:
            dialogue_number = "0" + str(dialogue_number)
        dialogue_number = str(dialogue_number)
        if dialogue_number in EXAMPLES:
            print(f"{dialogue_number}/35 (Dialogue in training examples, skipping to the next one.)")
            continue
        else:
            print(f"{dialogue_number}/35")
        process(prompt, dialogue_number)
    print("Done.")


if __name__ == "__main__":
    main()


#EOF
