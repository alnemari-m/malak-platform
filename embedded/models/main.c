
/* Test application for CIFAR-10 inference on embedded hardware */
/* Compiled for ARM Cortex-M7 (STM32H7) */

#include "cifar10_model.h"
#include <stdio.h>
#include <stdint.h>

/* Sample CIFAR-10 test image (32x32x3 = 3072 bytes) */
/* This would be replaced with actual test data */
const uint8_t test_image[INPUT_SIZE] = {
    /* Placeholder: Random values for demonstration */
    128, 64, 192, 255, 0, /* ... */
};

/* DWT (Data Watchpoint and Trace) for cycle counting on Cortex-M */
#define DWT_CONTROL             (*((volatile uint32_t*)0xE0001000))
#define DWT_CYCCNT              (*((volatile uint32_t*)0xE0001004))
#define DEM_CR                  (*((volatile uint32_t*)0xE000EDFC))
#define DEM_CR_TRCENA           (1 << 24)

void enable_cycle_counter(void) {
    /* Enable DWT */
    DEM_CR |= DEM_CR_TRCENA;
    /* Reset cycle counter */
    DWT_CYCCNT = 0;
    /* Enable cycle counter */
    DWT_CONTROL |= 1;
}

uint32_t get_cycle_count(void) {
    return DWT_CYCCNT;
}

int main(void) {
    printf("========================================\n");
    printf("CIFAR-10 Inference Test on Embedded HW\n");
    printf("Platform: ARM Cortex-M7 (STM32H7)\n");
    printf("========================================\n\n");

    /* Initialize cycle counter */
    enable_cycle_counter();

    /* Initialize model */
    printf("Initializing model...\n");
    if (model_init() != 0) {
        printf("ERROR: Model initialization failed\n");
        return -1;
    }
    printf("✓ Model initialized\n\n");

    /* Print memory requirements */
    size_t memory_needed = model_get_memory_size();
    printf("Memory required: %zu bytes (%.2f KB)\n\n",
           memory_needed, memory_needed / 1024.0);

    /* Run inference */
    float output[NUM_CLASSES];

    printf("Running inference...\n");
    uint32_t start_cycles = get_cycle_count();

    int result = model_infer(test_image, output);

    uint32_t end_cycles = get_cycle_count();
    uint32_t elapsed_cycles = end_cycles - start_cycles;

    if (result != 0) {
        printf("ERROR: Inference failed\n");
        return -1;
    }

    /* Print results */
    printf("✓ Inference complete\n\n");

    printf("Performance Metrics:\n");
    printf("  Cycles: %lu\n", (unsigned long)elapsed_cycles);
    printf("  Time @ 480 MHz: %.2f ms\n", elapsed_cycles / 480000.0);
    printf("  Time @ 240 MHz: %.2f ms\n", elapsed_cycles / 240000.0);
    printf("\n");

    /* Print output logits */
    printf("Output Logits:\n");
    for (int i = 0; i < NUM_CLASSES; i++) {
        printf("  Class %d: %.4f\n", i, output[i]);
    }
    printf("\n");

    /* Get predicted class */
    int predicted = model_argmax(output);
    printf("Predicted class: %d\n", predicted);

    printf("\n========================================\n");
    printf("Test completed successfully!\n");
    printf("========================================\n");

    return 0;
}
