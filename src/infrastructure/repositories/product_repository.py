from typing import List


class ProductRepository:
    """Repositorio de productos fitosanitarios disponibles."""

    _PRODUCTOS: List[str] = [
        "Acisol complex",
        "Aceite Agrícola Mineral 83%",
        "Aceite Emulsionable 90%",
        "Aceite Parafínico Agrícola",
        "Agrolite Oil",
        "Agromil",
        "Agrigent Plus",
        "Amistar",
        "Aminol",
        "Banole",
        "Basfoliar",
        "Bayfolan",
        "Bellis",
        "Biozyme",
        "Bravo",
        "Bacterol",
        "Cabrio",
        "Cari Gold",
        "Carrier",
        "Cavendish care",
        "Citroil",
        "Crop Oil Concentrate (COC)",
        "Cuprofix",
        "Cytogreen",
        "Dithane",
        "Foliup",
        "Folimax",
        "Humiplex",
        "Hidróxido de cobre",
        "Kasumin",
        "Kelatex",
        "Kanelcide",
        "Killbac Oil",
        "Mancozeb 80 WP (genéricos)",
        "Mimoten",
        "Mojave",
        "Mokave",
        "Nordox",
        "Nutre potasa",
        "Opera",
        "Oxicloruro de cobre",
        "Phyton",
        "Priori Xtra",
        "Saf-T-Side",
        "Score",
        "Serenade",
        "Stimulate",
        "Stratego",
        "Stylet Oil",
        "Sunspray Oil",
        "Tecamin",
        "Timorex Gold",
        "Tilt",
        "Otro",
    ]

    @classmethod
    def obtener_todos(cls) -> List[str]:
        """Retorna la lista de todos los productos disponibles."""
        return cls._PRODUCTOS.copy()
