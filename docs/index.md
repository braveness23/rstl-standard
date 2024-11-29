# Really Simple Time Line (RSTL) Documentation

Welcome to the documentation for the **Really Simple Time Line (RSTL)** standard. RSTL is a JSON-based data format designed to represent events across all periods of history, with varying levels of time precision and calendar systems. It is optimized for use with NoSQL databases and aims to be both flexible and extensible.

---

## Contents

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
- [JSON Structure Definition](#json-structure-definition)
- [JSON Schema](#json-schema)
- [Examples](#examples)
- [Implementation Guidelines](#implementation-guidelines)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Introduction

The **Really Simple Time Line (RSTL)** standard provides a unified way to represent temporal events ranging from precise moments to broad timespans, accommodating various calendar systems and levels of time precision. Whether you're cataloging historical events, planning future activities, or archiving data across different eras, RSTL offers a flexible and extensible format to meet your needs.

---

## Key Features

- **Temporal Flexibility**: Represent precise instants, timespans, and approximate dates.
- **Calendar Support**: Accommodate multiple calendar systems, including Gregorian, Julian, Islamic, Hebrew, Chinese, and Geological Time.
- **Precision Levels**: Specify the precision of time data—instant, timespan, or approximate.
- **Uncertainty Representation**: Use qualifiers and uncertainty ranges for approximate dates.
- **Extensible Metadata**: Include additional information such as categories, tags, and custom metadata.
- **JSON-Based**: Utilize the simplicity and ubiquity of JSON for data representation.
- **NoSQL Optimization**: Designed for efficient storage and querying in NoSQL databases.

---

## Getting Started

To begin using RSTL:

1. **Understand the JSON Structure**: Familiarize yourself with the core components of an RSTL event.
2. **Validate Your Data**: Use the provided JSON Schema to ensure your data conforms to the standard.
3. **Implement in Your Application**: Integrate RSTL into your data models, APIs, or databases.
4. **Contribute**: Join the community to improve and expand the standard.

---

## JSON Structure Definition

Each event in RSTL is represented as a JSON object with the following structure:

### **Root Object: Event**

| Field         | Type   | Required | Description                                              |
|---------------|--------|----------|----------------------------------------------------------|
| `id`          | string | No       | Unique identifier for the event.                         |
| `title`       | string | Yes      | Name of the event.                                       |
| `description` | string | Yes      | Detailed description of the event.                       |
| `location`    | string | No       | Geographical location of the event.                      |
| `time`        | object | Yes      | Temporal information of the event.                       |
| `metadata`    | object | No       | Additional information like categories and links.        |

---

### **Time Object**

| Field         | Type   | Required | Description                                              |
|---------------|--------|----------|----------------------------------------------------------|
| `calendar`    | string | Yes      | Calendar system used (e.g., "Gregorian").                |
| `precision`   | string | No       | Precision level ("instant", "timespan", "approximate").  |
| `instant`     | string | Cond.*   | Precise point in time (ISO 8601 format).                 |
| `start`       | string | Cond.*   | Start of the timespan (ISO 8601 format).                 |
| `end`         | string | Cond.*   | End of the timespan (ISO 8601 format).                   |
| `approximate` | string | Cond.*   | Approximate date as a string.                            |
| `qualifier`   | string | No       | Term indicating approximation (e.g., "circa").           |
| `uncertainty` | string | No       | Uncertainty range (e.g., "±5 years").                    |

*Conditional fields are required based on the `precision` value.

---

### **Metadata Object**

| Field        | Type            | Required | Description                                    |
|--------------|-----------------|----------|------------------------------------------------|
| `categories` | array of string | No       | Categories or tags associated with the event.  |
| `links`      | array of string | No       | URLs or URIs related to the event.             |
| `additional` | object          | No       | Custom metadata fields.                        |

---

## JSON Schema

The RSTL JSON Schema defines the structure and constraints of the data format. It can be used to validate your event data.

**Schema File**: [rstl-schema.json](schema/rstl-schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RSTL Event Schema",
  "type": "object",
  "required": ["title", "description", "time"],
  "properties": {
    "id": {
      "type": "string",
      "description": "A unique identifier for the event."
    },
    "title": {
      "type": "string",
      "description": "The name of the event."
    },
    "description": {
      "type": "string",
      "description": "A detailed description of the event."
    },
    "location": {
      "type": "string",
      "description": "The geographical location of the event."
    },
    "time": {
      "type": "object",
      "required": ["calendar"],
      "properties": {
        "calendar": {
          "type": "string",
          "description": "The calendar system used.",
          "enum": ["Gregorian", "Julian", "Islamic", "Hebrew", "Chinese", "GeologicalTime", "Custom"]
        },
        "precision": {
          "type": "string",
          "description": "The precision of the time representation.",
          "enum": ["instant", "timespan", "approximate"]
        },
        "instant": {
          "type": "string",
          "format": "date-time",
          "description": "A precise point in time."
        },
        "start": {
          "type": "string",
          "description": "The start of the timespan."
        },
        "end": {
          "type": "string",
          "description": "The end of the timespan."
        },
        "approximate": {
          "type": "string",
          "description": "An approximate date."
        },
        "qualifier": {
          "type": "string",
          "description": "Qualifier indicating approximation."
        },
        "uncertainty": {
          "type": "string",
          "description": "The uncertainty range."
        }
      },
      "oneOf": [
        {
          "required": ["instant"],
          "properties": {
            "precision": { "const": "instant" }
          }
        },
        {
          "required": ["start", "end"],
          "properties": {
            "precision": { "const": "timespan" }
          }
        },
        {
          "required": ["approximate"],
          "properties": {
            "precision": { "const": "approximate" }
          }
        }
      ]
    },
    "metadata": {
      "type": "object",
      "properties": {
        "categories": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Categories or tags for the event."
        },
        "links": {
          "type": "array",
          "items": { "type": "string", "format": "uri" },
          "description": "Related URLs or URIs."
        },
        "additional": {
          "type": "object",
          "description": "Additional custom metadata."
        }
      },
      "additionalProperties": true
    }
  },
  "additionalProperties": false
}
```

## Examples

Explore practical examples of RSTL events:

Example 1: Precise Instant Event

```json
{
  "id": "event-001",
  "title": "Moon Landing",
  "description": "The first human landing on the Moon.",
  "location": "Sea of Tranquility, Moon",
  "time": {
    "calendar": "Gregorian",
    "precision": "instant",
    "instant": "1969-07-20T20:17:00Z"
  },
  "metadata": {
    "categories": ["Space Exploration", "NASA Missions"],
    "links": ["https://en.wikipedia.org/wiki/Apollo_11"]
  }
}
```

---

Example 2: Precise Timespan Event

```json
{
  "id": "event-002",
  "title": "World War II",
  "description": "A global war that lasted from 1939 to 1945.",
  "time": {
    "calendar": "Gregorian",
    "precision": "timespan",
    "start": "1939-09-01",
    "end": "1945-09-02"
  },
  "metadata": {
    "categories": ["War", "Global Conflict"],
    "links": ["https://en.wikipedia.org/wiki/World_War_II"]
  }
}
```

---

Example 3: Approximate Date Event

```json
{
  "id": "event-003",
  "title": "Construction of Stonehenge",
  "description": "The estimated time when Stonehenge was constructed.",
  "location": "Wiltshire, England",
  "time": {
    "calendar": "Gregorian",
    "precision": "approximate",
    "approximate": "-3000",
    "qualifier": "circa",
    "uncertainty": "±200 years"
  },
  "metadata": {
    "categories": ["Archaeology", "Prehistoric Monuments"],
    "links": ["https://en.wikipedia.org/wiki/Stonehenge"]
  }
}
```

---

Example 4: Geological Timespan Event

```json
{
  "id": "event-004",
  "title": "Jurassic Period",
  "description": "A geological period that spanned 56 million years.",
  "time": {
    "calendar": "GeologicalTime",
    "precision": "timespan",
    "start": "-201300000",
    "end": "-145000000",
    "qualifier": "circa"
  },
  "metadata": {
    "categories": ["Geology", "Earth History"]
  }
}
```

---

Example 5: Event in a Different Calendar System

```json
{
  "id": "event-005",
  "title": "Hijra (Migration to Medina)",
  "description": "The migration of the Islamic prophet Muhammad and his followers from Mecca to Medina.",
  "location": "From Mecca to Medina",
  "time": {
    "calendar": "Islamic",
    "precision": "instant",
    "instant": "0001-01-01",
    "qualifier": "1 AH"
  },
  "metadata": {
    "categories": ["Islamic History"],
    "links": ["https://en.wikipedia.org/wiki/Hijra_(Islam)"]
  }
}
```

---

## Implementation Guidelines

### Time Fields

**ISO 8601 Format:** Use ISO 8601 extended format for instant, start, and end fields.
Years Beyond Standard Range: ISO 8601 allows expanded representations for years outside the standard range (e.g., -0001 for 1 BCE).

**Negative Years:** Represent BCE dates with negative years (e.g., -0444 for 444 BCE).

**Large Numbers:** Use strings to represent large numbers, especially for geological times (e.g., "-201300000").

### Calendar Systems

**Supported Calendars:** The calendar field should be one of the supported systems: "Gregorian", "Julian", "Islamic", "Hebrew", "Chinese", "GeologicalTime", or "Custom".

**Custom Calendars:** If using a non-standard calendar, set calendar to "Custom" and provide details in metadata.additional.

**Conversion Utilities:** Consider developing utilities to convert dates between calendar systems if necessary.

### Qualifiers and Uncertainty

**Qualifiers:** Use the qualifier field to express approximate dates (e.g., "circa", "approximately").

**Uncertainty:** Use the uncertainty field to express the range of uncertainty (e.g., "±5 years").

### Metadata Extension

**Flexible Metadata:** The metadata.additional object can hold any key-value pairs for extended information.

**Links:** Include relevant URLs in the links array for more information.

### Storage and Querying in NoSQL Databases

**Document Structure:** Store each event as a separate document in your NoSQL database.

**Indexing:** Index time fields and metadata categories for efficient querying.

**Querying:** Utilize the database's querying capabilities to filter events based on time ranges, categories, and other criteria.

### Example Queries (MongoDB)

- Find Events in a Time Range

```javascript
db.events.find({
  $or: [
    {
      "time.instant": {
        $gte: "1900-01-01T00:00:00Z",
        $lte: "2000-12-31T23:59:59Z"
      }
    },
    {
      "time.start": { $lte: "2000-12-31T23:59:59Z" },
      "time.end": { $gte: "1900-01-01T00:00:00Z" }
    }
  ]
})
```

`

- Find Events with a Specific Category

```javascript
db.events.find({
  "metadata.categories": "Space Exploration"
})
```

## Contributing

We welcome contributions from the community!

## How to Contribute

1. Fork the Repository: Create a personal copy of the repository.
2. Create a Branch: Use descriptive names (e.g., feature/add-new-calendar).
3. Make Changes: Implement your feature or fix.
4. Commit: Write clear and concise commit messages.
5. Push and Pull Request: Push your branch and open a pull request against the develop branch.
6. Review: Participate in the review process and make any necessary changes.

## Contribution Guidelines

- Code Style: Follow the established code style guidelines.
- Testing: Write unit tests for new code and ensure all tests pass.
- Documentation: Update or add documentation for your changes.

For detailed guidelines, see CONTRIBUTING.md.

## License

The RSTL standard is open-source and distributed under the MIT License.

## Acknowledgments

We thank all contributors and the community for their support and feedback in developing the RSTL standard.
