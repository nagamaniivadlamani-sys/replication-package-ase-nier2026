# IM-CED: Intent-Mined Counterexample Detection for Vulnerability Analysis

IM-CED is a lightweight hybrid vulnerability detection framework that combines semantic intent mining, lightweight static analysis, angr-based execution analysis, and KLEE symbolic execution for software vulnerability analysis.

The framework integrates:
- CodeBERT semantic embeddings
- Lightweight static analysis
- angr-based execution analysis
- KLEE symbolic execution
- Hybrid vulnerability prediction

---

# Project Structure

```bash
imcedd_project/
│
├── imced_finaloutput.py
│
├── binaries/
│   ├── Juliet benchmark binaries
│   └── vulnerable binaries
│
├── programs/
│   ├── overflow.c
│   ├── int_overflow.c
│   ├── nullp.c
│   ├── safe programs
│   └── other vulnerable programs
│
├── klee programs/
│   ├── overflow.bc
│   ├── int_overflow.bc
│   └── nullp.bc
│
└── output/
    └── results table
```

---

# Vulnerability Categories

The framework evaluates vulnerable and safe C programs across multiple CWE categories:

| Vulnerability Type | CWE |
|---|---|
| Buffer Overflow | CWE-121 |
| Command Injection | CWE-78 |
| Integer Overflow | CWE-190 |
| Memory Leak | CWE-401 |
| Null Pointer Dereference | CWE-690 |

The dataset includes:
- Juliet benchmark samples
- Curated vulnerable programs
- Safe program samples

---

# Experimental Environment

The experiments were conducted using:

- Windows Subsystem for Linux (WSL)
- Ubuntu Linux
- Python 3.x
- CodeBERT
- angr
- KLEE
- Docker
- LLVM/Clang

---

# Step 1: Create Virtual Environment

```bash
python3 -m venv imced_env
source imced_env/bin/activate
```

---

# Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Step 3: Compile Programs

Compile vulnerable programs using GCC:

```bash
gcc programs/overflow.c -o programs/overflow
gcc programs/int_overflow.c -o programs/int_overflow
gcc programs/nullp.c -o programs/nullp
```

Compiled binaries are used for angr-based execution analysis.

---

# Step 4: Run IM-CED Framework

Execute the integrated framework:

```bash
python imced_finaloutput.py
```

The framework performs:
- Program loading
- Semantic embedding generation
- Cosine similarity computation
- Lightweight static analysis
- angr-based execution analysis
- Hybrid vulnerability prediction
- Accuracy and F1-score evaluation

---

# Step 5: Running KLEE Symbolic Execution

Compile vulnerable programs into LLVM bitcode:

```bash
clang -emit-llvm -c -g programs/overflow.c -o overflow.bc
```

Run KLEE through Docker:

```bash
docker run --rm -v $(pwd):/home/klee klee/klee klee /home/klee/overflow.bc
```

This step generates:
- Symbolic execution paths
- Test cases
- Error reports
- Counterexamples

---

# Representative Counterexamples

| Vulnerability Type | Counterexample | Observed Behavior |
|---|---|---|
| Buffer Overflow | AAAAAAAAAAAA | Out-of-bound memory access |
| Integer Overflow | 2147483647 | Arithmetic overflow |
| Null Pointer Dereference | NULL symbolic path | Null page access violation |

---

# Experimental Results

| Model | Accuracy | Precision | Recall | F1-score |
|---|---|---|---|---|
| Baseline | 50% | 70% | 61% | 65% |
| IM-CED | 83% | 100% | 78% | 88% |

---

# Reproducibility

The repository contains implementation artifacts, benchmark programs, symbolic execution outputs, and evaluation results to support reproducibility of the reported experiments.

---

# License

This project is provided for research and educational purposes.
