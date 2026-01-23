---
name: Setup Guide
title: CrateDB Setup Guide
description: Setup Guide for CrateDB Fivetran Destination
hidden: false
---

# CrateDB Setup Guide {% badge text="Partner-Built" /%} {% availabilityBadge connector="cratedb_destination" /%}

Follow the setup guide to connect your CrateDB data warehouse to Fivetran.

-----

## Prerequisites

To connect CrateDB as a [Destination] to Fivetran, you need the following:

- Authentication credentials (hostname, username, password) for a CrateDB
  or CrateDB Cloud database cluster.

- A Fivetran role with the [Create Destinations or Manage Destinations] permissions

-----

## Setup instructions

### <span class="step-item">Choose your deployment model</span>

Before setting up your destination, decide which deployment model best suits
your organization's requirements. This destination supports both SaaS,
Hybrid, and Self-Hosted deployment models, offering flexibility to meet diverse compliance
and data governance needs.

See the [Deployment Models documentation] to understand the use cases of each
model and choose the model that aligns with your security and operational
requirements.

### <span class="step-item"> Complete Fivetran configuration </span>

1. Log in to your [Fivetran account].
2. Go to the **Destinations** page and click **Add destination**.
3. Enter a **Destination name** of your choice and then click **Add**.
4. Select **CrateDB** as the destination type.
5. In the destination setup form, enter the **URL** of your database cluster.
6. Enumerate the steps from the destination setup form.
7. List one action per step.
8. Click **Save & Test**.

   Fivetran [tests and validates]
   the database connection. Upon successfully completing the setup tests, you can
   sync your data using Fivetran connectors to the CrateDB destination.


### Setup tests

Fivetran performs the following connection tests:

The Host Connection test checks the host's accessibility and validates the
database credentials you provided in the setup form.
  
> NOTE: The tests may take a couple of minutes to complete.

-----

## Related articles

[<i aria-hidden="true" class="material-icons">description</i> Destination Overview](/docs/destinations/cratedb)

<b> </b>

[<i aria-hidden="true" class="material-icons">assignment</i> Release Notes](/docs/destinations/cratedb/changelog)

<b> </b>

[<i aria-hidden="true" class="material-icons">settings</i> API Destination Configuration](/docs/destinations/cratedb/api-configuration)

<b> </b>

[<i aria-hidden="true" class="material-icons">home</i> Documentation Home](/docs/getting-started)


[Create Destinations or Manage Destinations]: /docs/using-fivetran/fivetran-dashboard/account-settings/role-based-access-control#rbacpermissions
[Deployment Models documentation]: /docs/deployment-models
[Destination]: /docs/using-fivetran/fivetran-dashboard/destination
[Fivetran account]: https://fivetran.com/login
[tests and validates]: /docs/destinations/cratedb/setup-guide#setuptests
