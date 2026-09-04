import org.junit.platform.engine.TestExecutionResult;
import org.junit.platform.engine.discovery.DiscoverySelectors;
import org.junit.platform.launcher.Launcher;
import org.junit.platform.launcher.LauncherDiscoveryRequest;
import org.junit.platform.launcher.TestExecutionListener;
import org.junit.platform.launcher.TestIdentifier;
import org.junit.platform.launcher.core.LauncherDiscoveryRequestBuilder;
import org.junit.platform.launcher.core.LauncherFactory;

import java.util.concurrent.atomic.AtomicInteger;

public final class TestSuiteRunner {
    public static void main(String[] args) {
        AtomicInteger passed = new AtomicInteger();
        AtomicInteger failed = new AtomicInteger();
        LauncherDiscoveryRequest request = LauncherDiscoveryRequestBuilder.request()
                .selectors(DiscoverySelectors.selectPackage("lk.sunrise.dental"))
                .build();
        Launcher launcher = LauncherFactory.create();
        launcher.registerTestExecutionListeners(new TestExecutionListener() {
            @Override
            public void executionFinished(TestIdentifier identifier, TestExecutionResult result) {
                if (!identifier.isTest()) {
                    return;
                }
                if (result.getStatus() == TestExecutionResult.Status.SUCCESSFUL) {
                    passed.incrementAndGet();
                    System.out.println("PASS | " + identifier.getDisplayName());
                } else {
                    failed.incrementAndGet();
                    System.out.println("FAIL | " + identifier.getDisplayName());
                    result.getThrowable().ifPresent(error -> System.out.println("       " + error.getMessage()));
                }
            }
        });
        launcher.execute(request);
        System.out.printf("SUMMARY | Passed: %d | Failed: %d%n", passed.get(), failed.get());
        if (failed.get() > 0) {
            System.exit(1);
        }
    }
}
