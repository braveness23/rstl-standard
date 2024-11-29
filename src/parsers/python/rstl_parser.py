import json
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from datetime import datetime
import jsonschema
from jsonschema import validate, ValidationError

# Define the schema (truncated for brevity; use the full schema in actual implementation)
RSTL_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "RSTL Event Schema",
    "type": "object",
    "required": ["title", "description", "time"],
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "location": {"type": "string"},
        "time": {
            "type": "object",
            "required": ["calendar"],
            "properties": {
                "calendar": {
                    "type": "string",
                    "enum": [
                        "Gregorian",
                        "Julian",
                        "Islamic",
                        "Hebrew",
                        "Chinese",
                        "GeologicalTime",
                        "Custom"
                    ]
                },
                "precision": {
                    "type": "string",
                    "enum": ["instant", "timespan", "approximate"]
                },
                "instant": {
                    "type": "string",
                    "format": "date-time"
                },
                "start": {"type": "string"},
                "end": {"type": "string"},
                "approximate": {"type": "string"},
                "qualifier": {"type": "string"},
                "uncertainty": {"type": "string"}
            },
            "oneOf": [
                {
                    "required": ["instant"],
                    "properties": {
                        "precision": {"const": "instant"}
                    }
                },
                {
                    "required": ["start", "end"],
                    "properties": {
                        "precision": {"const": "timespan"}
                    }
                },
                {
                    "required": ["approximate"],
                    "properties": {
                        "precision": {"const": "approximate"}
                    }
                }
            ]
        },
        "metadata": {
            "type": "object",
            "properties": {
                "categories": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "links": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "format": "uri"
                    }
                },
                "additional": {"type": "object"}
            },
            "additionalProperties": True
        }
    },
    "additionalProperties": False
}

@dataclass
class Time:
    calendar: str
    precision: Optional[str] = None
    instant: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    approximate: Optional[str] = None
    qualifier: Optional[str] = None
    uncertainty: Optional[str] = None

@dataclass
class Metadata:
    categories: Optional[List[str]] = field(default_factory=list)
    links: Optional[List[str]] = field(default_factory=list)
    additional: Optional[Dict[str, Any]] = field(default_factory=dict)

@dataclass
class Event:
    id: Optional[str]
    title: str
    description: str
    location: Optional[str]
    time: Time
    metadata: Optional[Metadata]

def parse_time(data: Dict[str, Any]) -> Time:
    return Time(
        calendar=data.get('calendar'),
        precision=data.get('precision'),
        instant=data.get('instant'),
        start=data.get('start'),
        end=data.get('end'),
        approximate=data.get('approximate'),
        qualifier=data.get('qualifier'),
        uncertainty=data.get('uncertainty')
    )

def parse_metadata(data: Dict[str, Any]) -> Metadata:
    return Metadata(
        categories=data.get('categories', []),
        links=data.get('links', []),
        additional=data.get('additional', {})
    )

def parse_event(data: Dict[str, Any]) -> Event:
    # Validate the data against the schema
    try:
        validate(instance=data, schema=RSTL_SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Invalid RSTL event data: {e.message}")

    time_data = parse_time(data['time'])
    metadata_data = parse_metadata(data.get('metadata', {}))
    
    return Event(
        id=data.get('id'),
        title=data['title'],
        description=data['description'],
        location=data.get('location'),
        time=time_data,
        metadata=metadata_data
    )

# Example usage
if __name__ == "__main__":
    # Sample RSTL event JSON
    sample_json = '''
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
    '''
    # Parse the JSON string into a dictionary
    event_data = json.loads(sample_json)
    
    # Parse the event
    try:
        event = parse_event(event_data)
        print(f"Event Title: {event.title}")
        print(f"Event Description: {event.description}")
        print(f"Event Time Instant: {event.time.instant}")
        print(f"Event Categories: {event.metadata.categories}")
    except ValueError as ve:
        print(ve)
