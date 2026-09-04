package lk.sunrise.dental.service;

import lk.sunrise.dental.model.Appointment;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.LinkedHashMap;
import java.util.Map;

public final class AppointmentValidator {
    private static final LocalTime OPENING_TIME = LocalTime.of(8, 0);
    private static final LocalTime CLOSING_TIME = LocalTime.of(18, 0);

    public Map<String, String> validate(Appointment appointment) {
        Map<String, String> errors = new LinkedHashMap<>();

        if (!appointment.getAppointmentNumber().matches("APT-\\d{4,6}")) {
            errors.put("appointmentNumber", "Use the format APT-1001.");
        }
        if (appointment.getPatientName().length() < 2 || appointment.getPatientName().length() > 80) {
            errors.put("patientName", "Patient name must contain 2 to 80 characters.");
        }
        if (appointment.getAddress().length() < 5 || appointment.getAddress().length() > 160) {
            errors.put("address", "Address must contain 5 to 160 characters.");
        }
        if (!appointment.getContactNumber().matches("^(?:\\+94|0)\\d{9}$")) {
            errors.put("contactNumber", "Enter a Sri Lankan number such as 0771234567.");
        }
        if (appointment.getDentistName().isBlank()) {
            errors.put("dentistName", "Select a dentist.");
        }
        if (!TreatmentCatalog.contains(appointment.getTreatmentType())) {
            errors.put("treatmentType", "Select a valid treatment type.");
        }
        if (appointment.getAppointmentDate().isBefore(LocalDate.now())) {
            errors.put("appointmentDate", "Appointment date cannot be in the past.");
        }
        if (appointment.getAppointmentTime().isBefore(OPENING_TIME)
                || appointment.getAppointmentTime().isAfter(CLOSING_TIME)) {
            errors.put("appointmentTime", "Choose a time between 08:00 and 18:00.");
        }
        return errors;
    }
}

