#!/bin/bash
# run_mutation_comparison.sh
#
# Compares mutation scores between the baseline and partition test suites
# against register() and login() in backend/app/routes/auth.py.
#
# Usage (run from project root):
#   bash testing/mutation-analysis/auth-register-login/run_mutation_comparison.sh
#
# Passes:
#   1 — baseline suite:   testing/baseline-tests/test_auth.py          (8 tests)
#   2 — partition suite:  test_register_partition.py + test_login_partition.py  (17 tests)
#
# Output:
#   testing/mutation-analysis/auth-register-login/mutation_results/baseline_results.txt
#   testing/mutation-analysis/auth-register-login/mutation_results/partition_results.txt
#   testing/mutation-analysis/auth-register-login/mutation_results/mutmut-cache-baseline
#   testing/mutation-analysis/auth-register-login/mutation_results/mutmut-cache-partition
#
# To inspect a saved run later:
#   cp testing/mutation-analysis/auth-register-login/mutation_results/mutmut-cache-baseline .mutmut-cache
#   mutmut results

set -euo pipefail

TARGET="backend/app/routes/auth.py"
RESULTS_DIR="testing/mutation-analysis/auth-register-login/mutation_results"

BASELINE_RUNNER="python3 -m pytest testing/baseline-tests/test_auth.py -x -q"
PARTITION_RUNNER="python3 -m pytest \
  testing/input-partition-models/test_register_partition.py \
  testing/input-partition-models/test_login_partition.py \
  -x -q"

mkdir -p "$RESULTS_DIR"

# ── helper: extract killed/total from mutmut results ─────────────────────────
summarize() {
    local label="$1"
    local out_file="$2"
    mutmut results > "$out_file"
    echo ""
    echo "=== $label ==="
    cat "$out_file"
}

# ── Pass 1: baseline ──────────────────────────────────────────────────────────
echo ""
echo "######################################"
echo "#  Pass 1/2 — Baseline: test_auth.py  #"
echo "######################################"

rm -f .mutmut-cache
mutmut run \
    --paths-to-mutate "$TARGET" \
    --tests-dir testing/baseline-tests \
    --runner "$BASELINE_RUNNER" \
    --simple-output || true   # non-zero exit when mutants survive is expected

summarize "Baseline results" "$RESULTS_DIR/baseline_results.txt"
cp .mutmut-cache "$RESULTS_DIR/mutmut-cache-baseline"

# ── Pass 2: partition ─────────────────────────────────────────────────────────
echo ""
echo "########################################################"
echo "#  Pass 2/2 — Partition: register + login partition    #"
echo "########################################################"

rm -f .mutmut-cache
mutmut run \
    --paths-to-mutate "$TARGET" \
    --tests-dir testing/input-partition-models \
    --runner "$PARTITION_RUNNER" \
    --simple-output || true

summarize "Partition results" "$RESULTS_DIR/partition_results.txt"
cp .mutmut-cache "$RESULTS_DIR/mutmut-cache-partition"

# ── Side-by-side summary ──────────────────────────────────────────────────────
echo ""
echo "========================================"
echo "  Mutation comparison complete"
echo "  Results saved to: $RESULTS_DIR/"
echo "    baseline_results.txt"
echo "    partition_results.txt"
echo "    mutmut-cache-baseline  (restore with: cp $RESULTS_DIR/mutmut-cache-baseline .mutmut-cache)"
echo "    mutmut-cache-partition (restore with: cp $RESULTS_DIR/mutmut-cache-partition .mutmut-cache)"
echo "========================================"
