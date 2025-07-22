# Makefile for Twelve Labs Single Asset Process CLI
# Provides convenient commands for building, testing, and managing the project

.PHONY: help build clean test install dev-setup lint format check-all deps demo info commands

# Default target
help:
	@echo "Twelve Labs Single Asset Process CLI - Makefile"
	@echo ""
	@echo "Available commands:"
	@echo "  build          - Build wheel and executable using uv"
	@echo "  clean          - Clean build artifacts and temporary files"
	@echo "  test           - Run all tests"
	@echo "  test-search    - Test search functionality"
	@echo "  test-metadata  - Test metadata generation"
	@echo "  test-eval      - Test evaluation logic"
	@echo "  install        - Install the package in development mode"
	@echo "  dev-setup      - Set up development environment"
	@echo "  deps           - Install dependencies"
	@echo "  lint           - Run linting checks"
	@echo "  format         - Format code with black"
	@echo "  check-all      - Run all checks (lint, format, test)"
	@echo "  demo           - Run quick demo"
	@echo "  info           - Show project information"
	@echo "  commands       - Show all available commands"
	@echo "  help           - Show this help message"

# Build wheel and executable
build:
	@echo "🚀 Building Twelve Labs Single Asset Process CLI..."
	@./build_with_uv.py

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info/
	@rm -rf __pycache__/
	@rm -rf .pytest_cache/
	@rm -rf test_results/
	@rm -rf batch_output/
	@rm -rf search_output/
	@rm -rf output/
	@rm -rf spec_demo_output/
	@rm -rf asset_processing_demo/
	@rm -rf comprehensive_tests/
	@rm -rf demo_output/
	@rm -f twelve-labs-sa
	@rm -f *.json
	@rm -f *.yaml
	@rm -f *.csv
	@echo "✅ Clean completed"

# Run all tests
test:
	@echo "🧪 Running all tests..."
	@uv run python -m twelve_labs_sa.cli test all --output-dir test_results
	@echo "✅ All tests completed"

# Test search functionality
test-search:
	@echo "🔍 Testing search functionality..."
	@uv run python -m twelve_labs_sa.cli test search

# Test metadata generation
test-metadata:
	@echo "📝 Testing metadata generation..."
	@uv run python -m twelve_labs_sa.cli test metadata

# Test evaluation logic
test-eval:
	@echo "📊 Testing evaluation logic..."
	@uv run python -m twelve_labs_sa.cli test eval

# Install package in development mode
install:
	@echo "📦 Installing package in development mode..."
	@uv pip install -e .
	@echo "✅ Installation completed"

# Set up development environment
dev-setup:
	@echo "🔧 Setting up development environment..."
	@uv sync
	@uv pip install -e .
	@echo "✅ Development setup completed"

# Install dependencies
deps:
	@echo "📦 Installing dependencies..."
	@uv sync
	@echo "✅ Dependencies installed"

# Run linting checks
lint:
	@echo "🔍 Running linting checks..."
	@uv run ruff check .
	@echo "✅ Linting completed"

# Format code
format:
	@echo "🎨 Formatting code..."
	@uv run black .
	@uv run ruff format .
	@echo "✅ Code formatting completed"

# Run all checks
check-all: lint format test
	@echo "✅ All checks completed"

# Quick demo
demo:
	@echo "🎬 Running quick demo..."
	@uv run python -m twelve_labs_sa.cli spec compliance-demo --output-dir demo_output
	@echo "✅ Demo completed"

# Show CLI help
help-cli:
	@echo "📋 CLI Help:"
	@uv run python -m twelve_labs_sa.cli --help

# Show test commands help
help-test:
	@echo "🧪 Test Commands Help:"
	@uv run python -m twelve_labs_sa.cli test --help

# Build and test
build-test: build test
	@echo "✅ Build and test completed"

# Development workflow
dev: clean deps build-test
	@echo "✅ Development workflow completed"

# Production build
prod: clean build
	@echo "✅ Production build completed"

# Show project info
info:
	@echo "📊 Project Information:"
	@echo "  Name: Twelve Labs Single Asset Process CLI"
	@echo "  Version: 0.1.0"
	@echo "  Python: $(shell python --version)"
	@echo "  UV: $(shell uv --version)"
	@echo "  Build Status: $(shell if [ -f ./twelve-labs-sa ]; then echo "✅ Built"; else echo "❌ Not built"; fi)"

# Show all available commands
commands:
	@echo "📋 Available Commands:"
	@echo "  make help          - Show this help"
	@echo "  make build         - Build wheel and executable"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make test          - Run all tests"
	@echo "  make test-search   - Test search functionality"
	@echo "  make test-metadata - Test metadata generation"
	@echo "  make test-eval     - Test evaluation logic"
	@echo "  make demo          - Run quick demo"
	@echo "  make deps          - Install dependencies"
	@echo "  make lint          - Run linting"
	@echo "  make format        - Format code"
	@echo "  make check-all     - Run all checks"
	@echo "  make dev           - Development workflow"
	@echo "  make prod          - Production build"
	@echo "  make info          - Show project info"
	@echo "  make commands      - Show this command list" 