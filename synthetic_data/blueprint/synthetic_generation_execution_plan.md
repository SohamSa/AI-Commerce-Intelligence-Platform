# Synthetic Generation Execution Plan

## Purpose

This document defines the full execution order for generating the synthetic data system for the Commerce Intelligence Platform.

It connects everything together from:
- vendor truth
- transaction behavior
- Shopify-like raw source
- Square-like raw source
- staging pipelines
- canonical merge
- scoring and API output

This file is the **control tower** for the synthetic generation layer.

---

# High-Level Goal

Build a fully connected synthetic data system with:

- 2,000 vendors
- 250,000 transactions
- Shopify-like raw source data
- Square-like raw source data
- canonical 20-column business insights dataset
- opportunity score, insight, and action outputs

---

# Core Architectural Principle

We do **not** generate Shopify, Square, and canonical outputs independently.

Instead, the system must follow this dependency chain:

```text
vendor_master
    ↓
transactions
    ↓
shopify_raw + square_raw
    ↓
shopify_staging + square_staging
    ↓
canonical_merge
    ↓
opportunity_score + insight + action
    ↓
FastAPI output / PostgreSQL storage / dashboard