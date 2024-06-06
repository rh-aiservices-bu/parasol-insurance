package org.parasol.ui;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import jakarta.ws.rs.core.Response.Status;

import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.junit.jupiter.api.Test;

import io.quarkus.test.junit.QuarkusTest;
import io.quarkus.test.junit.TestProfile;

import com.microsoft.playwright.BrowserContext;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Response;
import com.microsoft.playwright.assertions.PlaywrightAssertions;
import com.microsoft.playwright.options.AriaRole;
import com.microsoft.playwright.options.LoadState;
import io.quarkiverse.playwright.InjectPlaywright;
import io.quarkiverse.playwright.WithPlaywright;
import io.quarkiverse.quinoa.testing.QuinoaTestProfiles;

@QuarkusTest
@TestProfile(QuinoaTestProfiles.Enable.class)
@WithPlaywright
public class ClaimsListPageTests {
	private static final int NB_CLAIMS = 6;

	@InjectPlaywright
	BrowserContext context;

	@ConfigProperty(name = "quarkus.http.test-port")
  int quarkusPort;

	@Test
	void pageLoads() {
		var page = loadPage();

		PlaywrightAssertions.assertThat(page)
			.hasTitle("Claims List");
	}

	@Test
	void correctTable() {
		var table = getAndVerifyClaimsTable(NB_CLAIMS);
		var tableColumns = table.getByRole(AriaRole.COLUMNHEADER).all();

		assertThat(tableColumns)
			.isNotNull()
			.hasSize(5)
			.extracting(Locator::textContent)
			.containsExactly(
"Claim Number",
				"Category",
				"Client Name",
				"Policy Number",
				"Status"
			);

		var rows = getTableBodyRows(table);
		assertThat(rows)
			.isNotNull()
			.hasSize(NB_CLAIMS);

		var firstRow = rows.get(0).getByRole(AriaRole.GRIDCELL).all();
		assertThat(firstRow)
			.isNotNull()
			.hasSize(5);

		assertThat(firstRow.get(0))
			.isNotNull()
			.extracting(
				Locator::textContent,
				l -> l.getByRole(AriaRole.LINK).getAttribute("href")
			)
			.containsExactly(
				"CLM195501",
				"/ClaimDetail/1".formatted(this.quarkusPort)
			);

		assertThat(firstRow.get(1))
			.isNotNull()
			.extracting(Locator::textContent)
			.isEqualTo("Multiple vehicle");

		assertThat(firstRow.get(2))
			.isNotNull()
			.extracting(Locator::textContent)
			.isEqualTo("Marty McFly");

		assertThat(firstRow.get(3))
			.isNotNull()
			.extracting(Locator::textContent)
			.isEqualTo("AC-987654321");

		assertThat(firstRow.get(4))
			.isNotNull()
			.extracting(Locator::textContent)
			.isEqualTo("Processed");
	}

	private List<Locator> getTableBodyRows(Locator table) {
		// Rowgroup 1 is the header row
		// Rowgroup 2 is the body rows
		var rowGroups = table.getByRole(AriaRole.ROWGROUP).all();
		assertThat(rowGroups)
			.isNotNull()
			.hasSize(2);

		return rowGroups.get(1).getByRole(AriaRole.ROW).all();
	}

	private Locator getAndVerifyClaimsTable(Page page, int expectedNumRows) {
		var table = page.getByRole(AriaRole.GRID);
		assertThat(table).isNotNull();

		var tableBodyRows = getTableBodyRows(table);
		assertThat(tableBodyRows)
			.isNotNull()
			.hasSize(expectedNumRows);

		return table;
	}

	private Locator getAndVerifyClaimsTable(int expectedNumRows) {
		return getAndVerifyClaimsTable(loadPage(), expectedNumRows);
	}

	private Page loadPage() {
		var page = this.context.newPage();
		var response = page.navigate("http://localhost:%d/ClaimsList".formatted(this.quarkusPort));

		assertThat(response)
			.isNotNull()
			.extracting(Response::status)
			.isEqualTo(Status.OK.getStatusCode());

		page.waitForLoadState(LoadState.NETWORKIDLE);

		return page;
	}
}
