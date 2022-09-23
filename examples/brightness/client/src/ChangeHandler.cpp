class ChangeHandler {
    private:
        float lastState = 0;
    public:
        ChangeHandler() { }

        void onChange(float value, void callback(float)) {
            if (value != lastState) {
                lastState = value;
                callback(lastState);
            }

            lastState = value;
        }
};