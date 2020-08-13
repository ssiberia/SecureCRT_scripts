
print("Szia, hany gyumolcs kell:")
gyumolcs = input()

gyumolcs = int(gyumolcs)

ember = "Orsi"
masik_ember = "Attila"
egy_par = ember + " " + masik_ember + " megevett " + str(gyumolcs) + "db almat"
print(egy_par)
if gyumolcs > 8:
    print("Sok gyumolcs van")
else:
    print("Keves a gyumolcs")


while gyumolcs >= 3:
    print("meg " + str(gyumolcs) + " db gyumolcs van!")
    gyumolcs = gyumolcs - 1

