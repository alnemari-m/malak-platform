#!/bin/bash
# Run all Renode simulations for Malak Platform validation

set -e

echo "============================================================"
echo "Malak Platform - Complete Renode Validation Suite"
echo "============================================================"
echo ""

# Step 1: Build model
echo "Step 1: Building model for embedded deployment..."
cd ../models
if [ ! -f "Makefile" ]; then
    echo "ERROR: Makefile not found. Run export_model.py first."
    exit 1
fi

make clean
make

if [ ! -f "cifar10_demo.elf" ]; then
    echo "ERROR: Build failed. Check compiler errors above."
    exit 1
fi

echo "✓ Model built successfully"
echo ""

cd ../simulations

# Step 2: Run STM32H7 simulation
echo "Step 2: Running STM32H7 (Cortex-M7) simulation..."
./run_stm32h7.sh
echo "✓ STM32H7 simulation complete"
echo ""

# Step 3: Run Raspberry Pi 3 simulation
echo "Step 3: Running Raspberry Pi 3 (Cortex-A53) simulation..."
./run_rpi3.sh
echo "✓ Raspberry Pi 3 simulation complete"
echo ""

# Step 4: Collect and analyze metrics
echo "Step 4: Analyzing results..."
cd ../scripts
python collect_metrics.py all

echo ""
echo "============================================================"
echo "✓ All simulations complete!"
echo "============================================================"
echo ""
echo "Results summary:"
echo "  - STM32H7: ../results/stm32h7_metrics.json"
echo "  - RPi3:    ../results/rpi3_metrics.json"
echo "  - Summary: ../results/simulation_summary.json"
echo ""
echo "To generate paper tables:"
echo "  python generate_paper_tables.py"
echo ""
