import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        countryList = self._model.getAllCountries()
        # countryListDD = map(lambda x: ft.dropdown.Option(x),
        #                     countryList)
        # self._view.ddcountry.options = countryListDD
        for c in countryList:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))

        for i in range(2015, 2019):
            self._view.ddyear.options.append(ft.dropdown.Option(str(i)))

        self._view.update_page()

    def handle_graph(self, e):
        anno = self._view.ddyear.value
        country = self._view.ddcountry.value
        if anno is None or country is None:
            self._view.create_alert("Non lasciare i dropdown vuoti!")
            return
        self._model.buildGraph(country, anno)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {nNodes} "
                                                      f"Numero di archi: {nEdges}"))
        self._view.btn_volume.disabled = False
        self._view.update_page()

    def handle_volume(self, e):
        listRetailerVolume = self._model.getVolumiVendita()
        self._view.txtOut2.controls.clear()
        for element in listRetailerVolume:
            self._view.txtOut2.controls.append(ft.Text(f"{element[0].Retailer_name} --> {element[1]}"))
        self._view.update_page()

    def handle_path(self, e):
        try:
            N = int(self._view.txtN.value)
        except ValueError:
            self._view.create_alert("Inserisci un valore numerico!")
            return
        if N < 2:
            self._view.create_alert("Inserci un valore maggiore o uguale a 2")
            return

        self._model.computePath(N)

        self._view.txtOut3.controls.append(ft.Text(
            f"Peso cammino massimo: {str(self._model.solBest)}"))

        for ii in self._model.path_edge:
            self._view.txtOut3.controls.append(ft.Text(
                f"{ii[0].Retailer_name} --> {ii[1].Retailer_name}: {str(ii[2])}"))

        self._view.update_page()


