#!/bin/bash
# Monitor all running experiments
# Usage: ./monitor_experiments.sh

echo "=============================================================================="
echo "EXPERIMENT MONITORING DASHBOARD"
echo "=============================================================================="
echo ""

# Check pruning experiment
echo "📊 PRUNING EXPERIMENT STATUS:"
if [ -f "experiment_results/pruning_log.txt" ]; then
    echo "  File exists: experiment_results/pruning_log.txt"
    LAST_EPOCH=$(tail -100 experiment_results/pruning_log.txt | grep "Epoch" | tail -1)
    LAST_ACC=$(tail -100 experiment_results/pruning_log.txt | grep "Test Acc" | tail -1)
    echo "  $LAST_EPOCH"
    echo "  $LAST_ACC"
else
    echo "  ⏳ Not started or no log file yet"
fi
echo ""

# Check architecture experiment
echo "📊 ARCHITECTURE COMPARISON STATUS:"
if [ -f "experiment_results/architectures/architecture_log.txt" ]; then
    echo "  File exists: experiment_results/architectures/architecture_log.txt"
    LAST_LINE=$(tail -5 experiment_results/architectures/architecture_log.txt)
    echo "  $LAST_LINE"
else
    echo "  ⏳ Not started yet"
fi
echo ""

# Check completed experiments
echo "✅ COMPLETED EXPERIMENTS:"
[ -f "experiment_results/results.json" ] && echo "  ✅ CIFAR-10 baseline"
[ -f "experiment_results/fashion_mnist/results.json" ] && echo "  ✅ Fashion-MNIST"
[ -f "renode_experiments/results/real_simulation_metrics.json" ] && echo "  ✅ Renode validation"
echo ""

# Check for results files
echo "📁 RESULTS FILES:"
find experiment_results -name "*.json" -o -name "*_results.json" 2>/dev/null | while read file; do
    echo "  - $file"
done
echo ""

# System resources
echo "💻 SYSTEM RESOURCES:"
echo "  CPU Usage: $(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}')"
echo "  Memory: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo ""

echo "=============================================================================="
echo "Run this script periodically to monitor progress"
echo "=============================================================================="
