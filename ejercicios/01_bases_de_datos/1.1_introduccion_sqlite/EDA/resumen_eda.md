# Resumen EDA tienda informática

Archivos analizados: 25

## Columnas comunes entre todos los CSV

name, price


## Categorías (basadas en nombres de archivo)

- case
- case-accessory
- case-fan
- cpu
- cpu-cooler
- external-hard-drive
- fan-controller
- headphones
- internal-hard-drive
- keyboard
- memory
- monitor
- motherboard
- mouse
- optical-drive
- os
- power-supply
- sound-card
- speakers
- thermal-paste
- ups
- video-card
- webcam
- wired-network-card
- wireless-network-card


## Resumen por archivo

### case-accessory.csv

- Filas: 8, Columnas: 4
- Columnas: name, price, type, form_factor
- Columnas numéricas: price, form_factor
- Columnas categóricas: name, type
- Fabricantes detectados (ejemplos): NZXT, Unitech, Vantec, nMEDIAPC

### case-fan.csv

- Filas: 2181, Columnas: 8
- Columnas: name, price, size, color, rpm, airflow, noise_level, pwm
- Columnas numéricas: price, size
- Columnas categóricas: name, color, rpm, airflow, noise_level, pwm
- Fabricantes detectados (ejemplos): ADATA, APNX, ARCTIC, Aerocool, Akasa, Alpenföhn, Anidees, Antec, Apevia, Asiahorse
- Colores detectados: Black, Black / Blue, Black / Brown, Black / Clear, Black / Gray, Black / Green, Black / Multicolor, Black / Orange, Black / Pink, Black / Purple, Black / Red, Black / Silver, Black / Teal, Black / Translucent Black, Black / Translucent White, Black / Transparent, Black / White, Black / Yellow, Blue, Blue / Black, Blue / White, Brown, Brown / Black, Clear, Clear / Blue, Gray, Gray / Black, Gray / Blue, Gray / White, Green, Green / Black, Multicolor, Orange, Pink, Pink / White, Purple, Red, Red / Black, Silver, Silver / Black, Teal / White, Translucent Black, Translucent Blue, Translucent Gray, Translucent White, Translucent Yellow, Transparent, Turquoise, UV Blue, UV Green, White, White / Black, White / Blue, White / Gray, White / Red, White / Silver, White / Translucent White, White / Transparent, Yellow, Yellow / Black, Yellow / Gray

### case.csv

- Filas: 5486, Columnas: 8
- Columnas: name, price, type, color, psu, side_panel, external_volume, internal_35_bays
- Columnas numéricas: price, psu, external_volume, internal_35_bays
- Columnas categóricas: name, type, color, side_panel
- Fabricantes detectados (ejemplos): ABKONCORE, ABS, ADATA, APNX, AQIRYS, Aerocool, Anidees, Antec, Apevia, Apex
- Colores detectados: Beige, Beige / Gray, Black, Black / Black, Black / Blue, Black / Brown, Black / Clear, Black / Gold, Black / Gray, Black / Green, Black / Multicolor, Black / Orange, Black / Pink, Black / Purple, Black / Red, Black / Silver, Black / White, Black / Yellow, Blue, Blue / Black, Blue / Red, Blue / Silver, Blue / Yellow, Brown, Camo, Clear, Cyan / Black, Gold, Gold / Black, Gold / White, Gray, Gray / Black, Gray / Orange, Gray / Silver, Green, Green / Black, Green / Blue, Green / Brown, Green / Silver, Green / White, Gunmetal, Multicolor, Orange, Orange / Black, Orange / Silver, Orange / White, Pink, Pink / Black, Pink / Silver, Pink / White, Purple, Purple / Black, Purple / Blue, Red, Red / Black, Red / Blue, Red / Silver, Red / White, Silver, Silver / Black, Silver / Brown, Silver / Gray, Silver / Multicolor, Silver / Orange, Silver / White, Turquoise, Turquoise / Black, White, White / Black, White / Blue, White / Brown, White / Gold, White / Gray, White / Green, White / Multicolor, White / Pink, White / Purple, White / Red, White / Silver, Yellow, Yellow / Black, Yellow / Red

### cpu-cooler.csv

