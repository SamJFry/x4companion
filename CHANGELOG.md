# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[0.1.0]
### Added
- Added Sector templates. These map to datasets, this table contains all sectors available in a dataset.
- Added React frontend with material UI. This includes:
  - Sign in and authentication.
  - Save management.
  - basic page layout for all future pages.
- Added API endpoints for Sector Templates.

### Changed
- Sectors now map to sector templates, previously each sector was unique within a save game.
- Save games must be associated to a dataset.

## [Unreleased]
## Added
- Sector Templates now have a Sunlight Percent field.

### Changed
- Sector Templates no longer give their Dataset ID in GET responses, since the user already has
to give this detail in the URL.
- Sector Templates no longer require the Dataset ID when creating them via POST requests.

## [0.0.1] - 2024-12-20

### Added
- Added API GET, POST and DELETE endpoints and supporting DB tables for:
  - Save Games
  - Datasets
  - Sectors
  - Stations
  - Habitat Modules
  - Habitats
- Added Standardised pagination to all API endpoints.
- Defined generic post, get, bulk get and delete responses to be used by all endpoints.
- Basic Swagger docs for the API.