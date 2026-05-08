#include "defect_detector.h"
#include <stddef.h>
#include <stdio.h>

int main()
{
    int * defects = detectar("images/01.png", NULL);

    printf("["); 
    for (size_t i = 0; i < defects[0] * 5 + 1; i++) {
        if (i > 0) {
            printf(", ");
        }
        printf("%d",defects[i]);
    }
    printf("]\n"); 

    free(defects);

    return 0;
}