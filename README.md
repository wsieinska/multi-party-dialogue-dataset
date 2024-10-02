# A Multi-party Dialogue Dataset

This repository contains a multi-party dialogue dataset designed for the task of dialogue goal tracking in a hospital setting. Our dialogues can be found in the `dialogues/` directory. A detailed description of our dataset can be found in our [paper](https://www.semdial.org/anthology/papers/Z/Z24/Z24-4016/).

Example dialogue:

|Turn|Speaker -> Addressee|Utterance|Goal Annotation|
|:----|:----|:----|:----|
|01 |ARI->Pat+Com |Hello, my name is ARI. How can I help you? |`@-$`|
|02 |Com->Pat |I'm hungry. |`@G(Com, eat())$`|
|03 |Pat->ARI |We're hungry. |`@G(Pat+Com, eat())$`|
|04 |Com->ARI |We'd like to eat. |`@G(Pat+Com, eat())$`|
|05 |ARI->Pat+Com |It's the most important question of the day. Are you hungry yet? You can ask my colleague in the room who is responsible for the meals. |`@AGP(Pat+Com, eat())$`|
|06 |Pat->ARI |Ok, thank you. |`@CGP(Pat+Com, eat())$`|
|07 |ARI->Pat |You're welcome. |`@-$`|
|08 |ARI->Pat+Com |Is there anything else I can help you with? |`@-$`|
|09 |Com->ARI |I'd like to go to the toilet before the consultation. |`@G(Com, go-to(toilet))$`|
|10 |ARI->Com |Very easy! You have to go to the corridor at the end of the room. It's the second door on the right. |`@AGP(Com, go-to(toilet))$`|
|11 |Com->ARI |Thank you. |`@CGP(Com, go-to(toilet))$`|
|12 |ARI->Com |You're welcome. |`@-$`|
|13 |ARI->Pat+Com |Thank you, have a nice day. |`@-$`|

## Paper title:

_A Multi-party Dialogue Dataset for Dialogue Goal Tracking in a Hospital Setting and How It Can Be Used in LLM Prompt Engineering Experiments_

## Paper link:

https://www.semdial.org/anthology/papers/Z/Z24/Z24-4016/

## Cite as:

```
@inproceedings{sieinska-etal-2024-multi,
    title = "A Multi-party Dialogue Dataset for Dialogue Goal Tracking in a Hospital Setting and How It Can Be Used in LLM Prompt Engineering Experiments",
    author = "Siei{\'n}ska, Weronika and Addlesee, Angus and Hern{\'a}ndez Garc{\'i}a, Daniel and Gunson, Nancie and Romeo, Marta and Dondrup, Christian and Lemon, Oliver",
    booktitle = "Proceedings of the 28th Workshop on the Semantics and Pragmatics of Dialogue - Poster Abstracts",
    month = sep,
    year = "2024",
    address = "Trento, Italy",
    publisher = "SEMDIAL",
    url = "http://semdial.org/anthology/Z24-Sieinska_semdial_0016.pdf",
}
```

## Abstract:

We describe a multi-party dialogue dataset, which we collected, annotated, and released on GitHub for public use. The dataset is specifically designed for the task of dialogue goal tracking. It consists of transcriptions of 35 conversational interactions between 2 human speakers and a humanoid social robot called ARI in a hospital setting. The robot is there to alleviate the workload of medical staff by providing patients with information related to the hospital. In the dataset, each utterance that states a goal of a human speaker, e.g., to go to the reception or to find out where they can get a cup of coffee, is explicitly annotated with that goal. In this paper, we also describe a computational experiment we conducted with the use of the dataset to illustrate how it can be used. We prompt engineered 5 large language models for the task or dialogue goal tracking. While some of the models performed very poorly, others were able to grasp the task quite well and predicted most goal annotations correctly.

## Our LLM prompt engineering experiment:

We prompt engineered 5 LLMs to perform goal tracking in multi-party conversations, namely:
- GPT-4o,
- GPT-4 Turbo,
- GPT-3.5 Turbo,
- Vicuna-13b-v1.5-16k, and
- Llama-2-13b-chat-hf-16k.

We used the `run_experiment.py` script for the experiment. The prompt we used can be found in the `prompt.txt` file. We took the few-shot learning approach and added 3 training examples to the prompt (dialogues 1, 11, and 21) leaving 32 dialogues for testing (3 was the highest possible number due to memory limitations).

For each dialogue file (from the `dialogues/` directory), we created a copy and replaced goal annotations with blanks (see the `dialogues-with-blanks/` directory) with the use of the `replace_goals_with_blanks.sh` script.

The task for the LLMs was to return these dialogues with blanks filled in with their predictions of goal annotations. It can be divided into two subtasks:
1. return the same text of the given test dialogue,
2. replace blanks with predictions of goal annotations.

Predictions returned by the models can be found in the `predictions/` directory.

We evaluated performance at subtask 1 by computing similarity scores between generated dialogues and dialogues from our dataset. We used `python3 difflib.SequenceMatcher` as our metric. Then, to evaluate performance at subtask 2, we extracted predicted goal annotations and compared them to gold annotations from our dataset with the use of the same metric. We used the `evaluate_predictions.py` script for evaluation. Results can be found in the `evaluation-results/` directory.

However, due to the fact that the LLMs did not perform very well at (it would seem straightforward) subtask 1 (especially Llama-2-13b-chat-hf-16k), some generated dialogues needed to be slightly altered to enable automatic extraction of predicted goal annotations. These prediction files can be found in the `predictions-altered-manually-for-evaluation/` directory.
