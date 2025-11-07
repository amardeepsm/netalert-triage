.PHONY: setup test report clean

# Detect OS and choose activate path dynamically
ifeq ($(OS),Windows_NT)
	ACTIVATE=.venv\Scripts\activate
else
	ACTIVATE=.venv/bin/activate
endif

# 🧰 Create virtual environment and install dependencies
setup:
	@echo "📦 Setting up environment..."
	python -m venv .venv
	@echo "🐍 Activating venv and installing dependencies..."
	$(ACTIVATE) && pip install -r requirements.txt && pip install -e . && pip install pytest
	@echo "✅ Setup complete."

# 🧪 Run tests
test:
	@echo "🧪 Running unit tests..."
	$(ACTIVATE) && pytest -q

# 🧾 Generate demo triage report
report:
	@echo "🧾 Generating triage report..."
	$(ACTIVATE) && mkdir -p artifacts && python -m netalert.run --alerts sample_data/sample_alerts.json --logs sample_data/sample_gateway_logs.json --out artifacts/report.md
	@echo "✅ Report generated at artifacts/report.md"

# 🧹 Clean artifacts and cache
clean:
	@echo "🧹 Cleaning artifacts..."
	@if exist artifacts (rmdir /s /q artifacts) || rm -rf artifacts
	@if exist .pytest_cache (rmdir /s /q .pytest_cache) || rm -rf .pytest_cache
	@echo "✅ Clean complete."
