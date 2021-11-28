# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import argparse
from batch_eval_KB_completion import main as run_evaluation
from batch_eval_KB_completion import load_file
from lama.modules import build_model_by_name
import pprint
import statistics
from os import listdir
import os
from os.path import isfile, join
from shutil import copyfile
from collections import defaultdict

LMs = [
    # {
    #     "lm": "albert",
    #     "label": "indobert_lite_base",
    #     "models_names": ["bert"],
    #     "bert_model_name": "indobenchmark/indobert-lite-base-p2",
    #     "bert_model_dir": None,
    # },
    {
        "lm": "distilbert",
        "label": "distilbert_base",
        "models_names": ["distilbert"],
        "distilbert_model_name": "cahya/distilbert-base-indonesian",
        "distilbert_model_dir": None,
        "distilbert_vocab_name": "cahya/distilbert-base-indonesian"
    },
    {
        "lm": "bert",
        "label": "indobert_base",
        "models_names": ["bert"],
        "bert_model_name": "indolem/indobert-base-uncased",
        "bert_model_dir": None,
    },
]


def run_experiments(
    relations,
    data_path_pre,
    data_path_post,
    input_param={
        "lm": "bert",
        "label": "indobert_base",
        "models_names": ["bert"],
        "bert_model_name": "indolem/indobert-base-uncased",
    },
    use_negated_probes=False,
):
    model = None
    pp = pprint.PrettyPrinter(width=41, compact=True)

    all_Precision1 = []
    type_Precision1 = defaultdict(list)
    type_count = defaultdict(list)

    results_file = open("last_results.csv", "w+")

    for relation in relations:
        pp.pprint(relation)
        PARAMETERS = {
            "dataset_filename": "{}{}{}".format(
                data_path_pre, relation["relation"], data_path_post
            ),
            "common_vocab_filename": "common_vocab.txt",
            "template": "",
            "bert_vocab_name": "vocab.txt",
            "batch_size": 32,
            "logdir": "output",
            "full_logdir": "output/results/{}/{}".format(
                input_param["label"], relation["relation"]
            ),
            "lowercase": True,
            "max_sentence_length": 100,
            "threads": -1,
            "interactive": False,
            "use_negated_probes": use_negated_probes,
        }

        if "template" in relation:
            PARAMETERS["template"] = relation["template"]
            if use_negated_probes:
                PARAMETERS["template_negated"] = relation["template_negated"]

        PARAMETERS.update(input_param)
        print(PARAMETERS)

        args = argparse.Namespace(**PARAMETERS)

        # see if file exists
        try:
            data = load_file(args.dataset_filename)
        except Exception as e:
            print("Relation {} excluded.".format(relation["relation"]))
            print("Exception: {}".format(e))
            continue

        if model is None:
            [model_type_name] = args.models_names
            model = build_model_by_name(model_type_name, args)

        Precision1 = run_evaluation(args, shuffle_data=False, model=model)
        print("P@1 : {}".format(Precision1), flush=True)
        all_Precision1.append(Precision1)

        results_file.write(
            "{},{}\n".format(relation["relation"], round(Precision1 * 100, 2))
        )
        results_file.flush()

        if "type" in relation:
            type_Precision1[relation["type"]].append(Precision1)
            data = load_file(PARAMETERS["dataset_filename"])
            type_count[relation["type"]].append(len(data))

    mean_p1 = statistics.mean(all_Precision1)
    print("@@@ {} - mean P@1: {}".format(input_param["label"], mean_p1))
    results_file.close()

    for t, l in type_Precision1.items():

        print(
            "@@@ ",
            input_param["label"],
            t,
            statistics.mean(l),
            sum(type_count[t]),
            len(type_count[t]),
            flush=True,
        )

    return mean_p1, all_Precision1


def get_IndoWiki_parameters(data_path_pre="data/"):
    relations = load_file("{}relations.jsonl".format(data_path_pre))
    data_path_pre += "IndoWiki/"
    data_path_post = ".jsonl"
    return relations, data_path_pre, data_path_post


def run_all_LMs(parameters):
    for ip in LMs:
        print(ip["label"])
        run_experiments(*parameters, input_param=ip, use_negated_probes=False)


if __name__ == "__main__":
    parameters = get_IndoWiki_parameters()
    run_all_LMs(parameters)

