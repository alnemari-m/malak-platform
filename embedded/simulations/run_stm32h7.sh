#!/bin/bash
# Run CIFAR-10 inference simulation on STM32H7 (Cortex-M7)

set -e

echo "=========================================="
echo "STM32H7 Simulation - Malak Platform"
echo "=========================================="
echo ""

# Check if model is compiled
if [ ! -f "../models/cifar10_demo.elf" ]; then
    echo "ERROR: Model binary not found!"
    echo "Please run: cd ../models && make"
    exit 1
fi

# Check if Renode is installed
if ! command -v renode &> /dev/null; then
    echo "ERROR: Renode not found!"
    echo "Please run: ../install_renode.sh"
    exit 1
fi

echo "Starting Renode simulation..."
echo "Platform: STM32H7 (ARM Cortex-M7 @ 480 MHz)"
echo ""

# Run simulation
renode --disable-xwt --console ../platforms/stm32h7.resc

echo ""
echo "=========================================="
echo "Simulation complete!"
echo "=========================================="
echo ""
echo "Results saved to: ../results/stm32h7_simulation.log"
echo ""
echo "To view results:"
echo "  cat ../results/stm32h7_simulation.log"
echo ""
echo "To analyze metrics:"
echo "  python ../scripts/collect_metrics.py stm32h7"
echo ""
