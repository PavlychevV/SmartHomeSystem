#include <stdint.h>

class Timer {    
    public:
        uint32_t lastTime = 0;

        Timer() { }

        bool isTime(uint32_t interval, uint32_t current) {
            if (current - lastTime < interval) return false;

            lastTime = current;
            return true;
        }
};