# IndoLAMA

IndoLAMA is a knowledge probing benchmark for Indonesian language models. Processing of IndoLAMA dataset follows [Petroni et al. 2019](https://github.com/facebookresearch/LAMA)

## Versions

This repository contais 3 variants of IndoLAMA. All variants are built from [IndoWiki](https://github.com/IgoRamli/IndoWiki.git):
- IndoLAMA: Probing dataset taken from the transductive training split of IndoWiki (indowiki_transductive_train.txt). This means that any model trained with IndoWiki would have encountered these dataset. Useful to determine whether the trained model can recall factual knowledge properly.
- IndoLAMA-Test-Only: Probing dataset taken from the transductive **test** split of IndoWiki (indowiki_transductive_test.txt). Knowledge in this dataset is not present in the training split. However, entities (subject/object) that appear on this dataset may also appear in the training split. 
- IndoLAMA-Inductive: Probing dataset taken from the **inductive** test split of IndoWiki (indowiki_inductive_test.txt). No entities present on this knowledge probing dataset should appear on the inductive training split of IndoWiki. This dataset is meant to test if a model is able to "induce" knowledge on unseen entities.

## Knowledge Source

This benchmark uses IndoWiki as it's knowledge source. IndoWiki is a knowledge-graph dataset based on Wikipedia Bahasa Indonesia and WikiData. The method of acquiring factual knowledge from IndoWiki follows LAMA's preprocessing step for T-Rex dataset:

"""
We consider 41 Wikidata relations and subsam-
ple at most 1000 facts per relation. As with the
Google-RE corpus, we manually define a tem-
plate for each relation
"""

This repository follows the list of Wikidata relations used by LAMA.

## Templates

The templates for each relation is manually defined. Below is the template definition for each predicate:

| Relation ID | Label                   | Template                                             |
|-------------|-------------------------|------------------------------------------------------|
| P17         | country                 | (subjek) berada di negara (objek)                    |
| P19         | place of birth          | (subjek) dilahirkan di (objek)                       |
| P20         | place of death          | (subjek) wafat di (objek)                            |
| P27         | country of citizenship  | (subjek) merupakan warga negara dari (objek)         |
| P30         | continent               | (subjek) terletak di benua (objek)                   |
| P31         | instance of             | (subjek) adalah (objek)                              |
| P36         | capital                 | Ibu kota dari (subjek) adalah (objek)                |
| P37         | official language       | Salah satu bahasa resmi dari (subjek) adalah (objek) |
| P39         | position held           | (subjek) memiliki jabatan sebagai (objek)            |
| P47         | shares border with      | (subjek) memiliki perbatasan dengan (objek)          |
| P54         | member of sports team   | (subjek) bermain untuk (objek)                       |
| P69         | educated at             | (subjek) pernah menempuh pendidikan di (objek)       |
| P101        | field of work           | (subjek) memiliki spesialisasi di bidang (objek)     |
| P102        | member of<br>political party | (subjek) adalah anggota partai (objek)          |
| P103        | native language         | Bahasa ibu dari (subjek) adalah (objek)              |
| P106        | occupation              | (subjek) bekerja sebagai (objek)                     |
| P108        | employer                | (subjek) bekerja untuk (objek)                       |
| P127        | owned by                | (subjek) dimiliki oleh (objek)                       |
| P131        | located in the adm.<br>territorial entity | (subjek) berada di daerah (objek)  |
| P136        | genre                   | (subjek) memainkan musik (objek)                     |
| P138        | named after             | (subjek) mendapatkan namanya dari (objek)            |
| P140        | religion                | Agama dari (subjek) adalah (objek)                   |
| P159        | headquarters location   | Kantor pusat (subjek) terletak di (objek)            |
| P166        | award received          | (subjek) pernah menerima penghargaan (objek)         |
| P176        | manufacturer            | (subjek) diproduksi oleh (objek)                     |
| P178        | developer               | (subjek) dikembangkan oleh (objek)                   |
| P190        | twinned administrative body | (subjek) dan (objek) merupakan kota kembar       |
| P264        | record label            | Merek (subjek) dimiliki oleh (objek)                 |
| P276        | location                | (subjek) terletak di (objek)                         |
| P279        | subclass of             | (subjek) adalah jenis dari (objek)                   |
| P361        | part of                 | (subjek) merupakan bagian dari (objek)               |
| P364        | original language of<br>film or TV show | Bahasa asli dari (subjek) adalah (objek) |
| P407        | language of work or name| (subjek) ditulis dalam bahasa (objek)                |
| P413        | position played on<br>team/speciality | (subjek) bermain di posisi (objek)     |
| P449        | original network        | (subjek) ditayangkan pertama kali pada (objek)       |
| P463        | member of               | (subjek) adalah anggota dari (objek)                 |
| P495        | country of origin       | (subjek) berasal dari (objek)                        |
| P527        | has part                | (subjek) terdiri dari (objek)                        |
| P530        | diplomatic relation     | (subjek) memiliki hubungan diplomatik dengan (objek) |
| P740        | location of formation   | (subjek) didirikan di (objek)                        |
| P937        | work location           | (subjek) bekerja di (objek)                          |
| P1001       | applies to jurisdiction | (subjek) pernah diterapkan ke yurisdiksi (objek)     |
| P1303       | instrument              | (subjek) bisa memainkan instrumen (objek)            |
| P1376       | capital of              | (subjek) adalah ibu kota dari (objek)                |
| P1412       | language spoken,<br>written, or signed | (subjek) berbahasa (objek)            |
| P1923       | participating team      | (objek) adalah tim yang ikut serta pada (subjek)     |