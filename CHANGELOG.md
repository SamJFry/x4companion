# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[Unreleased]
### Added
- Added Sector templates. These map to datasets, this table contains all sectors available in a dataset.
- Added React frontend with material UI. This includes:
  - Sign in and authentication.
  - Save management.
  - basic page layout for all future pages.

### Changed
- Sectors now map to sector templates, previously each sector was unique within a save game.

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