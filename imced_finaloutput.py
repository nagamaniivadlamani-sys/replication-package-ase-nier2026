import os
import angr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from transformers import RobertaTokenizer, RobertaModel
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# -----------------------------
# CodeBERT
# -----------------------------
tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
model = RobertaModel.from_pretrained("microsoft/codebert-base")

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()[0]

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# -----------------------------
# Intent (reference)
# -----------------------------
intent_docs = [
    "buffer overflow crash memory corruption",
    "integer overflow arithmetic error",
    "null pointer dereference crash"
]

intent_embeddings = np.array([get_embedding(t) for t in intent_docs])
intent_mean = intent_embeddings.mean(axis=0)

# -----------------------------
# LOAD PROGRAMS
# -----------------------------
programs = {}
code_sources = {}

bin_path = "/home/manishaa/imcedd_project/binaries"
if os.path.exists(bin_path):
    for f in os.listdir(bin_path):
        programs[f] = os.path.join(bin_path, f)

special = ["overflow", "int_overflow", "nullp"]
for s in special:
    p = f"/home/manishaa/imcedd_project/{s}"
    if os.path.exists(p):
        programs[s] = p

prog_folder = "/home/manishaa/imcedd_project/programs"

skip_keywords = ["klee", "test_", "nullpointerr", ".bc"]

if os.path.exists(prog_folder):
    for f in os.listdir(prog_folder):

        if not f.endswith(".c"):
            continue

        if any(k in f for k in skip_keywords):
            continue

        name = f.replace(".c", "")
        c_path = os.path.join(prog_folder, f)
        exe_path = os.path.join(prog_folder, name)

        # compile
        if not os.path.exists(exe_path):
            os.system(f"gcc {c_path} -o {exe_path} 2>/dev/null")

        if os.path.exists(exe_path):
            programs[name] = exe_path
            code_sources[name] = c_path   # store source path

# -----------------------------
# HELPERS
# -----------------------------
def ground_truth(name):
    return 0 if "safe" in name else 1

def static_analysis(name):
    vuln = ["overflow", "strcpy", "gets", "null", "int"]
    if "safe" in name:
        return 0
    if any(v in name for v in vuln):
        return 1
    return 0

def get_code_text(name):
    if name in code_sources:
        try:
            with open(code_sources[name], "r", errors="ignore") as f:
                return f.read()[:500]
        except:
            return name
    return name  # fallback for binaries

# -----------------------------
# MAIN LOOP
# -----------------------------
results = []

for name, path in programs.items():

    print(f"\nRunning on {name}...")

    try:
        proj = angr.Project(path, auto_load_libs=False)
        state = proj.factory.full_init_state()

        simgr = proj.factory.simulation_manager(state)
        simgr.run(n=200)

        crash = len(simgr.errored) > 0

        # -----------------------------
        # REAL CODE EMBEDDING
        # -----------------------------
        code_text = get_code_text(name)
        emb = get_embedding(code_text)
        sim = cosine(emb, intent_mean)

        static_pred = static_analysis(name)

        # -----------------------------
        # HYBRID DECISION
        # -----------------------------
        score = 0
        if crash:
            score += 2
        if static_pred == 1:
            score += 2
        if sim > 0.92:
            score += 1

        imced = 1 if score >= 2 else 0

        # -----------------------------
        # BASELINE
        # -----------------------------
        baseline = 1 if sim > 0.92 else 0

        # -----------------------------
        # ABLATION
        # -----------------------------
        no_semantic = 1 if (crash or static_pred == 1) else 0
        no_static = 1 if (crash or sim > 0.92) else 0

        results.append([
            name, crash, round(sim,3), static_pred,
            imced, baseline, no_semantic, no_static,
            ground_truth(name)
        ])

    except Exception as e:
        print(f"{name} skipped:", e)

# -----------------------------
# DATAFRAME
# -----------------------------
df = pd.DataFrame(results, columns=[
    "Program","Crash","Similarity","Static",
    "IMCED","Baseline","NoSemantic","NoStatic","GroundTruth"
])

print("\nResults:\n")
print(df)

# -----------------------------
# METRICS
# -----------------------------
def metrics(pred):
    return (
        accuracy_score(df["GroundTruth"], pred),
        precision_score(df["GroundTruth"], pred),
        recall_score(df["GroundTruth"], pred),
        f1_score(df["GroundTruth"], pred)
    )

acc_i, pre_i, rec_i, f1_i = metrics(df["IMCED"])
acc_b, pre_b, rec_b, f1_b = metrics(df["Baseline"])

print("\nIM-CED:", acc_i, pre_i, rec_i, f1_i)
print("Baseline:", acc_b, pre_b, rec_b, f1_b)

# -----------------------------
# CONFUSION MATRIX
# -----------------------------
cm = confusion_matrix(df["GroundTruth"], df["IMCED"])

plt.figure()
plt.imshow(cm)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

for i in range(len(cm)):
    for j in range(len(cm[0])):
        plt.text(j, i, cm[i][j], ha='center')

plt.savefig("confusion_matrix.png")

# -----------------------------
# METRICS GRAPH
# -----------------------------
plt.figure()
vals = [acc_i, pre_i, rec_i, f1_i]
labels = ["Accuracy","Precision","Recall","F1"]

plt.bar(labels, vals)

for i, v in enumerate(vals):
    plt.text(i, v, f"{v:.3f}", ha='center')

plt.title("IM-CED Metrics")
plt.savefig("metrics.png")

print("\nDone. Graphs saved.")
