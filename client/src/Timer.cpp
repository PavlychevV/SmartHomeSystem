class Timer {    
public:
    unsigned int lastTime = 0;

    Timer() { }

    bool isTime(unsigned int interval, unsigned int current) {
        if (current - lastTime < interval) return false;

        lastTime = current;
        return true;
    }

    void reset(unsigned int current) {
        lastTime = current;
    }
};