- Filas: 2166, Columnas: 6
- Columnas: name, price, rpm, noise_level, color, size
- Columnas numéricas: price, size
- Columnas categóricas: name, rpm, noise_level, color
- Fabricantes detectados (ejemplos): ADATA, AMD, APNX, ARCTIC, ARESGAME, Aerocool, Akasa, Alpenföhn, Alphacool, Antec
- Colores detectados: Beige / Brown, Black, Black / Blue, Black / Gray, Black / Multicolor, Black / Orange, Black / Red, Black / Silver, Black / Teal, Black / Translucent White, Black / White, Black / Yellow, Blue, Blue / Black, Blue / Silver, Blue / White, Brown, Brown / Beige, Brown / Black, Brown / Silver, Gray, Gray / Black, Gray / Silver, Green, Green / Black, Orange, Orange / Brown, Orange / Red, Orange / Silver, Pink, Pink / Purple, Red / Black, Red / Silver, Silver, Silver / Beige, Silver / Black, Silver / Gray, Silver / Red, Silver / Teal, Teal, Teal / Silver, White, White / Black, White / Gray, White / Orange, White / Pink, White / Silver, Yellow / Black

### cpu.csv

- Filas: 1353, Columnas: 8
- Columnas: name, price, core_count, core_clock, boost_clock, tdp, graphics, smt
- Columnas numéricas: price, core_count, core_clock, boost_clock, tdp
- Columnas categóricas: name, graphics, smt
- Fabricantes detectados (ejemplos): AMD, Intel

### external-hard-drive.csv

- Filas: 519, Columnas: 7
- Columnas: name, price, type, interface, capacity, price_per_gb, color
- Columnas numéricas: price, capacity, price_per_gb
- Columnas categóricas: name, type, interface, color
- Fabricantes detectados (ejemplos): ADATA, Apacer, Apricom, Asus, Axiom, Buffalo, Buslink, Corsair, Crucial, Edge
- Colores detectados: Beige, Black, Black / Orange, Black / Silver, Black / Yellow, Blue, Blue / Silver, Blue / White, Gold, Gray, Orange / Silver, Red, Red / Silver, Silver, White

### fan-controller.csv

- Filas: 37, Columnas: 7
- Columnas: name, price, channels, channel_wattage, pwm, form_factor, color
- Columnas numéricas: price, channels, channel_wattage
- Columnas categóricas: name, pwm, form_factor, color
- Fabricantes detectados (ejemplos): Aerocool, BitFenix, Deepcool, Gelid, Kingwin, Lamptron, NZXT, Scythe, Silverstone, Thermaltake
- Colores detectados: Black

### headphones.csv

- Filas: 2746, Columnas: 8
- Columnas: name, price, type, frequency_response, microphone, wireless, enclosure_type, color
- Columnas numéricas: price
- Columnas categóricas: name, type, frequency_response, microphone, wireless, enclosure_type, color
- Fabricantes detectados (ejemplos): 1MORE, A4Tech, ADATA, AKG, AOC, ARCTIC, AZIO, Acer, Adesso, Altec
- Colores detectados: Beige, Beige / Black, Beige / Blue, Beige / Silver, Black, Black / Beige, Black / Blue, Black / Brown, Black / Clear, Black / Copper, Black / Gold, Black / Gray, Black / Green, Black / Orange, Black / Pink, Black / Purple, Black / Red, Black / Silver, Black / White, Black / Yellow, Blue, Blue / Black, Blue / Pink, Blue / Silver, Blue / White, Brown, Brown / Beige, Brown / Black, Camo, Camo / Black, Clear, Copper / Black, Gold, Gold / Black, Gold / Silver, Gray, Gray / Black, Gray / Brown, Gray / Cyan, Gray / Green, Gray / White, Green, Green / Black, Green / Blue, Green / Gold, Green / Purple, Green / White, Gunmetal, Multicolor, Orange, Orange / White, Pink, Pink / Black, Pink / Gray, Pink / Silver, Pink / White, Purple, Purple / Black, Purple / Green, Red, Red / Amber, Red / Black, Red / Blue, Red / Silver, Red / White, Silver, Silver / Beige, Silver / Black, Silver / Blue, Silver / Brown, Silver / Purple, Silver / White, Translucent Black, Translucent Blue, Transparent, White, White / Beige, White / Black, White / Blue, White / Brown, White / Gray, White / Green, White / Pink, White / Purple, White / Red, White / Silver, Yellow, Yellow / Gray

### internal-hard-drive.csv

