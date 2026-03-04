/* Startup code for ARM Cortex-M7 (STM32H7) */
/* Minimal bare-metal initialization for Renode simulation */

#include <stdint.h>

/* External symbols from linker script */
extern uint32_t _estack;
extern uint32_t _sidata;
extern uint32_t _sdata;
extern uint32_t _edata;
extern uint32_t _sbss;
extern uint32_t _ebss;

/* Main function */
extern int main(void);

/* Reset handler - entry point after reset */
void Reset_Handler(void);

/* Default handler for unused interrupts */
void Default_Handler(void);

/* Cortex-M7 core interrupts */
void NMI_Handler(void) __attribute__((weak, alias("Default_Handler")));
void HardFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void MemManage_Handler(void) __attribute__((weak, alias("Default_Handler")));
void BusFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void UsageFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void SVC_Handler(void) __attribute__((weak, alias("Default_Handler")));
void DebugMon_Handler(void) __attribute__((weak, alias("Default_Handler")));
void PendSV_Handler(void) __attribute__((weak, alias("Default_Handler")));
void SysTick_Handler(void) __attribute__((weak, alias("Default_Handler")));

/* Vector table */
__attribute__((section(".isr_vector")))
void (* const g_pfnVectors[])(void) = {
    (void (*)(void))(&_estack),          /* Initial stack pointer */
    Reset_Handler,                        /* Reset handler */
    NMI_Handler,                         /* NMI handler */
    HardFault_Handler,                   /* Hard fault handler */
    MemManage_Handler,                   /* MPU fault handler */
    BusFault_Handler,                    /* Bus fault handler */
    UsageFault_Handler,                  /* Usage fault handler */
    0,                                   /* Reserved */
    0,                                   /* Reserved */
    0,                                   /* Reserved */
    0,                                   /* Reserved */
    SVC_Handler,                         /* SVCall handler */
    DebugMon_Handler,                    /* Debug monitor handler */
    0,                                   /* Reserved */
    PendSV_Handler,                      /* PendSV handler */
    SysTick_Handler,                     /* SysTick handler */

    /* External interrupts (STM32H7 specific) */
    /* For simulation, we only need the core handlers above */
};

/* Reset handler implementation */
void Reset_Handler(void) {
    uint32_t *src, *dest;

    /* Copy initialized data from flash to RAM */
    src = &_sidata;
    dest = &_sdata;
    while (dest < &_edata) {
        *dest++ = *src++;
    }

    /* Zero-initialize BSS section */
    dest = &_sbss;
    while (dest < &_ebss) {
        *dest++ = 0;
    }

    /* Enable FPU (Cortex-M7 has hardware FPU) */
    /* CPACR = 0xE000ED88 */
    *(volatile uint32_t *)0xE000ED88 |= ((3UL << 10*2) | (3UL << 11*2));

    /* Initialize DWT cycle counter for profiling */
    /* Enable DWT and ITM blocks */
    *(volatile uint32_t *)0xE000EDFC |= (1 << 24);  /* Enable TRCENA */
    *(volatile uint32_t *)0xE0001000 |= 1;          /* Enable cycle counter */
    *(volatile uint32_t *)0xE0001004 = 0;           /* Reset cycle counter */

    /* Call main function */
    main();

    /* Infinite loop if main returns */
    while (1) {
        __asm__ volatile("nop");
    }
}

/* Default handler for unused interrupts */
void Default_Handler(void) {
    /* Hang in infinite loop */
    while (1) {
        __asm__ volatile("nop");
    }
}

/* Provide weak definitions for newlib stubs */
void _exit(int status) {
    (void)status;
    while (1);
}

int _write(int file, char *ptr, int len) {
    /* For Renode, we can write to UART or just return success */
    (void)file;
    (void)ptr;
    return len;  /* Pretend we wrote everything */
}

int _read(int file, char *ptr, int len) {
    (void)file;
    (void)ptr;
    (void)len;
    return 0;
}

int _close(int file) {
    (void)file;
    return -1;
}

int _lseek(int file, int offset, int whence) {
    (void)file;
    (void)offset;
    (void)whence;
    return 0;
}

int _fstat(int file, void *st) {
    (void)file;
    (void)st;
    return 0;
}

int _isatty(int file) {
    (void)file;
    return 1;
}

void *_sbrk(int incr) {
    extern char _end;
    static char *heap_end = 0;
    char *prev_heap_end;

    if (heap_end == 0) {
        heap_end = &_end;
    }
    prev_heap_end = heap_end;
    heap_end += incr;
    return (void *)prev_heap_end;
}

int _getpid(void) {
    return 1;
}

int _kill(int pid, int sig) {
    (void)pid;
    (void)sig;
    return -1;
}
