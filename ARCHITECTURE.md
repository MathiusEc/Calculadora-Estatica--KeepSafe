# DDD Architecture - Keep Safe Operation

## Overview

This project implements **Domain-Driven Design (DDD)** architecture with 4 clearly separated layers. Each layer has a specific responsibility, and dependencies always flow **inward** (from outer layers toward the domain).

---

## Layer Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐   │
│   │                    PRESENTATION                          │   │
│   │   src/presentation/                                      │   │
│   │   • Streamlit components (header, forms, tables)         │   │
│   │   • CSS utilities                                        │   │
│   │   • No business logic                                    │   │
│   │                                                          │   │
│   │   ┌──────────────────────────────────────────────────┐   │   │
│   │   │               APPLICATION                        │   │   │
│   │   │   src/application/                               │   │   │
│   │   │   • Use Cases (CalculateMixture, Flight)          │   │   │
│   │   │   • Validators (MixtureValidator)                 │   │   │
│   │   │   • Orchestrates domain logic                     │   │   │
│   │   │                                                  │   │   │
│   │   │   ┌──────────────────────────────────────────┐   │   │   │
│   │   │   │          INFRASTRUCTURE                  │   │   │   │
│   │   │   │   src/infrastructure/                    │   │   │   │
│   │   │   │   • Repositories (Crop, Product)         │   │   │   │
│   │   │   │   • Data access                          │   │   │   │
│   │   │   │                                          │   │   │   │
│   │   │   │   ┌──────────────────────────────────┐   │   │   │   │
│   │   │   │   │           DOMAIN                 │   │   │   │   │
│   │   │   │   │   src/domain/                    │   │   │   │   │
│   │   │   │   │   • Entities (Crop, Product,     │   │   │   │   │
│   │   │   │   │     Mixture, FlightOperation)    │   │   │   │   │
│   │   │   │   │   • Value Objects (MixtureResult,│   │   │   │   │
│   │   │   │   │     FlightOperation)             │   │   │   │   │
│   │   │   │   │   • Domain Services              │   │   │   │   │
│   │   │   │   │     (MixtureCalculator,          │   │   │   │   │
│   │   │   │   │      FlightCalculator)           │   │   │   │   │
│   │   │   │   │   • Pure business rules          │   │   │   │   │
│   │   │   │   └──────────────────────────────────┘   │   │   │   │
│   │   │   └──────────────────────────────────────────┘   │   │   │
│   │   └──────────────────────────────────────────────────┘   │   │
│   └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│   app.py  ←  Entry point / Orchestrator                          │
│              Connects all layers, contains no business logic     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Layer Details

### 1. Domain Layer — `src/domain/`

The innermost and most important layer. Contains all **pure business logic** with no dependency on external frameworks.

#### Entities (`src/domain/entities/`)

| File | Class | Type | Description |
|------|-------|------|-------------|
| `crop.py` | `Crop` | Entity (frozen) | Crop with technical parameters: application rate, speed, height, swath width, droplet type |
| `product.py` | `Product` | Entity (frozen) | Agrochemical product with name |
| `product.py` | `MixtureProduct` | Entity | Product in a mixture: name, amount (L/ha), mixing order |
| `mixture.py` | `Mixture` | Aggregate | Aggregate encapsulating product mixture. Methods: `calcular_por_hectarea()`, `calcular_total()`, `reactivos_superan_volumen()` |
| `mixture.py` | `MixtureResult` | Value Object | Immutable result: suma_reactivos, total_mezcla, agua_necesaria |
| `flight_operation.py` | `FlightOperation` | Value Object (frozen) | Flight calculations: total solution, estimated flights, estimated time |

#### Domain Services (`src/domain/services/`)

| File | Class | Description |
|------|-------|-------------|
| `mixture_calculator.py` | `MixtureCalculatorService` | Creates the `Mixture` aggregate with provided data |
| `flight_calculator.py` | `FlightCalculatorService` | Calculates flight operation parameters (solution, flights, time). Constants: `TANQUE_LITROS=40`, `TIEMPO_VUELO_MIN=10` |

---

### 2. Application Layer — `src/application/`

Contains **use cases** that orchestrate domain logic into complete workflows.

#### Use Cases (`src/application/use_cases/`)

