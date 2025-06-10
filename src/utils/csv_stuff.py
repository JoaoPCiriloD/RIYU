def coord_to_csv(array):
    return str(array[1]) + "," + str(array[0]) + "\n"

def write_csv_header(file_name, json_input):
    lines = []

    for v in json_input["veiculos"]:
        if "start" in v:
            lines.append(coord_to_csv(v["iniciar"]))
        if "end" in v:
            lines.append(coord_to_csv(v["terminar"]))

    if "jobs" in json_input:
        for job in json_input["trabalhos"]:
            lines.append(coord_to_csv(job["local"]))

    if "remessa" in json_input: 
        for remessa in json_input["remessa"]:
            lines.append(coord_to_csv(remessa["escolha"]["local"]))
            lines.append(coord_to_csv(remessa["entrega"]["local"]))

    print("Writing CSV header to", file_name + ".csv")
    with open(file_name + ".csv", "w") as output_file:
        for line in lines:
            output_file.write(line)


