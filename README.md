## data generation

### ✅ what’s been built

- **end-to-end fintech data generator** — simulates crypto, gold, fraud, and user data.
- **real + simulated data sources** — integrates apis and random event generation.
- **kafka-based streaming pipeline** — real-time producer → broker → consumer setup.
- **containerized infra** — official apache kafka (kraft), python producer & consumer in docker.
- **data persistence layer (bronze)** — consumer writes streamed data into partitioned parquet files.
- **fully functional EL part of ELT pipeline** — extract + load complete and verified.

---

### 🧩 what’s left

- **T (transform)** — dbt/spark models to clean, join, and aggregate parquet data.
- **serving layer** — fastapi or streamlit dashboards for analytics.
- **observability** — prometheus/grafana metrics, lag tracking.
- **optional future** — cdc sync (debezium), feature store for ml features.

```bash

data_generation/
├── src/
│   ├── data_sources/
│   │   ├── crypto_exchanges/
│   │   │   ├── binance_client.py
│   │   │   ├── coinbase_client.py
│   │   │   └── coin_gecko_client.py
│   │   ├── metals/
│   │   │   ├── gold_api.py
│   │   │   └── silver_api.py
│   │   └── financial_apis/
│   │       ├── alpha_vantage.py
│   │       └── financial_modeling.py
│   ├── generators/
│   │   ├── users/
│   │   │   ├── user_generator.py
│   │   │   └── kyc_generator.py
│   │   ├── transactions/
│   │   │   ├── crypto_trader.py
│   │   │   ├── gold_trader.py
│   │   │   └── portfolio_manager.py
│   │   └── fraud/
│   │       ├── pattern_detector.py
│   │       └── anomaly_generator.py
│   ├── models/
│   │   ├── real_time/
│   │   │   ├── market_data.py
│   │   │   └── live_prices.py
│   │   ├── simulated/
│   │   │   ├── user_profiles.py
│   │   │   └── transaction_events.py
│   │   └── hybrid/
│   │       ├── enriched_transaction.py
│   │       └── trading_session.py
│   ├── producers/
│   │   ├── kafka_producer.py
│   │   ├── topic_manager.py
│   │   └── schema_registry.py
│   ├── utils/
│   │   ├── logger.py
│   │   ├── error_handler.py
│   │   └── metrics.py
│   ├── config/
│   │   ├── real_apis.yaml
│   │   ├── kafka_config.yaml
│   │   └── simulation_rules.yaml
│   └── orchestration/
│       ├── data_orchestrator.py
│       ├── rate_controller.py
│       └── health_monitor.py
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
│   ├── architecture.md
│   └── runbook.md
├── infra/
│   ├── docker-compose.yml
│   └── kafka-setup/
└── scripts/
    ├── start_generator.py
    └── monitor_apis.py

```

---

> export PYTHONPATH="$PWD"

> find . | grep -E "(/**pycache**$|\.pyc$|\.pyo$)" | xargs rm -rf

> find . \( -name '**pycache**' -o -name '_.pyc' -o -name '_.pyo' \) -print -exec rm -rf {} +
