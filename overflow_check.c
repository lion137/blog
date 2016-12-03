#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <gmp.h>


int nlz(unsigned x) {//returns number of leading zeros of unsigned 32 bit int
    unsigned y;
    int n, c;
    n = 32;
    c = 16;
    do {
    y = x >> c; if (y != 0) {n = n - c; x = y;}
    c = c >> 1;
    } while (c != 0);
    return n - x;
}

int nlz_long(unsigned long x) {// number of leading zeroes of 64 bit unsigned int
    unsigned long y;
    long n, c;
    n = 64;
    c = 32;
    do {
    y = x >> c; if (y != 0) {n = n - c; x = y;}
    c = c >> 1;
    } while (c != 0);
    return n - x;
}
int unsigned_long_overflow(unsigned long x, unsigned long y){
	/*
	  Returns 1 if multiplication of  two unsigned 64 bit integers not overflow, zero otherwise.
	  * Analysis simlar to 32 bit case.
	 */
	unsigned long z, m, n, t;
	m = nlz_long(x);
	n = nlz_long(y);
	if (m + n <= 62) return 0;
	t = x * (y >> 1);
	if ( (long)t < 0) return 0;
	z = t * 2;
	if (y & 1){
		z = z + x;
		if (z < x) return 0;
	}
	return 1;
}
int unsigned_int_overflow(unsigned x, unsigned y){
	/*
	 * Returns 1 if multiplication of  two unsigned 32 bit integers not overflow, zero otherwise.
	 * 
	 */
	unsigned z, m, n, t;
	m = nlz(x);
	n = nlz(y);
	if (m + n <= 30) return 0; // if sum of number's  number of  trailing zeroes is less than or eq to 30
	t = x*(y >> 1);				// than there is definitely an  overflow, if is bigger or eg to 32 definitely  
	if ((int)t < 0) return 0;   // not overflow. If is eq to 31 it depends from value t = x * floor(y/2), 
	z = t*2;					// t not overflow and if t >= 2 ^ 31 multiplication overflows..
	if (y & 1) {
		z = z + x;
		if (z < x) return 0;
	}
	return 1;
}

int unsigned_long_overflow_bigint(unsigned long x, unsigned long y){
	/*
	  Returns 1 if multiplication of  two unsigned 64 bit integers not overflow, zero otherwise. Bigint testing 
	  * version , slow.
	  * 
	 */
	mpz_t test;
	mpz_init(test);
	mpz_set_ui(test, x * y);
	if(mpz_cmp_ui(test, ULONG_MAX) <= 0) return 1;
	else return 0;
	
}


int main(){
	unsigned long i = 0;
	unsigned long outcome;
	while (i < 1000000000){
		i++;
		if (unsigned_long_overflow(i, i+1))// when compiled with optimization enabled (gcc -O1 -std=c99 overflow_check.c -lgmp)
            outcome = i * (i + 1);                // no difference when line 88 commented or not:
                                                 // time ./a.out -> 0.388 / 0.362
	}
	return 0;
}
