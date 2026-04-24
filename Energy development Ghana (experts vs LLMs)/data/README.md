## LLM-generated data structure

This repository contains raw and processed outputs from Large Language Model (LLM) experiments conducted within the MCDA-based evaluation framework. The data are organized by model, with separate folders for each evaluated LLM:

- GPT 5.3-mini
- Flash 3.0
- Grok 4.2
- Sonar
- Sonnet 4.6

### Folder structure

Each model folder contains:

#### 1. Aggregated dataset (Excel file)

A file named: `model_run_data.xlsx`

This file includes the consolidated results of all prompt executions for a given model. It contains structured evaluation outputs used for subsequent MCDA analysis, including criteria weights and alternative performance assessments.

---

#### 2. Raw LLM outputs (text files)

Each individual prompt execution is stored as a separate `.txt` file following the naming convention: `model_run_<run_number>attempt<attempt_number>.txt`

Where:

- `run_number` refers to a single experimental run (corresponding to one complete evaluation set),
- `attempt_number` indicates the number of attempts required to obtain a valid response for that run.

---

### Handling of invalid or incomplete responses

In cases where the LLM output was incomplete, non-compliant with the prompt instructions, or did not contain a full set of required evaluation data (e.g., missing elements in decision matrices), the response was marked as invalid at the end of the text file.

For such cases:

- The same `run_number` was retained,
- The `attempt_number` was incremented,
- The prompt was re-executed in a new interaction until a valid output satisfying all prompt constraints was obtained.

This mechanism ensures:

- traceability of failed and successful generations,
- full transparency of re-prompting procedures,
- reproducibility of the dataset construction process.

---

### Reproducibility note

Both valid and invalid outputs are preserved in the repository to ensure full auditability of the experimental procedure and to allow independent replication of the LLM evaluation process.
