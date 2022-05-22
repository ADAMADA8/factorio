import wget,os, yaml,platform, shutil,numpy, sys, urllib.parse, urllib.error

sname = platform.system()
print("Система: "+sname+"\n")
#links
mfile="https://raw.githubusercontent.com/ADAMADA8/factorio/main/mods.yml"
#mfile=urllib.parse.quote(mfile)
moddownloadurl="https://github.com/ADAMADA8/factorio/raw/main/"
dmodlist=[]

if sname == "Windows":
    moddir=os.getenv("APPDATA")+"\\Factorio\\mods"
elif sname == "Linux":
    try:
        moddir=os.path.expanduser('~')+"/.factorio/mods"
    except urllib.error.URLError:
        print("Папка с модами не найдена, создание..")
        os.mkdir(os.path.expanduser('~')+"/.factorio/mods")
        moddir=os.path.expanduser('~')+"/.factorio/mods"

if os.path.exists("tmp") == False:
    os.mkdir(os.getcwd()+"\\tmp")
tmpfout=os.getcwd()
tmpfout=tmpfout+"\\tmp\\"

def stop():
    if os.path.exists(tmpfout+"mods.yml"):
        os.remove(tmpfout+"mods.yml")
    if len(os.listdir(tmpfout))==0:
        os.rmdir(tmpfout)
    input("Нажмите Enter для выхода ")
    sys.exit()

print("Загрузка списка модов в "+tmpfout)
try:
    wget.download(url=mfile,out=tmpfout)
except:
    print("Список модов не найден, завершение..")
    stop()
print("\n")
mlistp=os.getcwd()+"\\tmp\\mods.yml"
with open(mlistp) as file:
    modlist = yaml.load(file,Loader=yaml.FullLoader)
    modlist=modlist["download"]
print(f"Будут установлены моды ({len(modlist)}): ")
for mod in modlist:
    print(mod)
print("=========================")
k = input("Продолжить? y/n\n")
if k == "y":
    begin = True
else:
    stop()

print("Подождите..")

for mod in modlist:
    print("Установка "+mod+"..")
    modurl=moddownloadurl+mod
    try:
        modpath=wget.download(url=modurl,out=moddir)
        dmodlist.append(mod)
    except:
        print(f"Мод {mod} не найден, пропускаю..")
        continue
    print("")
    shutil.unpack_archive(modpath,moddir)
    os.remove(modpath)

print("=========================")
print(f"Скачано и установлено {len(dmodlist)} из {len(modlist)}")
notdownloaded=numpy.setdiff1d(modlist,dmodlist)
if len(notdownloaded) != 0:
    print(f"Неустановлено: ")
for mod in notdownloaded: print(mod)
stop()