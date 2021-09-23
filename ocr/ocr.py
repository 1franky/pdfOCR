import os
import img2pdf
import ocrmypdf
import shutil
from time import sleep

from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from configparser import ConfigParser

def createDirectory(path, name):
    here = os.getcwd()
    os.chdir(path)
    try:
        os.mkdir(name)
    except:
        pass
    os.chdir(here)

def obtenRutas():
    parser = ConfigParser()
    parser.read('conf.ini')
    urgentes   = parser.get('paths', 'urgentes')
    entrega    = parser.get('paths', 'entrega')
    proceso    = parser.get('paths', 'proceso')
    # tmp        = parser.get('paths', 'tmp')
    root       = parser.get('paths', 'root')
    tmp         = os.path.join(root, "tmp")
    # procesado  = parser.get('paths', 'procesad')
    return urgentes, entrega, tmp, root, proceso

def clear():
    os.system("cls")

def clearDIR(path):
    os.chdir(path)
    for borra in os.listdir():
        try:
            os.remove(borra)
        except:
            pass

def writePDFparte(parte, path, pdfWritte):
    name = ("0"*(5-len(str(parte)))) + str(parte) + ".pdf"
    pathSalida = os.path.join(path, name)
    try:
        if pdfWritte.getNumPages() > 0:
            with open(pathSalida,"wb") as f:
                pdfWritte.write(f)
    except Exception as e:
        print(e)
    print("Partition {} ".format(parte))
        
def dividePDF(tmpProceso, TMP, exp):
    os.chdir(tmpProceso)
    name = exp + ".pdf"
    pff = open(name, "rb")
    pdf = PdfFileReader(pff)
    page = contador = parte = 0 
    pdfWritte = PdfFileWriter()
    for num in range(pdf.getNumPages()):
        pdfWritte.addPage(pdf.getPage(page))
        contador -= -1
        page -= -1
        if contador >= 100:
            contador = 0 
            writePDFparte(parte, TMP, pdfWritte)
            parte += 1
            pdfWritte = PdfFileWriter()
    writePDFparte(parte, TMP, pdfWritte)
    pff.close()
    return pdf.getNumPages()

def comprime(name, part):
    ghost = r"C:\ocrCompresor\CompressPDF\ghostscript\gswin64c.exe"
    levelCompresion = {
        "screen"    : "/screen", #(screen-view-only quality, 72 dpi images)
        "ebook"     : "/ebook",  #(low quality, 150 dpi images)
        "printer"   : "/printer", #(high quality, 300 dpi images)
        "prepress " : "/prepress ", #(high quality, color preserving, 300 dpi imgs)
        "default"   : "/default" #(almost identical to /screen)
    }
    level = levelCompresion['ebook']

    # shutil.copy(name, "tmp.pdf")
    comprim = '{} -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS={} -dNOPAUSE -dBATCH -sOutputFile="{}" tmp.pdf'.format(ghost, level, part)
    # print(comprim)
    os.system(comprim)
    os.remove("tmp.pdf")

def ocr(tmp):
    os.chdir(tmp)
    partes = os.listdir()
    for part in partes:
        if part.endswith(".pdf"):
            try:
                # ocrmypdf.ocr(part, os.path.join(tmp, "tmp.pdf"), optimize=3, force_ocr=True, use_threads=True)
                ocrmypdf.ocr(part, os.path.join(tmp, part), optimize=3, force_ocr=True, use_threads=False)
            except Exception as e:
                print(e)
                print("---------")
                # ocrmypdf.ocr(part, os.path.join(tmp, "tmp.pdf"), force_ocr=True, use_threads=True)
                ocrmypdf.ocr(part, os.path.join(tmp, part), optimize=3, force_ocr=True, use_threads=False)
            # os.remove(part)
            # sleep(2)
            # comprime("tmp.pdf", part)

