import os
import argparse
import json
import random
import uuid
from tqdm import tqdm
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--title-path')
parser.add_argument('--triplet-path')
parser.add_argument('--vocab-path')
parser.add_argument('--out-dir', default='IndoLAMA')

random.seed(42)

LAMA_RELATIONS = [
  'P19', 'P20', 'P279', 'P37', 'P413',
  'P166', 'P449', 'P69', 'P47', 'P138',
  'P364', 'P54', 'P463', 'P101', 'P1923',
  'P106', 'P527', 'P102', 'P530', 'P176',
  'P27', 'P407', 'P30', 'P178', 'P1376',
  'P131', 'P1412', 'P108', 'P136', 'P17',
  'P39', 'P264', 'P276', 'P937', 'P140',
  'P1303', 'P127', 'P103', 'P190', 'P1001',
  'P31', 'P495', 'P159', 'P36', 'P740', 'P361'
]

if __name__ == '__main__':
  args = parser.parse_args()

  print('| Fetching common vocabulary')
  vocab = set()
  with open(args.vocab_path, 'r') as f:
    for line in f.readlines():
      vocab.add(line.strip('\n'))

  titles = {}
  single_tokens = set()
  with open(args.title_path, 'r') as f:
    for row in f:
      terms = row.split()
      k = terms[0]
      v = terms[1:]
      titles[k] = ' '.join(v)
      if titles[k].lower() in vocab:
        single_tokens.add(k)
  print('| Number of single token entities: {}'.format(len(single_tokens)))

  valid_relations = {}
  with open(args.triplet_path, 'r') as f:
    for row in f:
      head, relation, tail = row.split()
      if tail in single_tokens:
        if relation not in valid_relations:
          valid_relations[relation] = []
        valid_relations[relation].append((head, tail))

  print('| Number of single token objects per LAMA relations')
  for i in LAMA_RELATIONS:
    print(' -) {} ({})'.format(i, len(valid_relations.get(i, []))))

  for relation, entities in valid_relations.items():
    if relation not in LAMA_RELATIONS:
      continue
    print('| Collecting valid relations for {}'.format(relation))
    indolama = []
    for ent in tqdm(entities):
      head = ent[0]
      tail = ent[1]
      relation_dict = {
        'uuid': str(uuid.uuid4()),
        'sub_uri': head,
        'obj_uri': tail,
        'sub_label': titles[head],
        'obj_label': titles[tail],
        'predicate_id': relation
      }
      indolama.append(relation_dict)
    indolama_sample = random.sample(indolama, k=min(1000, len(indolama)))

    filename = '{}.jsonl'.format(relation)
    filename = os.path.join(args.out_dir, filename)
    Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    
    with open(filename, 'w+') as f:
      for rel in indolama_sample:
        f.write(json.dumps(rel) + '\n')
