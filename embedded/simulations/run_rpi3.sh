#!/bin/bash
# Run CIFAR-10 inference simulation on Raspberry Pi 3 (Cortex-A53)

set -e

echo "=========================================="
echo "Raspberry Pi 3 Simulation - Malak Platform"
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
echo "Platform: Raspberry Pi 3 (ARM Cortex-A53 @ 1.2 GHz)"
echo ""

# Run simulation
renode --disable-xwt --console ../platforms/rpi3.resc

echo ""
echo "=========================================="
echo "Simulation complete!"
echo "=========================================="
echo ""
echo "Results saved to: ../results/rpi3_simulation.log"
echo ""
echo "To view results:"
echo "  cat ../results/rpi3_simulation.log"
echo ""
echo "To analyze metrics:"
echo "  python ../scripts/collect_metrics.py rpi3"
echo ""