- Filas: 5705, Columnas: 8
- Columnas: name, price, capacity, price_per_gb, type, cache, form_factor, interface
- Columnas numéricas: price, capacity, price_per_gb, cache
- Columnas categóricas: name, type, form_factor, interface
- Fabricantes detectados (ejemplos): ADATA, AITC, AMD, Acer, Addlink, Angelbird, Apacer, Apotop, Asura, Asus

### keyboard.csv

- Filas: 2970, Columnas: 8
- Columnas: name, price, style, switches, backlit, tenkeyless, connection_type, color
- Columnas numéricas: price
- Columnas categóricas: name, style, switches, backlit, tenkeyless, connection_type, color
- Fabricantes detectados (ejemplos): 1STPLAYER, A4Tech, ADATA, AOC, ARCTIC, AUKEY, AZIO, Acco, Acer, Adesso
- Colores detectados: Beige, Beige / Gray, Beige / Green, Black, Black / Beige, Black / Blue, Black / Gold, Black / Gray, Black / Green, Black / Purple, Black / Red, Black / Silver, Black / White, Black / Yellow, Blue, Blue / Black, Blue / White, Camo, Gold / Black, Gold / White, Gray, Gray / Black, Gray / White, Green / Black, Green / White, Gunmetal, Multicolor, Orange / White, Pink, Pink / Green, Pink / White, Purple, Purple / Pink, Purple / White, Red, Red / White, Silver, Silver / Black, Silver / Gray, Silver / White, Translucent Black, White, White / Black, White / Blue, White / Gray, White / Pink, White / Silver, Yellow

### memory.csv

- Filas: 11734, Columnas: 8
- Columnas: name, price, speed, modules, price_per_gb, color, first_word_latency, cas_latency
- Columnas numéricas: price, price_per_gb, first_word_latency, cas_latency
- Columnas categóricas: name, speed, modules, color
- Fabricantes detectados (ejemplos): ADATA, AMD, Acer, Addlink, Antec, Apacer, Apotop, Avexir, Compustocx, Corsair
- Colores detectados: Beige, Black, Black / Black, Black / Blue, Black / Camo, Black / Gold, Black / Gray, Black / Green, Black / Orange, Black / Purple, Black / Red, Black / Silver, Black / White, Black / Yellow, Blue, Blue / Black, Blue / Orange, Blue / Silver, Blue / White, Camo, Camo / Black, Gold, Gold / Black, Gray, Gray / Black, Gray / Orange, Gray / Red, Gray / Silver, Gray / White, Green, Green / Black, Green / Blue, Green / Silver, Multicolor, Orange, Orange / White, Pink / Silver, Platinum, Red, Red / Amber, Red / Black, Red / Blue, Red / Silver, Red / White, Silver, Silver / Black, Silver / Blue, Silver / Camo, Silver / Gray, Silver / Green, Silver / Red, Silver / White, White, White / Black, White / Blue, White / Camo, White / Gold, White / Gray, White / Purple, White / Red, White / Silver, Yellow, Yellow / Black

### monitor.csv

- Filas: 4216, Columnas: 8
- Columnas: name, price, screen_size, resolution, refresh_rate, response_time, panel_type, aspect_ratio
- Columnas numéricas: price, screen_size, refresh_rate, response_time
- Columnas categóricas: name, resolution, panel_type, aspect_ratio
- Fabricantes detectados (ejemplos): 3M, AOC, AOPEN, ASRock, AXM, Acer, Achieva, Alienware, Apple, Asus

### motherboard.csv

- Filas: 4358, Columnas: 7
- Columnas: name, price, socket, form_factor, max_memory, memory_slots, color
- Columnas numéricas: price, max_memory, memory_slots
- Columnas categóricas: name, socket, form_factor, color
- Fabricantes detectados (ejemplos): ASRock, Asus, Biostar, Colorful, ECS, EVGA, Foxconn, Gigabyte, Intel, Jetway
- Colores detectados: Beige, Beige / Red, Black, Black / Beige, Black / Blue, Black / Copper, Black / Gold, Black / Gray, Black / Green, Black / Multicolor, Black / Orange, Black / Pink, Black / Red, Black / Silver, Black / White, Black / Yellow, Blue, Blue / Black, Blue / Red, Blue / Silver, Blue / White, Brown, Brown / Black, Brown / Gray, Brown / Red, Brown / Silver, Brown / Yellow, Camo, Gold / Black, Gray / Black, Gray / Brown, Green, Green / Black, Green / Blue, Green / Silver, Green / White, Multicolor, Orange / Black, Orange / White, Purple / Black, Purple / Green, Red, Red / Black, Silver, Silver / Black, Silver / Brown, Silver / Copper, Silver / Gold, Silver / Gray, Silver / Orange, Silver / Red, Silver / White, Translucent Black, White, White / Black, White / Blue, White / Gray, White / Silver, Yellow, Yellow / Black

