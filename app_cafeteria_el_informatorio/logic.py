from data import opciones_cafeteria, opciones_comidas

def calcular_demora(pedido):
    # Verificamos si hay artículos de cafetería o comida
    tiene_cafeteria = any(item in opciones_cafeteria for item, _ in pedido)
    tiene_comidas = any(item in opciones_comidas for item, _ in pedido)

    if tiene_cafeteria and tiene_comidas:
        return 35  # 25 minutos de comida + 10 minutos adicionales
    elif tiene_comidas:
        return 25
    elif tiene_cafeteria:
        return 15
    return 0

def calcular_total(pedido):
    # Sumamos los precios de los artículos en el pedido
    return sum(precio for _, precio in pedido)