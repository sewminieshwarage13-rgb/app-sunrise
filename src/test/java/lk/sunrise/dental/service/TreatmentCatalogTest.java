package lk.sunrise.dental.service;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class TreatmentCatalogTest {
    @Test
    void addsConsultationFeeToTreatmentFee() {
        assertEquals(new BigDecimal("7500.00"), TreatmentCatalog.totalFor("Dental Filling"));
    }

    @Test
    void consultationOnlyUsesStandardFee() {
        assertEquals(new BigDecimal("1500.00"), TreatmentCatalog.totalFor("Dental Consultation"));
    }

    @Test
    void rejectsUnknownTreatment() {
        assertThrows(IllegalArgumentException.class,
                () -> TreatmentCatalog.totalFor("Unknown Treatment"));
    }

    @Test
    void exposesExpectedTreatmentChoices() {
        assertTrue(TreatmentCatalog.treatmentTypes().contains("Root Canal Treatment"));
    }
}

