# ProGen2
Official release of the **ProGen2** models (`151M`, `764M`, `2.7B`, `6.4B`) for **Protein Engineering**.

## Models

| Model | Size | Checkpoint |
| ------ | ------ | ---------- |
| progen2-small	   | `151M` | https://storage.googleapis.com/anonymized-progen-research/checkpoints/progen2-small.tar.gz |
| progen2-medium   | `764M` | https://storage.googleapis.com/anonymized-progen-research/checkpoints/progen2-medium.tar.gz |
| progen2-oas	     | `764M` | https://storage.googleapis.com/anonymized-progen-research/checkpoints/progen2-oas.tar.gz |
| progen2-base     | `764M` | https://storage.googleapis.com/anonymized-progen-research/checkpoints/progen2-base.tar.gz |
| progen2-large    | `2.7B` |  https://storage.googleapis.com/anonymized-progen-research/checkpoints/progen2-large.tar.gz |
| progen2-BFD90    | `2.7B` | https://storage.googleapis.com/anonymized-progen-research/checkpoints/progen2-BFD90.tar.gz |
| progen2-xlarge   | `6.4B` | https://storage.googleapis.com/anonymized-progen-research/checkpoints/progen2-xlarge.tar.gz |

## Setup
```sh
# code
git clone https://github.com/anonymized-research/progen2
cd progen2

# checkpoint
model=progen2-large
wget -P checkpoints/${model} https://storage.googleapis.com/anonymized-progen-research/checkpoints/${model}.tar.gz
tar -xvf checkpoints/${model}/${model}.tar.gz -C checkpoints/${model}/

# venv
python3.8 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip setuptools
pip3 install -r requirements.txt

# sample
python3 sample.py --model ${model} --t 0.8 --p 0.9 --max-length 1024 --num-samples 2 --context "1"

# log-likelihood (GenBank: TMF32756.1)
python3 likelihood.py --model ${model} --context "1MGHGVSRPPVVTLRPAVLDDCPVLWRWRNDPETRQASVDEREIPVDTHTRWFEETLKRFDRKLFIVSADGVDAGMVRLDIQDRDAAVSVNIAPEWRGRGVGPRALGCLSREAFGPLALLRMSAVVKRENAASRIAFERAGFTVVDTGGPLLHSSKARLHVVAAIQARMGSTRLPGKVLVSIAGRPTIQRIAERLAVCQELDAVAVSTSVENRDDAIADLAAHLGLVCVRGSETDLIERLGRTAARTGADALVRITADCPLVDPALVDRVVGVWRRSAGRLEYVSNVFPPTFPDGLDVEVLSRTVLERLDREVSDPFFRESLTAYVREHPAAFEIANVEHPEDLSRLRWTMDYPEDLAFVEAVYRRLGNQGEIFGMDDLLRLLEWSPELRDLNRCREDVTVERGIRGTGYHAALRARGQAP2"
```

## License
Our code and models are BSD-3 licensed. See LICENSE.txt for details.

## Ethics
Predicting the fitness of a protein sequence and capturing the distribution of natural proteins for generative purposes could be a powerful tool for protein design. If our technique or a future iteration thereof is adopted broadly, care should be taken in terms of the end use-cases of these designed samples and downstream effects to ensure safe, non-nefarious, and ethical applications. For projects in any domain, active oversight during project initiation, experimental optimization, and deployment phases should be put in place to ensure safe usage and limitation of unintended harmful effects.

## Paper
[ProGen2: Exploring the boundaries of protein language models](https://www.sciencedirect.com/science/article/abs/pii/S2405471223002727?via%3Dihub)  

## Standard PROGEN2 models
The standard PROGEN2 models are pretrained on a mixture of Uniref90 (Suzek et al., 2015) and BFD30 (Steinegger & Söding, 2018) databases.  
Uniref90 are cluster representative sequences from UniprotKB at 90% sequence identity. The BFD30 dataset is approximately 1=3 the size of Uniref90, majority from metagenomic sources, commonly not full-length proteins, and clustered at 30% sequence identity.  

## PROGEN2-BFD90 model

For the PROGEN2-BFD90 model, Uniref90 is mixed with representative sequences with at least 3 cluster members after clustering UniprotKB, Metaclust, SRC, and MERC at 90% sequence identity. This BFD90 dataset is approximately twice the size as Uniref90. 

## PROGEN2-OAS Model
To train the antibody-specific PROGEN2-OAS, we collected unpaired antibody sequences from the Observed Antibody Space (OAS) database (Olsen et al., 2022a). OAS is a curated collection of
1.5B antibody sequences from eighty immune repertoire sequencing studies, which contains heavy and light chain sequences from six species (humans, mice, rats, camel, rabbit, and rhesus). The
sequences in OAS possess a significant degree of redundancy, due both to discrepancies in the sizes of its constituent studies, as well as the innate biological redundancy of antibody sequences within
organisms. To reduce this redundancy, we clustered the OAS sequences at 85% sequence identity using Linclust (Steinegger & Söding, 2018), yielding a set of 554M sequences for model training.
Alignment coverage in Linclust was calculated with respect to the target sequence ("cov-mode 1"), with all other parameters set to their default values.  

All samples are provided to the model with a 1 or 2 character token concatenated at the N-terminal and C-terminal side of the sequence. Each sequence is then provided as-is and flipped. For a given
batch, proteins are concatenated with others to fill the maximum token length during training.  


