class HighPassFilter {
private:
    float value = 0;
public:
    HighPassFilter() { }

    float filter(float val, float K) {
        value = K * (value + val - value);
        return value;
    }
};
