/** A dependency-free, bounded exponential backoff policy. */
public final class RetryPolicy {
    private RetryPolicy() {}

    public static long backoffMillis(int attempt, long baseMillis, long maxMillis) {
        if (attempt < 0 || baseMillis < 0 || maxMillis < 0 || baseMillis > maxMillis) {
            throw new IllegalArgumentException("invalid retry bounds");
        }
        long value = baseMillis;
        for (int i = 0; i < attempt && value < maxMillis; i++) {
            if (value > maxMillis / 2) {
                value = maxMillis;
            } else {
                value *= 2;
            }
        }
        return Math.min(value, maxMillis);
    }

    public static void main(String[] args) {
        System.out.println(backoffMillis(4, 100, 1000));
    }
}

