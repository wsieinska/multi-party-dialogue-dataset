import re
import json
from difflib import SequenceMatcher
import statistics

MODEL = "gpt-3.5-turbo"
#MODEL = "gpt-4-turbo"
#MODEL = "gpt-4o"
#MODEL = "llama-2-13b-chat-hf-16k"
#MODEL = "vicuna-13b-v1.5-16k"

all_s1_scores = []
all_s2_scores = []


def compute_subtask_2_statistics(dialogue_number, results_dict):
    scores = [result["score"] for result in results_dict]
    all_s2_scores.extend(scores)
    mean = statistics.mean(scores)
    sd = statistics.stdev(scores)
    stats = {"dialogue_number":dialogue_number, "number_of_turns":len(scores), "scores":scores, "mean":mean, "sd":sd}
    return stats


def evaluate_subtask_2(dialogue, prediction):
    # Create a list of gold annotations
    g_anns = []
    pattern = re.compile('@.*\$')
    for turn in dialogue:
        g_ann = pattern.search(turn).group()
        g_ann = g_ann.lstrip("@").rstrip("$")
        g_anns.append(g_ann)

    # Create a list of predicted annotations
    p_anns = []
    pattern = re.compile('@.*\$')
    for turn in prediction:
        p_ann = pattern.search(turn).group()
        # Warning! If @ and $ are missing from prediction,
        # they need to be added manually
        # before running the evaluation script!
        p_ann = p_ann.lstrip("@").rstrip("$")
        p_anns.append(p_ann)

    if len(g_anns) != len(p_anns):
        print(f"Warning! Lists have different lengths! gold: {len(g_anns)}, pred: {len(p_anns)}")

    # Compute similarity scores
    results = []
    for i in range(len(g_anns)):
        score = SequenceMatcher(None, g_anns[i], p_anns[i]).ratio()
        result = {"turn": i+1, "gold":g_anns[i], "pred":p_anns[i], "score":score}
        results.append(result)
    return results


def evaluate_subtask_1(dialogue, prediction):
    # Compute similarity score
    dialogue_str = "".join(dialogue)
    prediction_str = "".join(prediction)
    score = SequenceMatcher(None, dialogue_str, prediction_str).ratio()
    return score


def process(dialogue_number):
    # Read dialogues with gold annotations
    dialogue_path = f"dialogues-preprocessed/dialogue_{dialogue_number}.txt"
    dialogue_file = open(dialogue_path, "r")
    dialogue = dialogue_file.readlines()

    # Read dialogues with predicted annotations (unaltered)
    prediction_path = f"predictions/{MODEL}/prediction_{dialogue_number}.txt"
    prediction_file = open(prediction_path, "r")
    prediction_unaltered = prediction_file.readlines()

    # Read dialogues with predicted annotations (altered to enable automatic extraction of annotations)
    prediction_path = f"predictions-altered-for-evaluation/{MODEL}/prediction_{dialogue_number}.txt"
    prediction_file = open(prediction_path, "r")
    prediction_altered = prediction_file.readlines()

    # Evaluate subtask 1
    s1_score = evaluate_subtask_1(dialogue, prediction_unaltered)

    # Evaluate subtask 2
    s2_results_dict = evaluate_subtask_2(dialogue, prediction_altered)

    # Write subtask 2 evaluation results
    results_path = f"evaluation-results/{MODEL}/result_{dialogue_number}.json"
    with open(results_path, "w") as results_file:
        json.dump(s2_results_dict, results_file, indent = 4)

    return s1_score, s2_results_dict


def main():
    # Print model
    print(f"Model: {MODEL}")

    full_s2_stats = []

    # Process each dialogue
    for dialogue_number in range(1, 36):
        if dialogue_number < 10:
            dialogue_number = "0" + str(dialogue_number)

        print(f"Evaluating... [{dialogue_number}/35]")

        try:
            s1_score, s2_results_dict = process(dialogue_number)
        except FileNotFoundError:
            print(f"No prediction found with number {dialogue_number}. Skipping.")
            continue

        all_s1_scores.append(s1_score)

        # Compute statistics for subtask 2
        stats = compute_subtask_2_statistics(dialogue_number, s2_results_dict)
        full_s2_stats.append(stats)

    # Aggregate statistics for 35 dialogues
    aggregated_s1_mean = statistics.mean(all_s1_scores)
    aggregated_s1_sd = statistics.stdev(all_s1_scores)
    aggregated_s2_mean = statistics.mean(all_s2_scores)
    aggregated_s2_sd = statistics.stdev(all_s2_scores)
    full_stats_with_summary = {
        "model": MODEL,
        "subtask_1_mean": aggregated_s1_mean,
        "subtask_1_sd": aggregated_s1_sd,
        "subtask_2_mean" :aggregated_s2_mean,
        "subtask_2_sd": aggregated_s2_sd,
        "subtask_2_details": full_s2_stats
    }

    # Write full statistics for this model
    full_stats_path = f"evaluation-results/{MODEL}/statistics.json"
    with open(full_stats_path, "w") as full_stats_file:
        json.dump(full_stats_with_summary, full_stats_file, indent = 4)


if __name__ == "__main__":
    main()


#EOF
