# Data Dictionary

This file defines the columns the pipeline adds to the raw CRMLS schema. Source MLS fields such as `ClosePrice`, `LivingArea` and `DaysOnMarket` follow the [RESO Data Dictionary](https://www.reso.org/data-dictionary/) standard.

← [Back to README](../README.md)

---

## Enrichment Columns

| Column | Type | Stage | Description |
|---|---|---|---|
| `year_month` | period (`YYYY-MM`) | 2 | Join key. Uses `CloseDate` for sold data and `ListingContractDate` for listing data |
| `rate_30yr_fixed` | float (%) | 2 | Monthly average of the Freddie Mac 30-year fixed mortgage rate (FRED `MORTGAGE30US`) |
| `UnifiedSchoolDistrict` | string | 5 | Name of the California unified school district that contains the property. Null if the property is outside every unified district |

## Engineered Features

All of these are created in Stage 4.

| Column | Type | Formula / Definition |
|---|---|---|
| `Price Ratio` | float | `ClosePrice / OriginalListPrice` |
| `Close to Original List Ratio` | float | `ClosePrice / OriginalListPrice` |
| `Price Per Sq Ft` | float | `ClosePrice / LivingArea` |
| `Days On Market` | int | Copy of `DaysOnMarket` with a display-friendly name |
| `Listing to Contract Days` | timedelta | `PurchaseContractDate − ListingContractDate` |
| `Contract to Close Days` | timedelta | `CloseDate − PurchaseContractDate` |
| `close_year` | int | Year of `CloseDate` |
| `close_month` | int | Month (1–12) of `CloseDate` |
| `close_yrmo` | string | `CloseDate` formatted as `YYYY-MM` |

## Data-Quality Flags

All flags are boolean, and `True` means the row failed the check. They are added in Stage 3. The rows are flagged and kept, not dropped.

### Value validity

| Flag | True when |
|---|---|
| `invalid_closeprice_flag` | `ClosePrice <= 0` |
| `invalid_livingarea_flag` | `LivingArea <= 0` |
| `invalid_days_flag` | `DaysOnMarket < 0` |
| `invalid_beds_flag` | `BedroomsTotal < 0` |
| `invalid_baths_flag` | `BathroomsTotalInteger < 0` |

### Timeline consistency

| Flag | True when |
|---|---|
| `listing_after_close_flag` | `ListingContractDate > CloseDate` |
| `purchase_after_close_flag` | `PurchaseContractDate > CloseDate` |
| `negative_timeline_flag` | `PurchaseContractDate < ListingContractDate` |

### Geographic validity

| Flag | True when |
|---|---|
| `missing_coords_flag` | `Latitude` or `Longitude` is null |
| `zero_coords_flag` | `Latitude == 0` or `Longitude == 0` |
| `invalid_longitude_flag` | `Longitude > 0`, which is impossible for California (western hemisphere) |
| `implausible_coords_flag` | The point is outside the California bounding box (lat 32–42, lon −124 to −114) |

## Outlier Flags

These are added in Stage 6. Each one is `True` when the value is outside the Tukey fences `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]`.

| Flag | Field |
|---|---|
| `ClosePrice_outliers_flag` | `ClosePrice` |
| `LivingArea_outliers_flag` | `LivingArea` |
| `DaysOnMarket_outliers_flag` | `DaysOnMarket` |

Rows where any outlier flag is `True` are left out of `final_*_dataset.csv`. They are kept in `final_flagged_*_dataset.csv`.

## Removed Columns

These agent-identifying fields are dropped in Stage 3 to remove personally identifiable information:

`ListAgentFirstName`, `ListAgentLastName`, `ListAgentEmail`, `BuyerAgentFirstName`, `BuyerAgentLastName`, `BuyerAgentMlsId`, `CoListAgentFirstName`, `CoListAgentLastName`, `CoBuyerAgentFirstName`
