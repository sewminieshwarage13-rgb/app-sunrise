package lk.sunrise.dental.model;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.Objects;

public final class Appointment {
    private final String appointmentNumber;
    private final String patientName;
    private final String address;
    private final String contactNumber;
    private final String dentistName;
    private final String treatmentType;
    private final AppointmentMode appointmentMode;
    private final LocalDate appointmentDate;
    private final LocalTime appointmentTime;

    public Appointment(String appointmentNumber, String patientName, String address,
                       String contactNumber, String dentistName, String treatmentType,
                       AppointmentMode appointmentMode, LocalDate appointmentDate, LocalTime appointmentTime) {
        this.appointmentNumber = Objects.requireNonNull(appointmentNumber);
        this.patientName = Objects.requireNonNull(patientName);
        this.address = Objects.requireNonNull(address);
        this.contactNumber = Objects.requireNonNull(contactNumber);
        this.dentistName = Objects.requireNonNull(dentistName);
        this.treatmentType = Objects.requireNonNull(treatmentType);
        this.appointmentMode = Objects.requireNonNull(appointmentMode);
        this.appointmentDate = Objects.requireNonNull(appointmentDate);
        this.appointmentTime = Objects.requireNonNull(appointmentTime).withSecond(0).withNano(0);
    }

    public String getAppointmentNumber() { return appointmentNumber; }
    public String getPatientName() { return patientName; }
    public String getAddress() { return address; }
    public String getContactNumber() { return contactNumber; }
    public String getDentistName() { return dentistName; }
    public String getTreatmentType() { return treatmentType; }
    public AppointmentMode getAppointmentMode() { return appointmentMode; }
    public LocalDate getAppointmentDate() { return appointmentDate; }
    public LocalTime getAppointmentTime() { return appointmentTime; }
}
