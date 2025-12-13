# ALX Travel App

A modular travel planning application: search destinations, build itineraries, manage bookings, and track budgets.

## Features

- Destination discovery (search, filters, categories)
- Itinerary builder (days, activities, drag/drop ordering)
- Booking integration placeholders (flights, hotels, rentals)
- Budget tracking and cost summaries
- User accounts (auth, profiles, saved trips)
- Offline-friendly caching strategy (planned)
- API abstraction layer for external services

## Tech Stack

- Frontend: React / Next.js (or React SPA) + TypeScript
- Backend: Node.js (Express / Nest) or Django (TBD)
- Data: PostgreSQL (primary), Redis (cache), S3-compatible storage (media)
- Auth: JWT + refresh tokens (short-term), OAuth expansion (future)
- Infra: Docker, CI (GitHub Actions), optional Kubernetes (scaling phase)
- Testing: Jest + React Testing Library / PyTest (if Python backend)

## Architecture (High-Level)

- ui: presentation + state management (Redux / Zustand / Query)
- services: HTTP clients, API wrappers
- core: domain models (Trip, Activity, BudgetItem)
- api: REST/GraphQL endpoints
- integrations: external providers (maps, flights)
- worker: async tasks (notifications, periodic sync)

## Getting Started

1. Clone: git clone <repo_url>
2. Install: npm install (and/or pip install -r requirements.txt)
3. Copy env: cp .env.example .env
4. Run dev: npm run dev (and backend: npm run server / python manage.py runserver)
5. Open: http://localhost:3000

## Environment Variables (.env)

- APP_PORT=
- DATABASE_URL=
- REDIS_URL=
- JWT_SECRET=
- STORAGE_BUCKET=
- EXTERNAL_MAPS_KEY=
  (See .env.example)

## Scripts

- npm run dev: start frontend dev
- npm run build: production build
- npm run lint: static analysis
- npm test: run unit tests
- npm run format: apply code style

## Project Structure (Indicative)

```
alx_travel_app/
  frontend/
    src/
      components/
      pages/
      hooks/
      services/
  backend/
    src/
      modules/
      routes/
      models/
      workers/
  infra/
    docker/
    k8s/
```

## Data Models (Planned)

- User: id, name, email, roles
- Trip: id, userId, title, startDate, endDate
- Activity: id, tripId, dayIndex, type, notes, cost
- BudgetItem: id, tripId, category, amount, currency

## Testing

- Unit: core models, services
- Integration: API endpoints
- E2E: Cypress / Playwright (future)
- Coverage threshold: 80% min

## Deployment

- Containerized build
- Migrations on release
- Version tagging (semver)
- Monitoring: Prometheus + Grafana (future)
- Error tracking: Sentry (optional)

## Performance Considerations

- Caching frequent destination queries
- Lazy loading heavy components
- Batched API requests
- Optimistic UI for itinerary edits

## Contribution

1. Fork and branch: feat/<name>
2. Keep commits atomic
3. Add/update tests for changes
4. Submit PR with concise description

## Roadmap (Next)

- Real provider integrations
- Collaborative trip editing
- Push/mobile notifications
- Multi-currency budget handling

## License

MIT (unless changed later)

## Security

- Input validation (server + client)
- Rate limiting on auth endpoints
- Secure cookie for refresh tokens

## Disclaimer

Early-stage project; interfaces may change.

## API Endpoints

- Base: /api/
- Listings:
  - GET /api/listings/
  - POST /api/listings/
  - GET /api/listings/{id}/
  - PUT/PATCH /api/listings/{id}/
  - DELETE /api/listings/{id}/
- Bookings:
  - GET /api/bookings/
  - POST /api/bookings/
  - GET /api/bookings/{id}/
  - PUT/PATCH /api/bookings/{id}/
  - DELETE /api/bookings/{id}/

## API Documentation (Swagger)

- Swagger UI: /api/docs/
- ReDoc: /api/redoc/
- OpenAPI JSON: /api/schema.json
- OpenAPI YAML: /api/schema.yaml

### Setup

- `pip install drf-yasg`
- Add `rest_framework` and `drf_yasg` to INSTALLED_APPS in Django settings.
