.RECIPEPREFIX := >
TARGET = transpose_cep
CC = riscv64-unknown-elf-gcc
OBJDUMP = riscv64-unknown-elf-objdump

DEFS ?=

CFLAGS = -gdwarf-2 -O2 \
  -march=rv64gc -mabi=lp64d -mcmodel=medany \
  -nostdlib -static -fno-tree-loop-distribute-patterns \
  -T../common/test.ld -I../common $(DEFS)

all: $(TARGET)

$(TARGET): transpose_cep.c
>$(CC) -o $(TARGET) $(CFLAGS) transpose_cep.c ../common/crt.S ../common/syscalls.c
>$(OBJDUMP) -S -d $(TARGET) > $(TARGET).objdump

clean:
>rm -f $(TARGET) $(TARGET).objdump* $(TARGET).memfile