### mouse.csv

- Filas: 2355, Columnas: 7
- Columnas: name, price, tracking_method, connection_type, max_dpi, hand_orientation, color
- Columnas numéricas: price, max_dpi
- Columnas categóricas: name, tracking_method, connection_type, hand_orientation, color
- Fabricantes detectados (ejemplos): 3Dconnexion, 3M, A4Tech, ABKONCORE, ACGAM, ADATA, AOC, AZIO, Acco, Acer
- Colores detectados: Beige, Beige / Black, Black, Black / Blue, Black / Copper, Black / Cyan, Black / Gold, Black / Gray, Black / Green, Black / Multicolor, Black / Orange, Black / Pink, Black / Purple, Black / Red, Black / Silver, Black / White, Black / Yellow, Blue, Blue / Black, Blue / Gray, Blue / Green, Blue / Pink, Blue / Silver, Blue / White, Brown, Brown / Black, Camo, Cyan / Black, Gold, Gold / Black, Gray, Gray / Black, Gray / Blue, Gray / Silver, Gray / White, Gray / Yellow, Green, Green / Black, Green / Blue, Green / Gold, Green / Silver, Green / White, Gunmetal, Multicolor, Orange, Orange / Black, Orange / Red, Orange / White, Pink, Pink / Black, Pink / Gray, Pink / White, Purple, Purple / Black, Purple / Multicolor, Purple / Silver, Purple / White, Purple / Yellow, Red, Red / Black, Red / Blue, Red / Silver, Red / White, Silver, Silver / Beige, Silver / Black, Silver / Blue, Silver / White, Translucent Black / Black, Translucent Gray / Green, Transparent / Black, Transparent / Gray, White, White / Beige, White / Black, White / Blue, White / Gold, White / Gray, White / Multicolor, White / Pink, White / Purple, White / Red, White / Silver, White / Yellow, Yellow, Yellow / Black

### optical-drive.csv

- Filas: 227, Columnas: 8
- Columnas: name, price, bd, dvd, cd, bd_write, dvd_write, cd_write
- Columnas numéricas: price, bd, dvd, cd
- Columnas categóricas: name, bd_write, dvd_write, cd_write
- Fabricantes detectados (ejemplos): Archgon, Asus, Buslink, EVGA, Gear, HP, I/O, LG, Lenovo, Lite-On

### os.csv

- Filas: 62, Columnas: 4
- Columnas: name, price, mode, max_memory
- Columnas numéricas: price, max_memory
- Columnas categóricas: name, mode
- Fabricantes detectados (ejemplos): Microsoft

### power-supply.csv

- Filas: 2805, Columnas: 7
- Columnas: name, price, type, efficiency, wattage, modular, color
- Columnas numéricas: price, wattage
- Columnas categóricas: name, type, efficiency, modular, color
- Fabricantes detectados (ejemplos): ABS, ADATA, ARESGAME, Aerocool, Anima, Antec, Apevia, Apex, Asus, Athena
- Colores detectados: Black, Black / Blue, Black / Copper, Black / Gold, Black / Gray, Black / Green, Black / Multicolor, Black / Orange, Black / Purple, Black / Red, Black / Silver, Black / Teal, Black / White, Black / Yellow, Blue / Black, Gray, Orange / Black, Silver, Silver / Black, White, White / Black, White / Gray, White / Silver

### sound-card.csv

- Filas: 77, Columnas: 8
- Columnas: name, price, channels, digital_audio, snr, sample_rate, chipset, interface
- Columnas numéricas: price, channels, digital_audio, snr, sample_rate
- Columnas categóricas: name, chipset, interface
- Fabricantes detectados (ejemplos): Asus, Creative, Diamond, EVGA, Encore, HT, M-Audio, PPA, PowerColor, Rosewill

### speakers.csv

