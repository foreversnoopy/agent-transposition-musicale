"""
Outils de manipulation musicale pour l'agent
"""
from typing import List, Dict, Optional
import re


class MusicTools:
    """Classe contenant les outils de manipulation musicale"""
    
    # Mapping de toutes les notes possibles avec leurs équivalents enharmoniques
    NOTE_MAPPINGS = {
        'C': ['C', 'B#'],
        'C#': ['C#', 'Db'],
        'D': ['D'],
        'D#': ['D#', 'Eb'],
        'E': ['E', 'Fb'],
        'F': ['F', 'E#'],
        'F#': ['F#', 'Gb'],
        'G': ['G'],
        'G#': ['G#', 'Ab'],
        'A': ['A'],
        'A#': ['A#', 'Bb'],
        'B': ['B', 'Cb']
    }
    
    # Notes chromatiques pour les calculs de distance
    CHROMATIC_SCALE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def __init__(self, scales_config: Dict):
        """
        Initialise les outils musicaux avec la configuration des gammes
        
        Args:
            scales_config: Dictionnaire contenant les gammes de notes
        """
        self.scales = scales_config
    
    def normalize_note(self, note: str) -> str:
        """
        Normalise une note en enlevant les espaces et en standardisant le format
        
        Args:
            note: La note à normaliser (ex: "C#", "Db", "C ")
            
        Returns:
            La note normalisée
        """
        note = note.strip().upper()
        # Gérer les bémols et dièses
        note = note.replace('♯', '#').replace('♭', 'b')
        return note
    
    def get_scale_notes(self, scale_name: str) -> Optional[List[str]]:
        """
        Récupère les notes d'une gamme par son nom
        
        Args:
            scale_name: Nom de la gamme
            
        Returns:
            Liste des notes de la gamme ou None si la gamme n'existe pas
        """
        if scale_name in self.scales:
            return self.scales[scale_name]['notes']
        return None
    
    def is_note_in_scale(self, note: str, scale_name: str) -> bool:
        """
        Vérifie si une note est dans une gamme donnée
        
        Args:
            note: La note à vérifier
            scale_name: Nom de la gamme
            
        Returns:
            True si la note est dans la gamme
        """
        note = self.normalize_note(note)
        scale_notes = self.get_scale_notes(scale_name)
        
        if not scale_notes:
            return False
        
        # Normaliser les notes de la gamme
        normalized_scale = [self.normalize_note(n) for n in scale_notes]
        
        # Vérifier la note et ses équivalents enharmoniques
        for canonical, variants in self.NOTE_MAPPINGS.items():
            if note in variants:
                return any(v in normalized_scale for v in variants)
        
        return note in normalized_scale
    
    def find_closest_note_in_scale(self, note: str, scale_name: str) -> Optional[str]:
        """
        Trouve la note la plus proche dans une gamme donnée
        
        Args:
            note: La note source
            scale_name: Nom de la gamme cible
            
        Returns:
            La note la plus proche dans la gamme
        """
        note = self.normalize_note(note)
        scale_notes = self.get_scale_notes(scale_name)
        
        if not scale_notes:
            return None
        
        # Si la note est déjà dans la gamme, la retourner
        if self.is_note_in_scale(note, scale_name):
            return note
        
        # Trouver la position de la note dans l'échelle chromatique
        note_base = note.rstrip('#b')
        if note_base not in [n.rstrip('#b') for n in self.CHROMATIC_SCALE]:
            return None
        
        # Trouver l'index chromatique de la note
        chromatic_index = None
        for i, chromatic_note in enumerate(self.CHROMATIC_SCALE):
            for canonical, variants in self.NOTE_MAPPINGS.items():
                if note in variants and chromatic_note == canonical:
                    chromatic_index = i
                    break
            if chromatic_index is not None:
                break
        
        if chromatic_index is None:
            return scale_notes[0]
        
        # Trouver la note la plus proche dans la gamme
        min_distance = 12  # Maximum de demi-tons dans une octave
        closest_note = scale_notes[0]
        
        for scale_note in scale_notes:
            scale_note_norm = self.normalize_note(scale_note)
            scale_chromatic_index = None
            
            for i, chromatic_note in enumerate(self.CHROMATIC_SCALE):
                for canonical, variants in self.NOTE_MAPPINGS.items():
                    if scale_note_norm in variants and chromatic_note == canonical:
                        scale_chromatic_index = i
                        break
                if scale_chromatic_index is not None:
                    break
            
            if scale_chromatic_index is not None:
                distance = min(
                    abs(scale_chromatic_index - chromatic_index),
                    12 - abs(scale_chromatic_index - chromatic_index)
                )
                
                if distance < min_distance:
                    min_distance = distance
                    closest_note = scale_note
        
        return closest_note
    
    def parse_notes_from_text(self, text: str) -> List[str]:
        """
        Extrait les notes d'un texte
        
        Args:
            text: Texte contenant des notes
            
        Returns:
            Liste des notes trouvées
        """
        # Pattern pour trouver des notes (C, C#, Db, etc.)
        note_pattern = r'\b([A-G][#b]?)\b'
        matches = re.findall(note_pattern, text, re.IGNORECASE)
        return [self.normalize_note(note) for note in matches]
    
    def transpose_melody(self, notes: List[str], target_scale: str) -> Dict:
        """
        Transpose une mélodie vers une gamme cible
        
        Args:
            notes: Liste des notes à transposer
            target_scale: Nom de la gamme cible
            
        Returns:
            Dictionnaire avec les notes originales, transposées et les changements
        """
        if target_scale not in self.scales:
            return {
                'success': False,
                'error': f"La gamme '{target_scale}' n'existe pas"
            }
        
        transposed_notes = []
        changes = []
        
        for i, note in enumerate(notes):
            normalized_note = self.normalize_note(note)
            
            if self.is_note_in_scale(normalized_note, target_scale):
                transposed_notes.append(normalized_note)
                changes.append({
                    'position': i + 1,
                    'original': normalized_note,
                    'transposed': normalized_note,
                    'changed': False,
                    'reason': "Note déjà dans la gamme"
                })
            else:
                closest_note = self.find_closest_note_in_scale(normalized_note, target_scale)
                transposed_notes.append(closest_note)
                changes.append({
                    'position': i + 1,
                    'original': normalized_note,
                    'transposed': closest_note,
                    'changed': True,
                    'reason': f"Note transposée vers la note la plus proche"
                })
        
        return {
            'success': True,
            'original_notes': notes,
            'transposed_notes': transposed_notes,
            'target_scale': target_scale,
            'scale_description': self.scales[target_scale]['description'],
            'changes': changes,
            'change_count': sum(1 for c in changes if c['changed'])
        }
    
    def get_available_scales(self) -> List[Dict]:
        """
        Retourne la liste des gammes disponibles
        
        Returns:
            Liste des gammes avec leurs descriptions
        """
        return [
            {
                'name': name,
                'notes': config['notes'],
                'description': config['description']
            }
            for name, config in self.scales.items()
        ]
