package lk.sunrise.dental.service;

import lk.sunrise.dental.model.Appointment;
import lk.sunrise.dental.model.AppointmentMode;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AppointmentValidatorTest {
    private final AppointmentValidator validator = new AppointmentValidator();

    @Test
    void acceptsCompleteFutureAppointment() {
        assertTrue(validator.validate(validAppointment()).isEmpty());
    }

    @Test
    void rejectsInvalidReferenceAndPhoneNumber() {
        Appointment invalid = new Appointment("1001", "Asha Silva", "12 Palm Road, Colombo",
                "123", "Dr. Amaya Perera", "Teeth Cleaning",
                AppointmentMode.PHYSICAL, LocalDate.now().plusDays(1), LocalTime.of(10, 0));

        Map<String, String> errors = validator.validate(invalid);

        assertTrue(errors.containsKey("appointmentNumber"));
        assertTrue(errors.containsKey("contactNumber"));
    }

    @Test
    void rejectsAppointmentOutsideClinicHours() {
        Appointment invalid = new Appointment("APT-1001", "Asha Silva", "12 Palm Road, Colombo",
                "0771234567", "Dr. Amaya Perera", "Teeth Cleaning",
                AppointmentMode.PHYSICAL, LocalDate.now().plusDays(1), LocalTime.of(19, 0));

        assertFalse(validator.validate(invalid).isEmpty());
        assertTrue(validator.validate(invalid).containsKey("appointmentTime"));
    }

    private Appointment validAppointment() {
        return new Appointment("APT-1001", "Asha Silva", "12 Palm Road, Colombo",
                "0771234567", "Dr. Amaya Perera", "Teeth Cleaning",
                AppointmentMode.PHYSICAL, LocalDate.now().plusDays(1), LocalTime.of(10, 0));
    }
}
