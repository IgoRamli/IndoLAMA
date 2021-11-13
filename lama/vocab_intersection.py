# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from tqdm import tqdm
import argparse
from transformers import AutoTokenizer, BertTokenizer

COMMON_VOCAB_FILENAME = "common_vocab.txt"
TOKENIZERS = [
  'indolem/indobert-base-uncased',
  'cahya/distilbert-base-indonesian'
]

def __vocab_intersection(models, filename):
  vocabularies = []

  for tok_name in models:
    print('Fetching {}'.format(tok_name))
    if 'lite' in tok_name:
      tokenizer = BertTokenizer.from_pretrained(tok_name)
    else:
      tokenizer = AutoTokenizer.from_pretrained(tok_name)

    vocabularies.append(tokenizer.get_vocab())
    print(type(tokenizer.get_vocab()))

  if len(vocabularies) > 0:
    common_vocab = set(vocabularies[0])
    for vocab in vocabularies:
      common_vocab = common_vocab.intersection(set(vocab))

    # store common_vocab on file
    with open(filename, 'w') as f:
      for item in sorted(common_vocab):
        f.write("{}\n".format(item))

def main():
  __vocab_intersection(TOKENIZERS, COMMON_VOCAB_FILENAME)


if __name__ == '__main__':
  main()
