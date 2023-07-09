import gspread

sa = gspread.service_account(filename="C:/Users/user/Desktop/EL TAKE/eccomerceTake/eccomerceApp/static/archivos/eltake-6fb6c015a363.json")
sh = sa.open("El TAKE")
wks = sh.sheet1
values = ["Valor 1", "Valor 2", "Valor 3"]
wks.append_row(values)
print("holas")
print(wks)