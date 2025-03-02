# Event Manager - System zarządzania zdarzeniami

## 📌 Opis projektu

Event Manager to system symulujący zarządzanie zdarzeniami. API wykorzystuje **GraphQL**, umożliwiając operacje CRUD na zdarzeniach. System korzysta z **Kafki** do kolejkowania zdarzeń oraz **Fausta** do ich asynchronicznego przetwarzania i zapisywania do bazy danych SQLite.

## 🛠 Wykorzystane technologie

- **Python**
- **Django** + **Graphene (GraphQL dla Django)**
- **Kafka** (brokers i kolejkowanie zdarzeń)
- **Faust** (asynchroniczne przetwarzanie zdarzeń)
- **Docker** + **Docker Compose**
- **SQLite** (baza danych dla zdarzeń)

## 🗄 Model bazy danych

Tabela **Event** zawiera:

- `uuid` (UUID, klucz główny)
- `name` (nazwa zdarzenia)
- `source` (źródło: `users` lub `products`)
- `created_at` (data utworzenia)
- `updated_at` (ostatnia aktualizacja)
- `description` (opcjonalny opis)

## 🚀 Instalacja

### 1. Wymagania

- **Docker**: Dla projektu zostanie stworzony kontener zawierający wszystkie elementy potrzebne do działania programu, w tym:
    - Aplikacja Django wraz ze wszystkimi zainstalowanymi pakietami z **reauirements.txt**
    - Broker Kafka
    - Konsumer Faust

### 2. Uruchomienie (Docker)

```sh
docker-compose up --build
```
Jeżeli aplikacja nie wystartowała poprawnie, po chwili należy spróbować zrestartować odpowiedni moduł:
```sh
docker-compose restart faust_worker
docker-compose restart django
```
Jest to spowodowane tym, że czasem serwis **Kafka** nie włączył się w pełni.

## 🔄 Opis działania

### 📡 API GraphQL (Django + Graphene)

- `CreateEvent` – tworzenie zdarzenia
- `CreateEventAsync` – tworzenie zdarzenia prze Kafkę i Fausta
- `allEvents` – pobieranie listy zdarzeń
- `deleteEvent` – usuwanie zdarzenia


### 📨 Kafka (Producent zdarzeń)

Kod wysyłający zdarzenie:

```python
producer.send('events', {'name': 'Test', 'source': 'users'})
```
Kafka to broker wiadomości, działający jako pośrednik między aplikacją, a innym asynchronicznym serwisem , jak chociażby faust.

### 🎛 Faust (Konsument zdarzeń)

Kod odbierający zdarzenie:

```python
@app.agent(events_topic)
async def process_event(events):
    async for event in events:
        await save_event(event)
```
Faust to serwis przetworzający asynchronicznie podane zadania. Działa on po części niezależnie od serwera Django, pozwalając na wykonywanie poleceń w tle, podczas gdy użytkownik nie oczekuje na response od serwera, jeżeli to nie jest treaz konieczne.

## 📌 Endpointy GraphQL
| Mutacja / Query | Opis |
|----------------|------|
| `createEvent(name, source, description)` | Tworzy nowe zdarzenie |
| `createEventAsync(name, source, description)` | Tworzy zdarzenie i wysyła je do Kafki |
| `allEvents` | Pobiera wszystkie zdarzenia |
| `deleteEvent(uuid)` | Usuwa zdarzenie na podstawie UUID |

## 📌 Opis endpointów

### 🔹 `createEvent`
**Opis:** Tworzy nowe zdarzenie w bazie danych.

**Przykładowy request:**
```graphql
mutation {
  createEvent(name: "Test Event", source: "users", description: "Opis testowego eventu") {
    event {
      uuid
      name
      createdAt
    }
  }
}
```

**Przykładowy response:**
```json
{
  "data": {
    "createEvent": {
      "event": {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Test Event",
        "createdAt": "2025-03-02T12:00:00Z"
      }
    }
  }
}
```

---

### 🔹 `createEventAsync`
**Opis:** Tworzy zdarzenie i wysyła je do Kafki do asynchronicznego przetwarzania.

**Przykładowy request:**
```graphql
mutation {
  createEventAsync(name: "Async Event", source: "products", description: "Asynchroniczne przetwarzanie") {
    event {
      uuid
      name
      createdAt
    }
  }
}
```

**Przykładowy response:**
```json
{
  "data": {
    "createEventAsync": {
      "event": {
        "uuid": "123e4567-e89b-12d3-a456-426614174001",
        "name": "Async Event",
        "createdAt": "2025-03-02T12:05:00Z"
      }
    }
  }
}
```

---

### 🔹 `allEvents`
**Opis:** Pobiera wszystkie zdarzenia z bazy danych.

**Przykładowy request:**
```graphql
query {
  allEvents {
    edges {
      node {
        uuid
        name
        source
        createdAt
      }
    }
  }
}
```

**Przykładowy response:**
```json
{
  "data": {
    "allEvents": {
      "edges": [
        {
          "node": {
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Test Event",
            "source": "users",
            "createdAt": "2025-03-02T12:00:00Z"
          }
        }
      ]
    }
  }
}
```

---

### 🔹 `deleteEvent`
**Opis:** Usuwa zdarzenie na podstawie UUID.

**Przykładowy request:**
```graphql
mutation {
  deleteEvent(uuid: "123e4567-e89b-12d3-a456-426614174000") {
    success
  }
}
```

**Przykładowy response:**
```json
{
  "data": {
    "deleteEvent": {
      "success": true
    }
  }
}
```

