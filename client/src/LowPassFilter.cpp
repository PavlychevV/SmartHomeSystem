class LowPassFilter {
private:
    float value = 0;
public:
    LowPassFilter() {}

    float filter(float val, float K) {
        value = value * (1 - K) + val * K;
        return value;
    }
};
