"""
Application console pour l'agent musical Azure OpenAI
"""
import os
import sys
import yaml
from dotenv import load_dotenv
from colorama import init, Fore, Style
from agent import MusicAgent


# Initialiser colorama pour les sorties colorées
init(autoreset=True)


def print_banner():
    """Affiche la bannière de bienvenue"""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          🎵  AGENT MUSICAL AZURE OPENAI  🎵              ║
║                                                           ║
║     Adaptation intelligente de partitions musicales      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)


def load_config():
    """
    Charge la configuration depuis config.yaml
    
    Returns:
        Dictionnaire de configuration
    """
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Erreur: Le fichier config.yaml est introuvable{Style.RESET_ALL}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"{Fore.RED}❌ Erreur lors du parsing de config.yaml: {e}{Style.RESET_ALL}")
        sys.exit(1)


def check_environment():
    """Vérifie que les variables d'environnement Azure sont configurées"""
    required_vars = [
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_API_KEY',
        'AZURE_OPENAI_DEPLOYMENT_NAME',
        'AZURE_OPENAI_API_VERSION'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"{Fore.RED}❌ Variables d'environnement manquantes:{Style.RESET_ALL}")
        for var in missing_vars:
            print(f"   - {var}")
        print(f"\n{Fore.YELLOW}📝 Instructions:{Style.RESET_ALL}")
        print("1. Copiez le fichier .env.example vers .env")
        print("2. Remplissez vos credentials Azure OpenAI dans le fichier .env")
        print("3. Relancez l'application")
        sys.exit(1)


def print_help():
    """Affiche l'aide des commandes disponibles"""
    help_text = f"""
{Fore.CYAN}Commandes disponibles:{Style.RESET_ALL}

  {Fore.GREEN}/help{Style.RESET_ALL}       - Affiche cette aide
  {Fore.GREEN}/gammes{Style.RESET_ALL}     - Liste les gammes configurées
  {Fore.GREEN}/clear{Style.RESET_ALL}      - Efface l'historique de conversation
  {Fore.GREEN}/history{Style.RESET_ALL}    - Affiche l'historique de conversation
  {Fore.GREEN}/quit{Style.RESET_ALL}       - Quitte l'application

{Fore.CYAN}Exemples d'utilisation:{Style.RESET_ALL}

  • "Quelles gammes sont disponibles ?"
  • "Transpose cette mélodie C, D, E, F, G vers la gamme de sol majeur"
  • "Adapte la partition C, E, G, B, D vers re_mineur"
  • "Est-ce que la note F# est dans la gamme de do majeur ?"
  • "Voici une mélodie: A B C# D E. Transpose-la vers la_mineur"
    """
    print(help_text)


def display_scales(config):
    """Affiche les gammes configurées"""
    print(f"\n{Fore.CYAN}Gammes configurées:{Style.RESET_ALL}\n")
    for scale_name, scale_info in config['gammes'].items():
        print(f"{Fore.GREEN}• {scale_name}{Style.RESET_ALL}")
        print(f"  Notes: {', '.join(scale_info['notes'])}")
        print(f"  Description: {scale_info['description']}\n")


def display_history(agent: MusicAgent):
    """Affiche l'historique de conversation"""
    history = agent.get_conversation_history()
    if not history:
        print(f"{Fore.YELLOW}Aucun historique disponible{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}Historique de conversation:{Style.RESET_ALL}\n")
    for i, msg in enumerate(history):
        if msg.type == "human":
            print(f"{Fore.BLUE}👤 Vous:{Style.RESET_ALL} {msg.content}")
        elif msg.type == "ai":
            print(f"{Fore.GREEN}🤖 Agent:{Style.RESET_ALL} {msg.content}")
        print()


def main():
    """Fonction principale de l'application console"""
    print_banner()
    
    # Charger les variables d'environnement
    load_dotenv()
    
    # Vérifier la configuration Azure
    check_environment()
    
    # Charger la configuration
    print(f"{Fore.YELLOW}📁 Chargement de la configuration...{Style.RESET_ALL}")
    config = load_config()
    
    # Initialiser l'agent
    print(f"{Fore.YELLOW}🤖 Initialisation de l'agent musical...{Style.RESET_ALL}")
    try:
        agent = MusicAgent(config)
        print(f"{Fore.GREEN}✓ Agent initialisé avec succès!{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}❌ Erreur lors de l'initialisation de l'agent: {e}{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"{Fore.CYAN}Tapez /help pour voir les commandes disponibles{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Tapez /quit pour quitter{Style.RESET_ALL}\n")
    
    # Boucle principale
    while True:
        try:
            # Obtenir l'entrée utilisateur
            user_input = input(f"{Fore.BLUE}👤 Vous > {Style.RESET_ALL}").strip()
            
            if not user_input:
                continue
            
            # Traiter les commandes spéciales
            if user_input.lower() == '/quit':
                print(f"\n{Fore.CYAN}👋 Au revoir!{Style.RESET_ALL}")
                break
            
            elif user_input.lower() == '/help':
                print_help()
                continue
            
            elif user_input.lower() == '/gammes':
                display_scales(config)
                continue
            
            elif user_input.lower() == '/clear':
                agent.clear_memory()
                print(f"{Fore.GREEN}✓ Historique effacé{Style.RESET_ALL}\n")
                continue
            
            elif user_input.lower() == '/history':
                display_history(agent)
                continue
            
            # Exécuter l'agent
            print(f"\n{Fore.YELLOW}🤔 L'agent réfléchit...{Style.RESET_ALL}\n")
            response = agent.run(user_input)
            
            # Afficher la réponse
            print(f"\n{Fore.GREEN}🤖 Agent:{Style.RESET_ALL}\n{response}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.CYAN}👋 Au revoir!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"\n{Fore.RED}❌ Erreur: {e}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
