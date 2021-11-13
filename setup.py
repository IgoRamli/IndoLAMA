from setuptools import setup, find_packages

requirements = ['Cython==0.29.2', 'numpy==1.21.4', 'torch==1.10.0', 
'transformers==4.12.3', 'allennlp==2.8.0', 'spacy==3.1.4', 'tqdm==4.62.3', 'termcolor==1.1.0', 'pandas==1.3.4', 'fairseq==0.10.2', 'scipy==1.7.2']
setup(
    name = 'IndoLAMA',
    version = '0.1',
    url = 'https://github.com/IgoRamli/IndoLAMA',
    author = 'Inigo Ramli',
    author_email = 'inigo.ramli@ui.ac.id',
    description = 'IndoLAMA',
    packages = find_packages(),
    install_requires=requirements,
)
