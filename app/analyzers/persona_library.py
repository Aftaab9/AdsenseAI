"""
Persona Library Manager

Manages loading, caching, and retrieval of audience personas for testing.
Implements singleton pattern for efficient persona data management.

Requirements: 1.1-1.3
"""

import json
import os
from typing import List, Optional, Dict
from pathlib import Path

from app.models import Persona, PersonaCategory


class PersonaLibrary:
    """
    Manages the library of pre-built audience personas.
    
    Implements caching to avoid repeated file I/O operations.
    Provides methods to retrieve personas by ID, category, or all at once.
    """
    
    _instance = None
    _personas: Dict[str, Persona] = {}
    _loaded = False
    
    def __new__(cls):
        """Singleton pattern - only one instance of PersonaLibrary"""
        if cls._instance is None:
            cls._instance = super(PersonaLibrary, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the persona library (loads personas on first call)"""
        if not self._loaded:
            self.load_personas()
    
    def load_personas(self) -> None:
        """
        Load personas from JSON file and cache them.
        
        Loads the MVP personas from app/data/personas/mvp_personas.json
        and stores them in memory for fast retrieval.
        
        Requirements: 1.1
        """
        if self._loaded:
            return
        
        # Determine the path to the personas JSON file
        current_dir = Path(__file__).parent.parent
        personas_file = current_dir / "data" / "personas" / "mvp_personas.json"
        
        if not personas_file.exists():
            raise FileNotFoundError(
                f"Personas file not found at {personas_file}. "
                "Please ensure mvp_personas.json exists in app/data/personas/"
            )
        
        # Load and parse the JSON file
        with open(personas_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert JSON data to Persona objects and cache them
        self._personas = {}
        for persona_data in data.get('personas', []):
            try:
                persona = Persona(**persona_data)
                self._personas[persona.id] = persona
            except Exception as e:
                print(f"Warning: Failed to load persona {persona_data.get('id', 'unknown')}: {e}")
                continue
        
        self._loaded = True
        print(f"Loaded {len(self._personas)} personas into library")
    
    def get_persona_by_id(self, persona_id: str) -> Optional[Persona]:
        """
        Retrieve a specific persona by its ID.
        
        Args:
            persona_id: Unique identifier for the persona (e.g., 'gen_z_metro')
        
        Returns:
            Persona object if found, None otherwise
        
        Requirements: 1.2
        """
        return self._personas.get(persona_id)
    
    def get_all_personas(self) -> List[Persona]:
        """
        Retrieve all loaded personas.
        
        Returns:
            List of all Persona objects in the library
        
        Requirements: 1.3
        """
        return list(self._personas.values())
    
    def get_personas_by_category(self, category: PersonaCategory) -> List[Persona]:
        """
        Retrieve all personas in a specific category.
        
        Args:
            category: PersonaCategory enum value
        
        Returns:
            List of Persona objects matching the category
        """
        return [
            persona for persona in self._personas.values()
            if persona.category == category
        ]
    
    def get_personas_by_ids(self, persona_ids: List[str]) -> List[Persona]:
        """
        Retrieve multiple personas by their IDs.
        
        Args:
            persona_ids: List of persona IDs to retrieve
        
        Returns:
            List of Persona objects (skips IDs that don't exist)
        """
        personas = []
        for persona_id in persona_ids:
            persona = self.get_persona_by_id(persona_id)
            if persona:
                personas.append(persona)
        return personas
    
    def get_persona_count(self) -> int:
        """Get the total number of loaded personas"""
        return len(self._personas)
    
    def get_all_categories(self) -> List[PersonaCategory]:
        """Get list of all unique categories in the library"""
        categories = set(persona.category for persona in self._personas.values())
        return sorted(list(categories), key=lambda x: x.value)
    
    def search_personas(self, query: str) -> List[Persona]:
        """
        Search personas by name or tagline.
        
        Args:
            query: Search string (case-insensitive)
        
        Returns:
            List of matching Persona objects
        """
        query_lower = query.lower()
        return [
            persona for persona in self._personas.values()
            if query_lower in persona.name.lower() or query_lower in persona.tagline.lower()
        ]


# Singleton instance getter
_library_instance = None

def get_persona_library() -> PersonaLibrary:
    """
    Get the singleton PersonaLibrary instance.
    
    This is the recommended way to access the persona library.
    
    Returns:
        PersonaLibrary singleton instance
    """
    global _library_instance
    if _library_instance is None:
        _library_instance = PersonaLibrary()
    return _library_instance
