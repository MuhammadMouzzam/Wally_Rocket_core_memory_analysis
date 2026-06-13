#include <stdio.h>
#include <stdint.h>

#ifndef ROWS
#define ROWS 256
#endif

#ifndef COLS
#define COLS 64
#endif

#ifndef BLOCK_SIZE
#define BLOCK_SIZE 8
#endif

#ifndef MODE
#define MODE 0   // 0 = naive, 1 = blocked
#endif

static uint64_t src[ROWS][COLS];
static uint64_t dst[COLS][ROWS];
volatile uint64_t final_checksum = 0;

static inline uint64_t read_cycle(void) {
    uint64_t x;
    asm volatile ("rdcycle %0" : "=r"(x));
    return x;
}

static inline uint64_t read_instret(void) {
    uint64_t x;
    asm volatile ("rdinstret %0" : "=r"(x));
    return x;
}

static inline int min_int(int a, int b) {
    return (a < b) ? a : b;
}

__attribute__((noinline))
void init_src(void) {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            src[i][j] = (uint64_t)(i * COLS + j + 1);
        }
    }
}

__attribute__((noinline))
void clear_dst(void) {
    for (int i = 0; i < COLS; i++) {
        for (int j = 0; j < ROWS; j++) {
            dst[i][j] = 0;
        }
    }
}

__attribute__((noinline))
void transpose_naive(void) {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            dst[j][i] = src[i][j];
        }
    }
}

__attribute__((noinline))
void transpose_blocked(void) {
    for (int ii = 0; ii < ROWS; ii += BLOCK_SIZE) {
        for (int jj = 0; jj < COLS; jj += BLOCK_SIZE) {
            int i_max = min_int(ii + BLOCK_SIZE, ROWS);
            int j_max = min_int(jj + BLOCK_SIZE, COLS);

            for (int i = ii; i < i_max; i++) {
                for (int j = jj; j < j_max; j++) {
                    dst[j][i] = src[i][j];
                }
            }
        }
    }
}

__attribute__((noinline))
uint64_t checksum_dst(void) {
    uint64_t sum = 0;
    for (int i = 0; i < COLS; i++) {
        for (int j = 0; j < ROWS; j++) {
            sum += dst[i][j];
        }
    }
    return sum;
}

int main(void) {
    init_src();
    clear_dst();

    uint64_t c0 = read_cycle();
    uint64_t i0 = read_instret();

#if MODE == 0
    transpose_naive();
#else
    transpose_blocked();
#endif

    uint64_t i1 = read_instret();
    uint64_t c1 = read_cycle();

    final_checksum = checksum_dst();

#if MODE == 0
    printf("RESULT,mode=naive,B=0,rows=%d,cols=%d,cycles=%llu,instret=%llu,checksum=%llu\n",
           ROWS, COLS,
           (unsigned long long)(c1 - c0),
           (unsigned long long)(i1 - i0),
           (unsigned long long)final_checksum);
#else
    printf("RESULT,mode=blocked,B=%d,rows=%d,cols=%d,cycles=%llu,instret=%llu,checksum=%llu\n",
           BLOCK_SIZE, ROWS, COLS,
           (unsigned long long)(c1 - c0),
           (unsigned long long)(i1 - i0),
           (unsigned long long)final_checksum);
#endif

    return 0;
}
