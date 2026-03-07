
# Makefile for CIFAR-10 Embedded Inference
# Target: ARM Cortex-M7 (STM32H7)

# Toolchain
CC = arm-none-eabi-gcc
OBJCOPY = arm-none-eabi-objcopy
SIZE = arm-none-eabi-size

# Compiler flags for Cortex-M7
CFLAGS = -mcpu=cortex-m7 \
         -mthumb \
         -mfloat-abi=hard \
         -mfpu=fpv5-d16 \
         -O3 \
         -Wall \
         -ffunction-sections \
         -fdata-sections \
         -g

# Linker flags
LDFLAGS = -mcpu=cortex-m7 \
          -mthumb \
          -mfloat-abi=hard \
          -mfpu=fpv5-d16 \
          -specs=nosys.specs \
          -T stm32h7.ld \
          -Wl,--gc-sections \
          -Wl,--print-memory-usage

# Source files
SRCS = startup.c main.c cifar10_model.c

# Object files
OBJS = $(SRCS:.c=.o)

# Output
TARGET = cifar10_demo

# Build rules
all: $(TARGET).elf $(TARGET).bin

$(TARGET).elf: $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^
	$(SIZE) $@

$(TARGET).bin: $(TARGET).elf
	$(OBJCOPY) -O binary $< $@

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJS) $(TARGET).elf $(TARGET).bin

# For x86 testing (simulation without Renode)
test_x86:
	gcc -O2 -o cifar10_test_x86 main.c cifar10_model.c
	./cifar10_test_x86

.PHONY: all clean test_x86
