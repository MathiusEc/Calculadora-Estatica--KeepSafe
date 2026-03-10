# Keep Safe Operation - Mix Calculator

## Project Name
Keep Safe Operation - Mix Calculator

## Project Status
**Published and in production.**
This repository is for documentation and backup purposes only. The application is fully deployed and operational.

## Technologies Used
- Streamlit (Web Application Framework)
- Python 3.8+
- Pandas (Data Processing)
- Pillow (Image Processing)

## Software Architecture — Domain-Driven Design (DDD)

This project follows the **Domain-Driven Design (DDD)** architecture pattern, organizing the codebase into four clearly separated layers:

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    app.py (Entry Point)                      │
│              Orchestrator - No business logic                │
└──────────────┬─────────────┬────────────────┬───────────────┘
               │             │                │
    ┌──────────▼──────┐ ┌────▼────────┐ ┌─────▼──────────────┐
    │  Presentation   │ │ Application │ │  Infrastructure    │
    │  (UI/Streamlit) │ │ (Use Cases) │ │  (Repositories)    │
    └────────┬────────┘ └──────┬──────┘ └─────┬──────────────┘
             │                 │               │
             │          ┌──────▼──────┐        │
             └──────────► Domain      ◄────────┘
                        │ (Core Logic)│
                        └─────────────┘
```

### Layer Details

| Layer | Directory | Responsibility |
|-------|-----------|----------------|
| **Domain** | `src/domain/` | Core business logic, entities, value objects, domain services. No dependencies on external frameworks. |
| **Application** | `src/application/` | Use cases that orchestrate domain logic. Contains validators and calculation workflows. |
| **Infrastructure** | `src/infrastructure/` | Data access via repositories. Provides crop and product data to the application. |
| **Presentation** | `src/presentation/` | Streamlit UI components. Handles all visual rendering and user interaction. |

## Repository Structure
```
.
├── app.py                              # Entry point / Orchestrator (DDD)
├── DEPLOYMENT.md                       # Deployment notes
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
├── styles2.css                         # Main styles
├── styles2_backup.css                  # Styles backup
├── img/                                # Images and assets
│   ├── KEEP SAFE LOGO-01.png
│   └── icons/
│       └── browserconfig.xml
└── src/                                # DDD Source Code
    ├── domain/                         # DOMAIN LAYER
    │   ├── entities/
    │   │   ├── crop.py                 # Crop entity (parameters per crop)
    │   │   ├── product.py              # Product & MixtureProduct entities
    │   │   ├── mixture.py              # Mixture aggregate + MixtureResult VO
    │   │   └── flight_operation.py     # FlightOperation value object
    │   └── services/
    │       ├── mixture_calculator.py   # Mixture calculation domain service
    │       └── flight_calculator.py    # Flight operation domain service
    ├── application/                    # APPLICATION LAYER
    │   ├── use_cases/
    │   │   ├── calculate_mixture.py    # Mixture calculation use case
    │   │   └── calculate_flight.py     # Flight calculation use case
    │   └── validators/
    │       └── __init__.py             # MixtureValidator + ValidationResult
    ├── infrastructure/                 # INFRASTRUCTURE LAYER
    │   └── repositories/
    │       ├── crop_repository.py      # Crop data repository
    │       └── product_repository.py   # Product catalog repository
    └── presentation/                   # PRESENTATION LAYER
        ├── components/
        │   ├── header.py               # Header + logo + description
        │   ├── crop_form.py            # General data form (crop, hectares, date)
        │   ├── mixture_form.py         # Product mixture configuration form
        │   ├── results_display.py      # Mixture calculation results
        │   ├── flight_recommendations.py  # Technical flight recommendations
        │   └── flight_operations.py    # Operational flight calculations
        └── utils/
            └── __init__.py             # CSS loader utility
```

## DDD Layer Descriptions

### Domain Layer (`src/domain/`)
The core of the application. Contains all business rules independent of any framework:
- **Entities**: `Crop`, `Product`, `MixtureProduct` — represent the core business objects
- **Value Objects**: `MixtureResult`, `FlightOperation` — immutable data containers for calculation results
- **Aggregates**: `Mixture` — encapsulates the mixing logic and ensures consistency
- **Domain Services**: `MixtureCalculatorService`, `FlightCalculatorService` — stateless services for complex calculations

### Application Layer (`src/application/`)
Orchestrates domain logic into complete workflows:
- **Use Cases**: `CalculateMixtureUseCase`, `CalculateFlightUseCase` — coordinate validation and calculation
- **Validators**: `MixtureValidator` — validates business rules (no duplicate products/orders)

### Infrastructure Layer (`src/infrastructure/`)
Provides data access:
- **Repositories**: `CropRepository`, `ProductRepository` — supply crop parameters and product catalogs

### Presentation Layer (`src/presentation/`)
Streamlit-specific UI components:
- **Components**: Modular UI pieces (header, forms, results display, recommendations)
- **Utils**: CSS loader for custom styling

## Project Description
This tool calculates mixtures and operational parameters for agricultural drones (DJI Agras T50). It supports the following crops:
- Banana
- Corn
- Rice
- Cocoa

Features include:
- Automatic calculation of mixtures per hectare and totals
- Customizable mixing order for correct application
- Technical flight and application parameters for DJI Agras T50
- Resource estimation: required flights, time, and total solution
- Data validation to prevent mixing errors
- Intuitive, responsive interface
- Technical recommendations specific to each crop

## Author

Project developed by MathiusEc for Keep Safe S.A.S.

## License
Copyright © 2026 Keep Safe S.A.S. All rights reserved. This repository and all its contents are the exclusive property of Keep Safe S.A.S. Unauthorized reproduction, distribution, or use of any part of this project is strictly prohibited without prior written consent from Keep Safe S.A.S.
