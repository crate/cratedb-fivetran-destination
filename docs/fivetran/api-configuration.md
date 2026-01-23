---
name: API Configuration
title: CrateDB API Configuration
description: API Configuration for CrateDB Fivetran Destination
hidden: false
---

# CrateDB API Configuration

## Request

```text
POST https://api.fivetran.com/v1/destinations
```

```json
{
  "group_id": "group_id",
  "service": "big_query",
  "region": "GCP_US_WEST1",
  "time_zone_offset": "+3",
  "trust_certificates": true,
  "trust_fingerprints": true,
  "run_setup_tests": true,
  "daylight_saving_time_enabled": true,
  "hybrid_deployment_agent_id": "hybrid_deployment_agent_id",
  "private_link_id": "private_link_id",
  "networking_method": "Directly",
  "proxy_agent_id": "proxy_agent_id",
  "config": {
    "url": "crate://admin:password@testcluster.cratedb.net:4200/?ssl=true"
  }
}
```

## Config parameters

| Name  | Description                                                   | 
|-------|---------------------------------------------------------------|
| url   | The database connection URL to your CrateDB database cluster. |

The database connection URL needs to be in SQLAlchemy format.
Example: `crate://admin:password@testcluster.cratedb.net:4200/?ssl=true`
