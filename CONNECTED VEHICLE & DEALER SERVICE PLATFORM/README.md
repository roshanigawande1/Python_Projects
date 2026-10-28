# Ford Connected Vehicle & Dealer Service Platform (Practice Project)

This is a **runnable** Django + Django REST Framework (DRF) project that follows the
architecture described in the interview guide PDF. It is a *representative* enterprise
API — not real Ford code — built so you can run it on your own laptop, understand every
line, and confidently talk about it in an interview.

It exposes REST APIs for:
- **Vehicles** (VIN, model, year, owner, dealer)
- **Dealers**
- **Service Appointments** (booking a car for service)
- **Diagnostic Codes** (fault codes reported by a vehicle)

---

## 1. Folder structure (matches the PDF)

```
ford_platform/
├── manage.py                  # Django's command-line tool (run server, migrations, tests...)
├── requirements.txt           # Python packages this project needs
├── Dockerfile                 # Instructions to build a Docker image of the API
├── docker-compose.yml         # Runs the API + a Postgres database together
├── .env.example                # Example environment variables (copy to .env)
├── config/                    # Project-level settings (the "brain" of the Django project)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── vehicle_service/           # The Django "app" containing our actual business logic
│   ├── models.py              # Database tables, defined as Python classes
│   ├── serializers.py         # Converts between JSON <-> Python/DB objects, and validates input
│   ├── permissions.py         # Custom rules for "who is allowed to see/do what"
│   ├── views.py                # The actual API endpoints (business logic)
│   ├── urls.py                 # Maps URLs like /api/v1/vehicles/ to views
│   ├── admin.py                 # Registers models in Django's built-in admin panel
│   └── tests.py                 # Automated tests for the API
└── k8s/                       # Kubernetes deployment files (for the "how would this scale in production" story)
    ├── deployment.yaml
    ├── service.yaml
```

This is *exactly* the structure from the interview PDF, fleshed out into working code.

---

## 2. How to run this project in VS Code (step by step, beginner-friendly)

### Step 0 — Prerequisites
- Install **Python 3.11+** (check with `python --version` or `python3 --version`)
- Install **VS Code** and open the `ford_platform` folder in it (`File > Open Folder`)
- (Optional, for later) Install **Docker Desktop** if you want to try the containerized version

### Step 1 — Create a virtual environment
A virtual environment is just an isolated folder that holds Python packages for *this*
project only, so it doesn't mess with other projects on your machine.

