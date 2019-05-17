simps={
    "go":"move",
    "pickup":"get",
    "grab":"get",
    "inspect":"read",
    "attack":"hit",
    }


def simplify(line):
    for rfrom, rto in simps.items():
        line=line.replace(rfrom, rto)
    return line 
