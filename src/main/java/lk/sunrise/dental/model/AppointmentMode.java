package lk.sunrise.dental.model;

/** The delivery method selected for an appointment. */
public enum AppointmentMode {
    PHYSICAL("Physical clinic visit"),
    ONLINE("Online consultation");

    private final String displayName;

    AppointmentMode(String displayName) {
        this.displayName = displayName;
    }

    public String getDisplayName() {
        return displayName;
    }

    public static AppointmentMode fromValue(String value) {
        if (value == null) {
            throw new IllegalArgumentException("Select an appointment method.");
        }
        try {
            return valueOf(value.trim().toUpperCase());
        } catch (IllegalArgumentException exception) {
            throw new IllegalArgumentException("Select either an online or physical appointment.", exception);
        }
    }
}





