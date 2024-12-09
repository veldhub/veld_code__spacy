import json
import logging
import os
import random

import spacy
from spacy.cli import download
from spacy.tokens import Span, DocBin


IN_JSON_FILE = os.getenv("in_json_file")
if IN_JSON_FILE is None:
    raise Exception("parameter 'in_json_file' is missing")
IN_JSON_FILE = "/veld/input/" + IN_JSON_FILE
OUT_SPACY_DOCBIN_FOLDER = "/veld/output/docbin/"
OUT_LOG_FILE = os.getenv("out_log_file")
if OUT_LOG_FILE is None:
    raise Exception("parameter 'out_log_file' is missing")
OUT_LOG_FILE = "/veld/output/log/" + OUT_LOG_FILE
MODEL_TO_DOWNLOAD = os.getenv("model_to_download")
if MODEL_TO_DOWNLOAD is None:
    raise Exception("parameter 'model_to_download' is missing")
PERCENTAGE_TRAIN = os.getenv("percentage_train")
PERCENTAGE_DEV = os.getenv("percentage_dev")
PERCENTAGE_EVAL = os.getenv("percentage_eval")
SEED = os.getenv("seed")


if os.path.exists(OUT_LOG_FILE):
    os.remove(OUT_LOG_FILE)
logging.basicConfig(
    filename=OUT_LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def print_and_log(msg):
    print(msg)
    logging.info(msg)


def parse_env_vars():
    print_and_log("####################### reading args")
    perc_train = int(PERCENTAGE_TRAIN)
    perc_dev = int(PERCENTAGE_DEV)
    perc_eval = int(PERCENTAGE_EVAL)
    seed = int(SEED)
    print_and_log(f"perc_train: {perc_train}, perc_dev: {perc_dev}, perc_eval: {perc_eval}, seed: {seed}")
    if perc_train + perc_dev + perc_eval != 100:
        print_and_log("Percentages do not sum up to 100. Is that on purpose?")
    return perc_train, perc_dev, perc_eval, seed
    
    
def read_gold_data(perc_train, perc_dev, perc_eval, seed):
    random.seed(seed)
    with open(IN_JSON_FILE, "r") as f:
        gd_list = json.load(f)
    random.shuffle(gd_list)
    len_total = len(gd_list)
    cutoff_train = int(len_total / 100 * perc_train)
    cutoff_dev = int(len_total / 100 * (perc_train + perc_dev))
    perc_total = perc_train + perc_dev + perc_eval
    if perc_total == 100:
        cutoff_eval = len_total
    elif perc_total < 100:
        cutoff_eval = int(len_total / 100 * (perc_total))
    else:
        raise Exception(f"Percentages are above 100: {perc_total}")
    gd_all = {
        "train": gd_list[:cutoff_train],
        "dev": gd_list[cutoff_train:cutoff_dev],
        "eval": gd_list[cutoff_dev:cutoff_eval]
    }
    return gd_all


def merge_overlapping(gd_list):
    print_and_log("####################### merging overlapping entities")
    for gd in gd_list:
        ent_list = gd["entities"]
        ent_list_new = []
        i = 0
        while i < len(ent_list):
            ent_a = ent_list[i]
            ent_correct = ent_a
            for ent_b in ent_list[i + 1:]:
                if ent_a[1] > ent_b[0]:
                    if ent_a[1] > ent_b[1]:
                        ent_correct = (ent_a[0], ent_a[1], ent_a[2])
                    else:
                        ent_correct = (ent_a[0], ent_b[1], ent_a[2])
                    print_and_log(
                        f"Found overlap between: (subtext: {gd['text_raw'][ent_a[0]:ent_a[1]]},"
                        f" ent: {ent_a}), and (subtext: {gd['text_raw'][ent_b[0]:ent_b[1]]}, ent:"
                        f" {ent_b}); merged into {ent_correct}."
                    )
                    if ent_a[2] != ent_b[2]:
                        print_and_log(
                            f"Found conflicting entities at subtext:"
                            f" {gd['text_raw'][ent_a[0]:ent_a[1]]}, '{ent_a[2]}' and: '{ent_b[2]}'."
                            f" Took the first one: '{ent_correct[2]}'"
                        )
                    i += 1
                elif ent_a[0] > ent_b[0]:
                    raise Exception(
                        "list of entities is not correctly sorted by starting indices."
                    )
                else:
                    break
            ent_list_new.append(tuple(ent_correct))
            i += 1
        gd["entities"] = ent_list_new
    return gd_list
    
def convert_to_docbin(gd_list, nlp):
    
    def align_tokens(gd):
        text = gd["text_raw"]
        doc = nlp(text)
        span_list = []
        for ent in gd["entities"]:
            token_id_start = None
            token_id_end = None
            for token in doc:
                if token.idx <= ent[0]:
                    token_id_start = token.i
                elif token.idx < ent[1]:
                    token_id_end = token.i + 1
                else:
                    token_id_end = token.i
                    break
            span = Span(doc, token_id_start, token_id_end, ent[2])
            if span.text != text[ent[0]:ent[1]]:
                print_and_log(
                    f"Minor mismatch between original text of assigned entities and their"
                    f" aligned tokens. The tokens will be used for further processing."
                    f" Original sub text: '{text[ent[0]:ent[1]]}', aligned tokens: '{span.text}'"
                )
            span_list.append(span)
        return doc, span_list
    
    def clean_span_list(span_list, gd):
        text = gd["text_raw"]
        ent_list = gd["entities"]
        text_sub_list = [text[e[0]:e[1]] for e in ent_list]
        span_list_deduplicated = []
        for span in span_list:
            if span_list_deduplicated == []:
                span_list_deduplicated.append(span)
            else:
                valid = True
                for span_other in span_list_deduplicated:
                    if (
                        span == span_other
                        or (span_other.start <= span.start < span_other.end)
                        or (span_other.start < span.end <= span_other.end)
                    ):
                        valid = False
                if valid:
                    span_list_deduplicated.append(span)
        if span_list != span_list_deduplicated:
            print_and_log(
                f"Because of duplication or overlap, span data was converted"
                f" from: {[s.__repr__() for s in span_list]},"
                f" into: {[s.__repr__() for s in span_list_deduplicated]}"
            )
        return span_list_deduplicated
    
    def convert_to_docbin_main():
        print_and_log("####################### creating spacy docs and aligning tokens.")
        doc_bin = DocBin()
        count_handled = 0
        count_not_handled = 0
        for gd in gd_list:
            if len(gd["entities"]) > 0:
                doc, span_list = align_tokens(gd)
                span_list = clean_span_list(span_list, gd)
                doc.set_ents(span_list)
                doc_bin.add(doc)
                count_handled += 1
            else:
                print_and_log(
                    f"No entities found. Dismissing data. At text: {gd['text_raw'].__repr__()}"
                )
                count_not_handled += 1
        print_and_log(
            f"count of converted text-entity rows: {count_handled}, "
            f"count not converted: {count_not_handled}"
        )
        return doc_bin
    
    return convert_to_docbin_main()
    

def main():
    try:
        nlp = spacy.load("/tmp/models_cache/" + MODEL_TO_DOWNLOAD)
        print_and_log(f"loaded model {MODEL_TO_DOWNLOAD} from cache.")
    except OSError:
        print_and_log(f"no model {MODEL_TO_DOWNLOAD} in cache. Downloading.")
        download(MODEL_TO_DOWNLOAD)
        nlp = spacy.load(MODEL_TO_DOWNLOAD)
        nlp.to_disk("/tmp/models_cache/" + MODEL_TO_DOWNLOAD)
        nlp = spacy.load("/tmp/models_cache/" + MODEL_TO_DOWNLOAD)
    perc_train, perc_dev, perc_eval, seed = parse_env_vars()
    gd_all = read_gold_data(perc_train, perc_dev, perc_eval, seed)
    for gd_name, gd_list in gd_all.items():
        print_and_log(f"####################### converting {gd_name} data")
        gd_list = merge_overlapping(gd_list)
        docbin = convert_to_docbin(gd_list, nlp)
        docbin.to_disk(f"{OUT_SPACY_DOCBIN_FOLDER}/{gd_name}.spacy")
    

if __name__ == "__main__":
    main()

