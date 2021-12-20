from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Pdf
import codecs
import PyPDF2
from django.conf import settings


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    
    context = {"number" : 0}
    if request.user.is_authenticated:
       logout(request)
       context = {"number" : 1}
    return render(request, "index.html",context)
        
 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ogretmen_giris(request):
        
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                login(request, user)
                return redirect('/upload')
            else:
                messages.info(request, 'Email veya şifre hatalı')
                return render(request, "ogretmen_giris.html")

        else:
            context = {"number" : 0}
            if request.user.is_authenticated:
                logout(request)
                context = {"number" : 1}
            return render(request, "ogretmen_giris.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutUser(request):
    logout(request)
    return redirect('/giris')




    

@login_required(login_url='giris')
def upload(request):
    if request.method=='POST':
        uploaded_file=request.FILES['document']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)

        
        #pathfile = os.path.join(settings.BASE_DIR, 'media')+'\\'+uploaded_file.name
        
        import pdfplumber
        pdf = pdfplumber.open(uploaded_file)

        pdfReader = PyPDF2.PdfFileReader(uploaded_file)
        sayfasayisi = pdfReader.numPages
        
        file2 = codecs.open(r"MyFile.txt","w","utf-8")

        for x in range(int(sayfasayisi)):
            page = pdf.pages[x]
            text = page.extract_text()
            file2.write(text)
        

        file2.close()
        

       
        studentnamex = ""
        studentnox = ""
        studenttypex = ""
        projecttypex = ""
        projectsummaryx = ""
        projectdatex = ""
        projecttitlex = ""
        keywordsx = ""
        counselornamex = ""
        counselordegreex = ""
        jurynamex = ""
        jurydegreex = ""
        
        lines = []
        with codecs.open("MyFile.txt","r","utf-8") as f:
            lines = f.readlines()
        
        

        #Dersin adı için alternatif
        """
        for line in lines:
            count += 1
            if "LİSANS TEZİ" in line.upper():
                projecttypex = "LİSANS TEZİ"
                
                
            if "ARAŞTIRMA PROBLEMLERİ" in line.upper():
                projecttypex = "ARAŞTIRMA PROBLEMLERİ"
                
        """
        #Dersin adı için alternatif


        #Dersin adı         
        bayrak = 0
        bayrak2 = 0
        for line in lines:
                
            if "BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ" in line.upper():
                if(bayrak2 == 0):
                    bayrak2 += 1
                    continue
                else:
                    bayrak = 1
                    continue
            if(bayrak == 1):
                if(line.isspace()):
                    continue
                if(not line.isspace()):
                    projecttypex = line.strip()
                    print(projecttypex)
                    break
        #Dersin adı




        #Proje Başlığı / ödev konusu
        bayrak = 0
        bayrak2 = 0
        count = 0
        for line in lines:
            count += 1  

            if projecttypex in line.upper():
                bayrak = 1
                continue


            if(bayrak == 1):
                if(line.isspace()):  
                    if(not bayrak2 == 0):
                        count -= 1
                        break
                    else:
                        continue
                if(not line.isspace()):
                    projecttitlex += line.strip()
                    projecttitlex += " "
                    bayrak2 += 1
                    
        print(projecttitlex)
        #Proje Başlığı / ödev konusu


        #Hocalar  aşağıdaki biçimlerde pdfe yazilmasi gerekir // diğer veriler içinde geçerli
        bayrak = 0
        bayrak2 = 0
        countx = 0
        for line in lines:
            countx += 1    
            if (countx == count):
                bayrak += 1
                continue
            if(not bayrak == 0):
                if "öğr. gör. dr." in line.lower():
                    if(bayrak2 == 0):
                        counselordegreex = "Öğr. Gör. Dr."
                        jurydegreex = "Öğr. Gör. Dr."
                        counselornamex = line[13:-1]
                        jurynamex = line[13:-1]
                        bayrak2 +=1
                        continue
                    jurydegreex += ", "+"Öğr. Gör. Dr."
                    jurynamex += ", "+line[13:-1]       
                if "öğr. üyesi" in line.lower():
                    if(bayrak2 == 0):
                        counselordegreex = "Dr. Öğr. Üyesi"
                        jurydegreex = "Dr. Öğr. Üyesi"
                        counselornamex = line[15:-1]
                        jurynamex = line[15:-1]
                        bayrak2 +=1
                        continue  
                    jurydegreex += ", "+"Dr. Öğr. Üyesi"
                    jurynamex += ", "+line[15:-1]         
                if "doç." in line.lower():
                    if(bayrak2 == 0):
                        counselordegreex = "Doç. Dr."
                        jurydegreex = "Doç. Dr."
                        counselornamex = line[8:-1]
                        jurynamex = line[8:-1]
                        bayrak2 +=1
                        continue  
                    jurydegreex += ", "+"Doç. Dr."
                    jurynamex += ", "+line[8:-1]         
                if "prof." in line.lower():
                    if(bayrak2 == 0):
                        counselordegreex = "Prof. Dr."
                        jurydegreex = "Prof. Dr."
                        counselornamex = line[9:-1]
                        jurynamex = line[9:-1]
                        bayrak2 +=1        
                        continue
                    jurydegreex += ", "+"Prof. Dr."
                    jurynamex += ", "+line[9:-1]      
            
            if(len(line.strip()) == 0 and not len(jurynamex.strip()) == 0):
                print(counselordegreex+"|,|"+jurydegreex+"|,|"+counselornamex+"|,|"+jurynamex)
                break
            

        #Hocalar 

        #Odevin teslim edildiği dönem

        bayrak = 0
        for line in lines:
                
            if "tezin savunulduğu tarih" in line.lower():
                index = 0
                for c in line:
                    if c == ".":
                       ay = int(line[index+1])*10 + int(line[index+2])
                       yil = int(line[index+4])*1000 + int(line[index+5])*100 + int(line[index+6])*10 + int(line[index+7])
                       teslim = "" 
                       if ay >= 9 and ay <=12:
                           teslim = str(yil) + "-" + str(yil+1) + " Güz"  
                       if ay >= 1 and ay <=8:    
                           teslim = str(yil-1) + "-" + str(yil) + " Bahar"
                       projectdatex = teslim       
                       break
                    index += 1
                break
        print(projectdatex)

        #Odevin teslim edildiği dönem

        # Öğrenci adı ve numarası 
        bayrak = 0
        bayrakn = 0
        bayrak2 = 0
        for line in lines:
                
            

            if "öğrenci no" in line.lower():
                
                ogrnox =  [int(s) for s in line.split() if s.isdigit()]
                ogrno = ogrnox[0]
                if(bayrak == 1):
                    studentnox += ", "+str(ogrno)
                else:
                    studentnox += str(ogrno)
                bayrak = 1
                

            if "adı soyadı" in line.lower():
                
                if(bayrakn == 1):
                    studentnamex += ", "+line[12:-1]
                else:
                    studentnamex += line[12:-1]

                bayrakn = 1
                
                
            
            if "imza" in line.lower():
                bayrak2 = 1
                continue
            
            if bayrak2 == 1 and len(line.strip()) == 0:
                continue
            
            if(len(line.strip()) == 0 and not len(studentnamex.strip()) == 0):
                print(studentnamex+"|,|"+studentnox)
                break
        # Öğrenci adı ve numarası      

        # Proje özet
        bayrak = 0
        bayrakg = 0
        for line in lines:

            if "özet" in line.lower():
                if(bayrak == 0):
                    bayrak = 1
                    continue
                else:
                    bayrakg = 1
                    continue

            if bayrakg == 1:
                
                if "anahtar  kelimeler" in line.lower():
                   break
                else:
                   projectsummaryx += line     


        print(projectsummaryx)
        # Proje özet

        # Anahtar kelimeler
        bayrak = 0
        for line in lines:
            if "anahtar  kelimeler" in line.lower():
                    keywordsx += line.lower().replace('anahtar  kelimeler:','')
                    bayrak = 1
                    continue

            if(not len(line.strip()) == 0 and bayrak == 1):
                keywordsx += line.lower()
                continue
            if(len(line.strip()) == 0 and bayrak == 1):
                break
        # Anahtar kelimeler


        # Öğretim türü
        studenttypex = studentnox[5:-3]+". Öğretim"
        # Öğretim türü
        print(studenttypex)
        print(keywordsx)
        """
        pageObj = pdfReader.getPage(1)
        page_content = pageObj.extractText()
        print(page_content)
        uploaded_file.close()
        #print(pageObj.extractText()) 
        """

        
        modelsfd = Pdf(studentname = studentnamex, studentno = studentnox, studenttype = studenttypex,
        projecttype = projecttypex, projectsummary = projectsummaryx, projectdate = projectdatex,
        projecttitle = projecttitlex, keywords = keywordsx, counselorname = counselornamex,
        counselordegree = counselordegreex, juryname = jurynamex, jurydegree = jurydegreex, 
        pdfself = uploaded_file)
        modelsfd.save()

    todos = Pdf.objects.all()

    return render(request,'upload.html',{"todos":todos})

   
        