def unePDFs(path, salida, name):
    ghost = r"C:\ocrCompresor\CompressPDF\ghostscript\gswin64c.exe"
    levelCompresion = {
        "screen"    : "/screen", #(screen-view-only quality, 72 dpi images)
        "ebook"     : "/ebook",  #(low quality, 150 dpi images)
        "printer"   : "/printer", #(high quality, 300 dpi images)
        "prepress " : "/prepress ", #(high quality, color preserving, 300 dpi imgs)
        "default"   : "/default" #(almost identical to /screen)
    }
    level = levelCompresion['ebook']
    os.chdir(path)
    nam = name + ".pdf"
    # dirSalida = os.path.join(salida, nam)
    pdfs = os.listdir()
    mergedObject = PdfFileMerger()
    for pdf in pdfs:
        mergedObject.append(PdfFileReader(pdf, 'rb'))
    mergedObject.write("temporal.pdf")
    # os.chdir(salida)
    comprim = '{} -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS={} -dNOPAUSE -dBATCH -sOutputFile="{}" temporal.pdf'.format(ghost, level, "COMPRIMIDO.pdf")
    os.system(comprim)
    # os.remove("tmp.pdf", nam)
    # shutil.copy("comprimido.pdf")

def reporte(path, name, status):
    pass

def regresa(path, fil, destino):
    try:
        os.chdir(path)
        shutil.move(fil, destino)
        return
    except:
        pass
        # sleep(3)
        # print("Bucle {}->{}->{}".format(path, fil, destino))
        # return regresa(path, fil, destino)

def remove(path, fil):
    try:
        os.chdir(path)
        os.remove(fil)
        return
    except:
        pass
        # sleep(3)
        # print("Bucle {}->{}".format(path, fil))
        # return remove(path, fil)

def main(tipo):
    # clear()
    urgentes, entrega, tmp, rot, proceso = obtenRutas()
    here = os.getcwd()

    createDirectory(here, "TMP")
    TMP = os.path.join(here, "TMP")
    find = urgentes if (tipo == 1) else entrega
    for root, _, files in os.walk(find, topdown = False):
        print(root)
        for fil in files:
            if not fil.endswith(".pdf"):
                continue
            clearDIR(TMP)
            exp, _ = os.path.splitext(fil)
            os.chdir(root)
            try:
                print("Copiando {} -> {}".format(fil, proceso))
                shutil.move(fil, proceso)
                print("Archivo copiado...")
                # sleep(2)
            except Exception as e:
                print("No se pudo mover {}->{} error: 1.{} ".format(fil, proceso, e))
                continue
            
            try:
                pages = dividePDF(proceso, TMP, exp)
                # sleep(2)
            except Exception as e:
                print("No se pudo dividir PDF error: 2.{}".format(e))
                regresa(proceso, fil, root)
                continue

            try:
                ocr(TMP)
                # sleep(2)
            except Exception as e:
                print("No se pudo hacer OCR en PDF error: 3.{}".format(e))
                regresa(proceso, fil, root)
                continue

            a = exp.split("_")
            if (len(a) == 1):
                nameAsignado = "{}_{}".format(int(a[0]), pages)
            else:
                nameAsignado = "{}_{}_{}".format(int(a[0]), a[1], pages)
            print("OCR Terminado Nombre asignado: {}".format(nameAsignado))


            # nameAsignado = "{}_{}".format(exp, pages)
            try:
                unePDFs(TMP, tmp, nameAsignado)
                # sleep(2)
            except Exception as e:
                print("No se pudo hacer unir PDF error: 4.{}".format(e))
                regresa(proceso, fil, root)
                continue
            os.chdir(TMP)
            shutil.copy("COMPRIMIDO.pdf", os.path.join(tmp, "{}.pdf".format(nameAsignado)))
            # shutil.move("{}.pdf".format(nameAsignado), os.path.join(rot, "{}.pdf".format(nameAsignado)))
            # sleep(2)
            os.chdir(tmp)
            try:
                print("{}.pdf".format(nameAsignado), os.path.join(rot, "{}.pdf".format(nameAsignado)))
                shutil.move("{}.pdf".format(nameAsignado), os.path.join(rot))
                # sleep(4)
                #os.remove("{}.pdf".format(nameAsignado))
                remove(proceso, fil)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    here = os.getcwd()
    while True:
        try:
            tipo = int(input("1.Urgentes\n2.ProcesoNormal\nIngresa opcion: "))
        except:
            print("Solo se permiten valores entre 1 y 2.\nTry again\n")
            tipo = 3
        if (tipo == 2 or tipo == 1):
            break
    while True:
        main(tipo)
        os.chdir(here)
        print("Esperando archivos....")
        sleep(60)