Open the VS Code terminal (`` Ctrl+` ``) and run:

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows (PowerShell)
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

You'll see `(.venv)` appear at the start of your terminal prompt — that means it's active.

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

This reads `requirements.txt` and installs Django, Django REST Framework, etc.

### Step 3 — Set environment variables

Copy `.env.example` to `.env`:

```bash
# Mac/Linux
cp .env.example .env
# Windows
copy .env.example .env
```

By default this project is configured to use **SQLite** (a database that is just a single file — zero setup) so you can run it immediately with no extra installs.
 The `.env` file
also shows how you'd switch to **PostgreSQL** later (see Section 4).

### Step 4 — Create the database tables (migrations)

```bash
python manage.py makemigrations
python manage.py migrate
```

`migrate` reads your `models.py` and creates matching tables in the database.

### Step 5 — Create an admin user (so you can log in and test)

```bash
python manage.py createsuperuser
```

Follow the prompts (username, email, password).

### Step 6 — Run the server

```bash
python manage.py runserver
```

Now open your browser to:
- `http://127.0.0.1:8000/admin/` → Django admin panel (log in with the superuser you made)
- `http://127.0.0.1:8000/api/v1/vehicles/` → Your API (DRF gives you a nice browsable UI)
- `http://127.0.0.1:8000/health/` → Health check endpoint (used by Kubernetes in production)

### Step 7 — Try it out
1. Go to `/admin/`, log in, and manually add a **Dealer** and a **Vehicle** through the
   admin UI (easiest way to add test data).
2. Go to `/api/v1/vehicles/` in your browser — DRF's browsable API lets you see and even
   POST data through a web form, no extra tools needed.
3. Run the automated tests:
   ```bash
   python manage.py test
   ```

That's it — you have a fully working REST API running locally.

---

## 3. How the database is working (in simple words)

Think of the database as a set of **spreadsheets** (tables), one per model:

- `Dealer` table → one row per dealer (dealer_code, name)
- `Vehicle` table → one row per vehicle (VIN, model, year, owner, **which dealer it belongs to**)
- `ServiceAppointment` table → one row per booking (which vehicle, which dealer, when, status)
- `DiagnosticCode` table → one row per fault code reported by a vehicle

**How Django talks to the database (the ORM):**
You never write raw SQL. You write Python classes in `models.py` (e.g. `class Vehicle(models.Model)`),
and Django's **ORM** (Object-Relational Mapper) translates your Python code into SQL behind
the scenes.

Example: `Vehicle.objects.filter(dealer_id=7)` becomes something like
`SELECT * FROM vehicle_service_vehicle WHERE dealer_id = 7;` automatically.

**Relationships:**
- `Vehicle.dealer` is a `ForeignKey` → each vehicle belongs to exactly one dealer (one-to-many:
  one dealer can have many vehicles).
- `ServiceAppointment.vehicle` and `ServiceAppointment.dealer` are also ForeignKeys, linking an
  appointment back to a specific car and dealer.

**Migrations** are Django's version-control system for your database schema. Every time you
change `models.py`, you run `makemigrations` (Django writes a "diff" file describing the
change) then `migrate` (Django applies that diff to the actual database). This is how you
evolve a database safely over time, in a team, without manually writing `ALTER TABLE`.

**SQLite vs PostgreSQL (see Section 4 below):** for local development we use SQLite because
it needs zero setup. In the real/interview architecture (matching the PDF), production uses
**PostgreSQL** — a much more powerful, multi-user database server — because it handles many
simultaneous users, larger data volumes, and advanced features (indexes, replication, etc.)
much better than a single file can.

---

## 4. Switching to PostgreSQL (matches the "production" story from the PDF)

1. Install PostgreSQL locally, or run it via Docker:
   ```bash
   docker run --name ford-postgres -e POSTGRES_PASSWORD=change-me -e POSTGRES_DB=ford_platform -p 5432:5432 -d postgres:16
   ```
2. In `.env`, uncomment/set the PostgreSQL variables (DB_ENGINE=postgres, DB_NAME, DB_USER, etc.)
3. Re-run `python manage.py migrate` — Django will create the same tables, but now inside
   PostgreSQL instead of the local SQLite file.

This is exactly the same code — only the database *engine* changes. That's the power of
using Django's ORM instead of hand-written SQL: **your application code doesn't change** when
you switch databases, only the settings.

---

## 5. Running it with Docker (optional, matches the PDF's container story)

```bash
docker compose up --build
```

This starts **two containers**: one running PostgreSQL (`db`), one running your Django app
via Gunicorn (`web`). They talk to each other over Docker's internal network. This mirrors
exactly what Section 9 of the interview guide describes ("containerized with Docker,
deployed to Kubernetes for horizontal scaling").

---

## 6. How to explain this project in an interview (quick script)

> "I built a connected-vehicle and dealer-service REST API using Python, Django REST
> Framework, and PostgreSQL. It exposes endpoints for vehicles, service appointments, and
> diagnostic codes, with authentication, permission-based authorization so a dealer only
> sees their own vehicles, input validation via serializers, and rate limiting. It's
> containerized with Docker and designed to run on Kubernetes with multiple replicas,
> health checks, and autoscaling for production reliability."

Then be ready to walk through:
- **Request lifecycle**: Client → Load balancer → Django middleware → DRF auth → permissions
  → serializer validation → view/business logic → ORM → PostgreSQL → JSON response.
- **Why DRF over plain Django**: serializers, auth/permission classes, throttling, routers,
  browsable API, testing tools.
- **How dealer data isolation works**: `get_queryset()` in each ViewSet filters by the
  logged-in user's `dealer_id`, so Dealer A can never see Dealer B's vehicles even if they
  guess an ID.
- **Scaling**: stateless API pods behind a Kubernetes Service + HPA (Horizontal Pod
  Autoscaler); database scaled via indexing, connection pooling, and read replicas — not
  by adding more API pods.

See the original PDF's Section 13 for a full list of likely interview Q&A — the code in
this project directly backs every one of those answers.
