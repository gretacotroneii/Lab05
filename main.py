import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    input_tipo=ft.TextField(label='Tipo',expand=True)
    input_marca=ft.TextField(label='Marca',expand=True)
    input_anno=ft.TextField(label='Anno di acquisto',expand=True)
    input_valore=ft.TextField(label='Valore in euro',value='100.0',expand=True)

    #funzioni e bottoni per il contatore (+ e -)
    def decrementa_valore(e):
        try:
            val=float(input_valore.value)    #legge il valore e lo trasforma in decimale
            val=max(0.0,val-10.0)            #sottrae al valore attuale 10 euro, il 0.0 serve per non andare sotto allo 0 ed evitare valori negativi
            input_valore.value=str(val)      #ritrasformo il numero in stringa
            input_valore.update()            #aggiorna il prezzo, mostrando quello ribassato
        except ValueError:
            input_valore.value='100.0'       #se c'era un errore nella casella, si ritorna al valore predefinito 100.0, aggiornandolo sullo schermo
            input_valore.update()

    def incrementa_valore(e):
        try:
            val=float(input_valore.value)
            val=val+10.0                    #incrementa il valore di 10 euro
            input_valore.value=str(val)
            input_valore.update()
        except ValueError:
            input_valore.value='100.0'
            input_valore.update()

    #creo i due pulsanti + e - che poi l'utente può cliccare sullo schermo
    btn_meno=ft.Button('-',on_click=decrementa_valore)
    btn_piu=ft.Button('+',on_click=incrementa_valore)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        lista_strumenti.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        txt_responsabile.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def aggiungi_nuovo_strumento(e):
        tipo=input_tipo.value.strip()
        marca=input_marca.value.strip()
        anno_stringa=input_anno.value.strip()
        valore_stringa=input_valore.value.strip()

        #controllo se ci sono campi vuoti
        if not tipo or not marca or not anno_stringa or not valore_stringa:
            alert.show_alert('Errore: Tutti i campi devono essere compilati')
            return

        #controllo che l'anno sia un valore intero
        try:
            anno_acquisto=int(anno_stringa)
        except ValueError:
            alert.show_alert('Errore: Anno di acquisto deve essere un numero intero valido')
            return

        #controllo la validità del valore
        try:
            valore=float(valore_stringa)
        except ValueError:
            alert.show_alert('Errore: Il valore in euro deve essere un numero valido')
            return

        #chiamo al metodo già presente dal Lab03 per aggiungere lo strumento
        deposito.aggiungi_strumento(tipo, marca, anno_acquisto, valore)

        #svuoto i campi e resetto al valore predefinito
        input_tipo.value=''
        input_marca.value=''
        input_anno.value=''
        input_valore.value='100.00'
        page.update()

        #chiamo la funzione che aggiorna la schermata degli strumenti
        aggiorna_lista_strumenti()


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_aggiungi=ft.Button('Aggiungi Strumento',on_click=aggiungi_nuovo_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Text('Aggiungi Nuovo Strumento',size=20),    #creo l'"etichetta" di testo
        #creo le righe orizzontale con la lista di oggetti che vogliamo affiancati in questa riga
        ft.Row(controls=[input_tipo,input_marca]),
        ft.Row(controls=[input_anno,input_valore,btn_meno,btn_piu]),
        ft.Row(controls=[pulsante_aggiungi]),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
