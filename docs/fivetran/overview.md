---
name: CrateDB
title: CrateDB
description: Overview about CrateDB Fivetran Destination
hidden: false
---

# CrateDB {% badge text="Partner-Built" /%} {% badge text="Beta" /%} {% availabilityBadge connector="cratedb_destination" /%}

Fivetran supports [CrateDB] as a destination.

CrateDB is a distributed and scalable SQL database for storing and analyzing
massive amounts of data in near real-time, even with complex SQL queries. It
is PostgreSQL-compatible, and based on Lucene.
CrateDB Cloud is a cloud data warehouse with enterprise features.

Support works equally well across all editions:
[CrateDB Cloud], [CrateDB Enterprise], [CrateDB OSS].

This destination is [partner-built](/docs/partner-built-program). For any
questions related to the CrateDB destination and its documentation,
contact [CrateDB Support].

------------------

## Supported deployment models

The CrateDB data warehouse supports the
[SaaS](/deployment-models/saas-deployment),
[Hybrid](/deployment-models/hybrid-deployment), and
[Self-hosted](/docs/deployment-models/self-hosted-deployment)
deployment models.

------------------

## Setup guide

Follow the [step-by-step CrateDB setup guide](/docs/destinations/cratedb/setup-guide)
to connect your CrateDB data warehouse with Fivetran.

------------------

## Type transformation and mapping

The data types in your CrateDB data warehouse follow Fivetran's [standard data type storage](/docs/destinations#datatypes).

We use the following data type conversions:

| Fivetran Data Type | Destination Data Type | Notes |
|--------------------|-----------------------| - |
| BOOLEAN            | BOOLEAN               | |
| SHORT              | SMALLINT              | |
| INT                | INTEGER               | |
| LONG               | BIGINT                | |
| FLOAT              | FLOAT                 | |
| DOUBLE             | DOUBLE                | |
| BIGDECIMAL         | DECIMAL               | |
| LOCALDATE          | TIMESTAMP             | |
| LOCALDATETIME      | TIMESTAMP             | |
| INSTANT            | TIMESTAMP             | |
| STRING             | TEXT                  | |
| XML                | TEXT                  | |
| JSON               | OBJECT                | |
| BINARY             | TEXT                  | |

------------------

## Limitations

- Adding, removing, or modifying primary key columns is not supported.

- Certain schema migration operations will incur a loss of primary key constraints.

  CrateDB does not support creating primary key constraints on non-empty tables,
  nor dropping them or changing their values. To provide schema migration and
  history mode operations, the adapter uses table copy operations that drop primary
  key constraints while they go.

  This will effectively impact the schema migration operations [HISTORY_TO_SOFT_DELETE],
  [SOFT_DELETE_TO_HISTORY], [HISTORY_TO_LIVE], and [LIVE_TO_HISTORY].

- Certain column names are reserved for system purposes, so they will be rejected for users.
  Example: `InvalidColumnNameException["_id" conflicts with system column]`.


[CrateDB]: https://cratedb.com/database
[CrateDB Cloud]: https://cratedb.com/database/editions/cloud
[CrateDB Enterprise]: https://cratedb.com/database/editions/enterprise
[CrateDB OSS]: https://cratedb.com/database/editions/oss
[CrateDB Support]: https://cratedb.com/support

[HISTORY_TO_SOFT_DELETE]: https://github.com/fivetran/fivetran_partner_sdk/blob/main/schema-migration-helper-service.md#history_to_soft_delete
[SOFT_DELETE_TO_HISTORY]: https://github.com/fivetran/fivetran_partner_sdk/blob/main/schema-migration-helper-service.md#soft_delete_to_history
[HISTORY_TO_LIVE]: https://github.com/fivetran/fivetran_partner_sdk/blob/main/schema-migration-helper-service.md#history_to_live
[LIVE_TO_HISTORY]: https://github.com/fivetran/fivetran_partner_sdk/blob/main/schema-migration-helper-service.md#live_to_history