| File | Class | Description |
|------|-------|-------------|
| `calculate_mixture.py` | `CalculateMixtureUseCase` | Validates data → creates mixture → calculates per-ha and total results. Returns `MixtureCalculationResult` |
| `calculate_flight.py` | `CalculateFlightUseCase` | Receives crop and hectares → calculates flight operation. Returns `FlightCalculationResult` |

#### Validators (`src/application/validators/`)

| File | Class | Description |
|------|-------|-------------|
| `__init__.py` | `MixtureValidator` | Validates no duplicate mixing orders or products |
| `__init__.py` | `ValidationResult` | Validation result with error flags and descriptive message |

---

### 3. Infrastructure Layer — `src/infrastructure/`

**Data access** via repositories. Data is currently in-memory (constants), but the pattern allows easy migration to a database or external API.

#### Repositories (`src/infrastructure/repositories/`)

| File | Class | Methods | Description |
|------|-------|---------|-------------|
| `crop_repository.py` | `CropRepository` | `obtener_todos()`, `obtener_nombres()`, `obtener_por_nombre()` | Data for 4 crops: Banana, Corn, Rice, Cocoa |
| `product_repository.py` | `ProductRepository` | `obtener_todos()` | Catalog of 51 agrochemical products |

---

### 4. Presentation Layer — `src/presentation/`

**User interface components** with Streamlit. Each component is independent and reusable.

#### Components (`src/presentation/components/`)

| File | Function | Description |
|------|----------|-------------|
| `header.py` | `render_header()`, `render_description()` | Logo in base64, title, and introductory description |
| `crop_form.py` | `render_general_data_form()` | Form: crop selection, hectares, date |
| `mixture_form.py` | `render_mixture_form()` | Dynamic product mixture form with inline validation |
| `results_display.py` | `render_mixture_results()` | Tables and metrics for results (per-ha and totals) |
| `flight_recommendations.py` | `render_flight_recommendations()` | Editable technical flight parameters |
| `flight_operations.py` | `render_flight_operations()` | Operational metrics and calculation details |

#### Utilities (`src/presentation/utils/`)

| File | Function | Description |
|------|----------|-------------|
| `__init__.py` | `load_local_css()` | Loads and injects custom CSS into Streamlit |

---

## Execution Flow

```
1. app.py (Orchestrator)
   │
   ├─► Presentation: render_header() + render_description()
   │
   ├─► Infrastructure: CropRepository.obtener_nombres()
   │                    ProductRepository.obtener_todos()
   │
   ├─► Presentation: render_general_data_form() → crop, hectares, date
   │
   ├─► Presentation: render_mixture_form() → products, volume, errors
   │
   ├─► Application: CalculateMixtureUseCase.ejecutar()
   │   │
   │   ├─► Domain: MixtureCalculatorService.calcular_mezcla()
   │   │   └─► Domain: Mixture.calcular_por_hectarea() + calcular_total()
   │   │
   │   └─► Result → Presentation: render_mixture_results()
   │
   ├─► Infrastructure: CropRepository.obtener_por_nombre()
   │
   ├─► Presentation: render_flight_recommendations()
   │
   └─► Application: CalculateFlightUseCase.ejecutar()
       │
       ├─► Domain: FlightCalculatorService.calcular_operacion()
       │
       └─► Result → Presentation: render_flight_operations()
```

---

## DDD Principles Applied

| Principle | Implementation |
|-----------|---------------|
| **Separation of responsibilities** | Each layer has a clear function and does not mix logic from other layers |
| **Independent domain** | `src/domain/` does not import Streamlit, Pandas, or any external framework |
| **Dependency inversion** | Outer layers depend on inner layers, never the other way around |
| **Immutable entities** | `Crop`, `Product`, `FlightOperation` use `@dataclass(frozen=True)` |
| **Aggregates** | `Mixture` encapsulates mixing logic and ensures consistency |
| **Value Objects** | `MixtureResult`, `FlightOperation` are value objects with no identity |
| **Repositories** | Abstraction of data access (decoupled from domain) |
| **Use Cases** | Application flows that coordinate domain + validation + result |

---

## Benefits of this Architecture

1. **Maintainability**: Each module can be modified independently
2. **Testability**: The domain can be tested without Streamlit or UI
3. **Scalability**: Adding new crops, products, or calculations is simple
4. **Reusability**: Domain services can be used in other contexts (REST API, CLI, etc.)
5. **Clarity**: Any developer can quickly understand where each piece belongs
