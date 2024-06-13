package org.parasol.ui;

import static org.assertj.core.api.Assertions.assertThat;
import static org.awaitility.Awaitility.await;

import java.time.Duration;
import java.util.Optional;

import jakarta.ws.rs.core.Response.Status;

import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.junit.jupiter.api.Test;
import org.parasol.model.Claim;

import io.quarkus.test.junit.QuarkusTest;
import io.quarkus.test.junit.TestProfile;

import com.microsoft.playwright.BrowserContext;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Response;
import com.microsoft.playwright.assertions.PlaywrightAssertions;
import com.microsoft.playwright.options.LoadState;
import io.quarkiverse.playwright.InjectPlaywright;
import io.quarkiverse.playwright.WithPlaywright;
import io.quarkiverse.quinoa.testing.QuinoaTestProfiles;

@QuarkusTest
@TestProfile(QuinoaTestProfiles.Enable.class)
@WithPlaywright
public class ClaimsDetailPageTests {
	@InjectPlaywright
	BrowserContext context;

	@ConfigProperty(name = "quarkus.http.test-port")
  int quarkusPort;

	@Test
	void pageLoads() {
		var claim = Claim.<Claim>findAll().firstResultOptional().orElseThrow(() -> new IllegalArgumentException("Can not find a claim in the database to use for tests"));
		var page = loadPage(claim);

		PlaywrightAssertions.assertThat(page)
			.hasTitle("Claim Detail");

		PlaywrightAssertions.assertThat(page.getByText(claim.claimNumber))
			.isVisible();

		PlaywrightAssertions.assertThat(page.getByText(claim.summary))
			.isVisible();

		PlaywrightAssertions.assertThat(page.getByText(claim.sentiment))
			.isVisible();

		var openChatButton = page.getByLabel("OpenChat");
		PlaywrightAssertions.assertThat(openChatButton)
			.isVisible();

		openChatButton.click();

		PlaywrightAssertions.assertThat(page.getByText("Hi! I am Parasol Assistant. How can I help you today?"))
			.isVisible();

		assertThat(getChatResponseLocator(page).count())
			.isOne();

		var askMeAnythingField = page.getByPlaceholder("Ask me anything...");
		PlaywrightAssertions.assertThat(askMeAnythingField)
			.isVisible();
		askMeAnythingField.fill("Should I approve this claim?");

		var sendQueryButton = page.getByLabel("SendQuery");
		PlaywrightAssertions.assertThat(sendQueryButton)
			.isVisible();
		sendQueryButton.click();

		// Wait for the answer text to have at least one piece of text in the answer
		await()
			.atMost(Duration.ofMinutes(5))
			.until(() -> getChatResponseText(page).isPresent());

		assertThat(getChatResponseText(page))
			.isNotNull()
			.isPresent();

		assertThat(getChatResponseLocator(page).count())
			.isGreaterThanOrEqualTo(2);
	}

	private static Optional<String> getChatResponseText(Page page) {
		return getChatResponseLocator(page).all().stream()
			.map(Locator::textContent)
			.map(String::trim)
			.filter(answer -> !"Hi! I am Parasol Assistant. How can I help you today?".equals(answer))
			.findFirst()
			.filter(s -> !s.isEmpty());
	}

	private static Locator getChatResponseLocator(Page page) {
		return page.locator(".chat-answer-text");
	}

	private Page loadPage(Claim claim) {
		var page = this.context.newPage();
		var response = page.navigate("http://localhost:%d/ClaimDetail/%d".formatted(this.quarkusPort, claim.id));

		assertThat(response)
			.isNotNull()
			.extracting(Response::status)
			.isEqualTo(Status.OK.getStatusCode());

		page.waitForLoadState(LoadState.NETWORKIDLE);

		return page;
	}
}
