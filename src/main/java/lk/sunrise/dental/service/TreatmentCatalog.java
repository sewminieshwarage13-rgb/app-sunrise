package lk.sunrise.dental.service;

import java.math.BigDecimal;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;

public final class TreatmentCatalog {
    public static final BigDecimal CONSULTATION_FEE = new BigDecimal("1500.00");
    private static final Map<String, BigDecimal> TREATMENT_FEES;

    static {
        Map<String, BigDecimal> fees = new LinkedHashMap<>();
        fees.put("Dental Consultation", new BigDecimal("0.00"));
        fees.put("Teeth Cleaning", new BigDecimal("4500.00"));
        fees.put("Dental Filling", new BigDecimal("6000.00"));
        fees.put("Tooth Extraction", new BigDecimal("7500.00"));
        fees.put("Root Canal Treatment", new BigDecimal("18000.00"));
        fees.put("Teeth Whitening", new BigDecimal("12000.00"));
        fees.put("Orthodontic Consultation", new BigDecimal("2500.00"));
        TREATMENT_FEES = Collections.unmodifiableMap(fees);
    }

    private TreatmentCatalog() { }

    public static Set<String> treatmentTypes() {
        return TREATMENT_FEES.keySet();
    }

    public static boolean contains(String treatmentType) {
        return TREATMENT_FEES.containsKey(treatmentType);
    }

    public static BigDecimal treatmentFee(String treatmentType) {
        BigDecimal fee = TREATMENT_FEES.get(treatmentType);
        if (fee == null) {
            throw new IllegalArgumentException("Unknown treatment type: " + treatmentType);
        }
        return fee;
    }

    public static BigDecimal totalFor(String treatmentType) {
        return CONSULTATION_FEE.add(treatmentFee(treatmentType));
    }
}