- Filas: 268, Columnas: 6
- Columnas: name, price, configuration, wattage, frequency_response, color
- Columnas numéricas: price, configuration, wattage
- Columnas categóricas: name, frequency_response, color
- Fabricantes detectados (ejemplos): ADAM, Altec, AmazonBasics, Audioengine, Avermedia, Behringer, Bose, Corsair, Creative, Cyber
- Colores detectados: Black, Black / Beige, Black / Blue, Black / Brown, Black / Copper, Black / Gold, Black / Gray, Black / Green, Black / Red, Black / Silver, Blue / Black, Brown / Black, Green / Black, Red / Black, Silver / Black, White, White / Black, White / Brown, White / Copper, White / White

### thermal-paste.csv

- Filas: 149, Columnas: 3
- Columnas: name, price, amount
- Columnas numéricas: price, amount
- Columnas categóricas: name
- Fabricantes detectados (ejemplos): ARCTIC, Akasa, Antec, Arctic, Biostar, CRYORIG, Cooler, Coollaboratory, Corsair, Deepcool

### ups.csv

- Filas: 683, Columnas: 4
- Columnas: name, price, capacity_w, capacity_va
- Columnas numéricas: price, capacity_w, capacity_va
- Columnas categóricas: name
- Fabricantes detectados (ejemplos): APC, Belkin, CyberPower, Eaton, Fellowes, Fujitsu, HP, IBM, Lenovo, PowerWalker

### video-card.csv

- Filas: 5811, Columnas: 8
- Columnas: name, price, chipset, memory, core_clock, boost_clock, color, length
- Columnas numéricas: price, memory, core_clock, boost_clock, length
- Columnas categóricas: name, chipset, color
- Fabricantes detectados (ejemplos): AMD, ASRock, ATI, Acer, Asus, BFG, Biostar, Club, Colorful, Corsair
- Colores detectados: Beige, Black, Black / Beige, Black / Black, Black / Blue, Black / Clear, Black / Gold, Black / Gray, Black / Green, Black / Orange, Black / Purple, Black / Red, Black / Silver, Black / White, Black / Yellow, Blue, Blue / Black, Blue / Gold, Blue / Gray, Blue / Red, Blue / Silver, Blue / White, Brown, Brown / Beige, Brown / Black, Clear / Black, Gold, Gold / Black, Gold / Blue, Gold / White, Gray, Gray / Black, Gray / Blue, Green, Green / Black, Green / Blue, Green / Silver, Orange / Black, Pink, Purple / Blue, Purple / Green, Red, Red / Black, Red / Blue, Red / Silver, Red / White, Silver, Silver / Black, Silver / Blue, Silver / Green, Silver / Red, Silver / White, Silver / Yellow, Translucent Black, Translucent Blue, Transparent, Transparent / Black, White, White / Black, White / Blue, White / Gray, White / Orange, White / Pink, White / Red, White / Silver, Yellow / Black

### webcam.csv

- Filas: 65, Columnas: 7
- Columnas: name, price, resolutions, connection, focus_type, os, fov
- Columnas numéricas: price, fov
- Columnas categóricas: name, resolutions, connection, focus_type, os
- Fabricantes detectados (ejemplos): AUKEY, Adesso, Anker, Asus, Avermedia, Creative, Elgato, Green, Insta360, Logitech

### wired-network-card.csv

- Filas: 133, Columnas: 4
- Columnas: name, price, interface, color
- Columnas numéricas: price
- Columnas categóricas: name, interface, color
- Fabricantes detectados (ejemplos): Acer, Asus, Belkin, Cisco, D-Link, EDUP, Edimax, Gigabyte, HP, Intel
- Colores detectados: Black, Black / Gold, Black / Silver, Black / White, Blue, Blue / Silver, Green, Green / Black, Green / Copper, Green / Silver, Red, Silver / Black, Silver / Green, White, White / Silver

### wireless-network-card.csv

- Filas: 340, Columnas: 5
- Columnas: name, price, protocol, interface, color
- Columnas numéricas: price
- Columnas categóricas: name, protocol, interface, color
- Fabricantes detectados (ejemplos): 3M, AUKEY, AVM, Asus, Athenatech, Belkin, BenQ, BrosTrend, Buffalo, Cisco
- Colores detectados: Black, Black / Blue, Black / Gold, Black / Orange, Black / Silver, Blue, Blue / Black, Green, Green / Black, Red, Red / Black, White / Red
