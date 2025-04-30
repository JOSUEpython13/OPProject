'''
Autor: Josue Solano Redondo
Fecha: 03/20/2025
Version 1.0
Proyecto OP
'''
import os
from ExtractSetLinks import ExtractSetLinks, Extract_data_sets, save_set_links, load_set_links
from ExtractCardInfo import extract_card_info, extract_card_images, generate_card_htmls, generate_index_html
from ValidateStats import validate_deck, export_deck_to_html_with_images, plot_deck_cost_curve, plot_deck_type_distribution, plot_deck_color_distribution

def limpiar_pantalla():
    #Limpia pantalla de la terminal en ejecucion
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPresione ENTER para continuar.....")

#Menu Principal
def menu():
    #variable del sistema   
    set_links = []
    while True:
        print("\n******* Menu Principal *******")
        print("1. EXTRAER SETs")
        print("2. EXTRAER INFO SETs")
        print("3. CARD INFO")
        print("4. EXTRAER IMAGENES")
        print("5. GENERAR HTMLs")
        print("6. GENERAR INDEX")
        print("7. DECKS") 
        print("8. EXPORTAR DECK")
        print("9. CURVA DE COSTE DEL DECK")
        print("10. DISTRIBUCIÓN DE COLORES DEL DECK")
        print("11. DISTRIBUCIÓN DE TIPOS DE CARTA")
        print("12. Salir del sistema")
        opcion = input("Ingrese una opcion: ")
        
        if opcion == "1":
            limpiar_pantalla()
            print("\n ***** EXTRAER SETs *****")
            set_links = []
            ExtractSetLinks(set_links)
            save_set_links(set_links)
            pausar()
            
        elif opcion == "2":
            limpiar_pantalla()
            print("\n ***** EXTRAER INFO SETs *****")
            set_links = load_set_links()
            Extract_data_sets(set_links)
            pausar()
            
        elif opcion == "3":
            limpiar_pantalla()
            print("\n **** CARD INFO *****")
            extract_card_info()
            pausar()
        
        elif opcion == "4":
            limpiar_pantalla()
            print("\n **** IMAGENES *****")
            extract_card_images()
            pausar()
            
        elif opcion == "5":
            limpiar_pantalla()
            print("\n **** HTML *****")
            generate_card_htmls()
            pausar()

        elif opcion == "6":
            limpiar_pantalla()
            print("\n **** INDEX *****")
            generate_index_html()
            pausar()

        elif opcion == "7":
            limpiar_pantalla()
            print("\n **** VALIDAR DECK*****")
            validate_deck()
            pausar()
            
        elif opcion == "8":
            limpiar_pantalla()
            print("\n **** EXPORTAR DECK A HTML *****")
            export_deck_to_html_with_images()
            pausar()
            
        elif opcion == "9":
            limpiar_pantalla()
            print("\n **** CURVA DE COSTE *****")
            from ValidateStats import plot_deck_cost_curve
            plot_deck_cost_curve()
            pausar()
        
        elif opcion == "10":
            limpiar_pantalla()
            print("\n **** COLORES DEL DECK *****")
            from ValidateStats import plot_deck_color_distribution
            plot_deck_color_distribution()
            pausar()

        elif opcion == "11":
            limpiar_pantalla()
            print("\n **** TIPOS DE CARTA *****")
            from ValidateStats import plot_deck_type_distribution
            plot_deck_type_distribution()
            pausar()
                    
        elif opcion == "12":
            print("\n Gracias por usar el sistema, vuelva pronto!!")            
            break # - Cierre del sistema
        
        else:
            
            print("Opcion no valida. Intente nuevamente")
            pausar()
            
#Ejecucion del sistema
if __name__ == "__main__":
    print("BIENVENIDO AL SISTEMA")
    menu()
