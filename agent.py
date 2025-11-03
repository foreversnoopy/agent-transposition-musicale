"""
Agent musical Azure OpenAI avec LangChain
"""
import os
from typing import Dict, List, Optional
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import StructuredTool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
from music_tools import MusicTools


class MusicAgent:
    """Agent musical utilisant Azure OpenAI pour adapter des partitions"""
    
    def __init__(self, config: Dict):
        """
        Initialise l'agent musical
        
        Args:
            config: Configuration complète (gammes, agent, etc.)
        """
        self.config = config
        self.music_tools = MusicTools(config['gammes'])
        
        # Initialiser le client Azure OpenAI
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
            deployment_name=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
            temperature=config['agent']['temperature'],
            max_tokens=config['agent']['max_tokens']
        )
        
        # Initialiser la mémoire conversationnelle
        memory_config = config['memory']
        if memory_config['type'] == 'buffer':
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="output"
            )
        else:
            self.memory = None
        
        # Créer les outils pour l'agent
        self.tools = self._create_tools()
        
        # Créer le system prompt avec les gammes disponibles
        available_scales = ", ".join(config['gammes'].keys())
        system_prompt = config['agent']['system_prompt'].format(
            available_scales=available_scales
        )
        
        # Créer le prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Créer l'agent
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Créer l'executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            return_intermediate_steps=True,
            handle_parsing_errors=True
        )
    
    def _create_tools(self) -> List[StructuredTool]:
        """
        Crée les outils (functions) disponibles pour l'agent
        
        Returns:
            Liste des outils LangChain
        """
        tools = []
        
        # Outil 1: Lister les gammes disponibles
        def list_scales_tool() -> str:
            """Liste toutes les gammes de notes disponibles dans la configuration"""
            scales = self.music_tools.get_available_scales()
            result = "Gammes disponibles:\n\n"
            for scale in scales:
                result += f"- {scale['name']}: {scale['notes']}\n"
                result += f"  Description: {scale['description']}\n\n"
            return result
        
        tools.append(StructuredTool.from_function(
            func=list_scales_tool,
            name="list_available_scales",
            description="Liste toutes les gammes de notes disponibles. Utilise cet outil quand tu as besoin de connaître les gammes configurées."
        ))
        
        # Outil 2: Vérifier si une note est dans une gamme
        def check_note_in_scale(note: str, scale_name: str) -> str:
            """Vérifie si une note est dans une gamme spécifique"""
            is_in_scale = self.music_tools.is_note_in_scale(note, scale_name)
            if is_in_scale:
                return f"✓ La note {note} est dans la gamme {scale_name}"
            else:
                closest = self.music_tools.find_closest_note_in_scale(note, scale_name)
                return f"✗ La note {note} n'est PAS dans la gamme {scale_name}. Note la plus proche: {closest}"
        
        tools.append(StructuredTool.from_function(
            func=check_note_in_scale,
            name="check_note_in_scale",
            description="Vérifie si une note spécifique est dans une gamme donnée. Paramètres: note (ex: 'C#'), scale_name (ex: 'do_majeur')"
        ))
        
        # Outil 3: Transposer une mélodie
        def transpose_melody(notes_str: str, target_scale: str) -> str:
            """Transpose une série de notes vers une gamme cible"""
            # Parser les notes depuis la chaîne
            notes = [n.strip() for n in notes_str.split(',') if n.strip()]
            
            if not notes:
                return "Erreur: Aucune note fournie"
            
            result = self.music_tools.transpose_melody(notes, target_scale)
            
            if not result['success']:
                return f"Erreur: {result['error']}"
            
            output = f"=== TRANSPOSITION VERS {target_scale.upper()} ===\n\n"
            output += f"Gamme cible: {result['scale_description']}\n"
            output += f"Notes de la gamme: {', '.join(self.music_tools.get_scale_notes(target_scale))}\n\n"
            output += f"Notes originales: {', '.join(result['original_notes'])}\n"
            output += f"Notes transposées: {', '.join(result['transposed_notes'])}\n\n"
            output += f"Nombre de changements: {result['change_count']}/{len(notes)}\n\n"
            
            if result['change_count'] > 0:
                output += "Détails des changements:\n"
                for change in result['changes']:
                    if change['changed']:
                        output += f"  Position {change['position']}: {change['original']} → {change['transposed']} ({change['reason']})\n"
            else:
                output += "Aucune note n'a été modifiée - toutes les notes étaient déjà dans la gamme cible.\n"
            
            return output
        
        tools.append(StructuredTool.from_function(
            func=transpose_melody,
            name="transpose_melody_to_scale",
            description="Transpose une mélodie (série de notes) vers une gamme cible. Paramètres: notes_str (notes séparées par des virgules, ex: 'C,D,E,F'), target_scale (nom de la gamme)"
        ))
        
        # Outil 4: Extraire des notes d'un texte
        def extract_notes(text: str) -> str:
            """Extrait les notes musicales d'un texte"""
            notes = self.music_tools.parse_notes_from_text(text)
            if notes:
                return f"Notes détectées: {', '.join(notes)}"
            else:
                return "Aucune note détectée dans le texte"
        
        tools.append(StructuredTool.from_function(
            func=extract_notes,
            name="extract_notes_from_text",
            description="Extrait et identifie les notes musicales présentes dans un texte. Utilise cet outil pour parser des partitions au format texte."
        ))
        
        return tools
    
    def run(self, user_input: str) -> str:
        """
        Exécute l'agent avec une entrée utilisateur
        
        Args:
            user_input: Question ou commande de l'utilisateur
            
        Returns:
            Réponse de l'agent
        """
        try:
            response = self.agent_executor.invoke({
                "input": user_input
            })
            return response['output']
        except Exception as e:
            return f"Erreur lors de l'exécution: {str(e)}"
    
    def clear_memory(self):
        """Efface la mémoire conversationnelle"""
        if self.memory:
            self.memory.clear()
    
    def get_conversation_history(self) -> List:
        """Retourne l'historique de la conversation"""
        if self.memory:
            return self.memory.chat_memory.messages
        return []
