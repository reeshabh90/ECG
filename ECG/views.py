"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,jsonify
from ECG import app
from csv import *
import flask


@app.route('/')

@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        app_name='Hrydyalysis',
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Rupams Contact.',
        app_name='Hrydyalysis',
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Hrydyalysis- The ECG Cardio revolution',
        email='rupam.iics@gmail.com',
        phone='+919845048861',
        app_name='Hrydyalysis',

    )

from flask import request

@app.route('/form')
def form():
    return render_template(
    'form_submit.html',
     year=datetime.now().year,
     app_name='Hrydyalysis',
    
   
    )
@app.route('/fact')
def fact():
    return render_template(
    'factorial_submit.html',
     year=datetime.now().year,
     app_name='Hrydyalysis',
    
   
    )

Rdata=[]
Pdata=[]
Qdata=[]
Sdata=[]
Tdata=[]
    
tab=' '
L2=[]
l2=[]
stat=[]
lno=0
sr=0
@app.route('/ecg/', methods=['POST'])
def ecg():
    print('hi')
    global lno
    global leads
    global tab
    global l2
    global L2
    global stat
    global Rdata
    global Tdata
    global Pdata
    global Qdata
    global Sdata
    global sr
    import traceback
    
   
    try:
        hello();
        #print(tab)
        chartID = 'ecgChart';
        chart_type = 'line';
        chart_height = 550;
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,"width": 1000}
        series = [ {"name": 'Lead '+str(lno), "data": L2},{"name": 'Rpeak', "data": Rdata},{"name": 'Tpeak', "data": Tdata},{"name": 'Ppeak', "data": Pdata},{"name": 'Qpeak', "data": Qdata},{"name": 'Speak', "data": Sdata}]
        title = {"text": 'Raw ECG Signal of Lead '+str(lno)}
        xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
        yAxis = {"title": {"text": 'Amplitude'}}
        return render_template(
          'chart.html', 
           chartID=chartID, 
           fftChartID='fft',
           chart=chart, 
           series=series, 
           title=title, 
           xAxis=xAxis, 
           yAxis=yAxis,
           year=datetime.now().year,
           data=tab,
           app_name='Hrydyalysis',
        )
    except  Exception:
        if traceback.format_exc().find("url")!=-1:
            tab='<h2><p style = "color: red">Data Fetch Time out. Please try again</p></h2>'+tab+'<br/>'
            print (traceback.format_exc())
        else:
            tab='<h2><p style = "color: red">Cant Process The Signal </p></h2>'+tab+'<br/>'+traceback.format_exc()
        chartID = 'ecgChart';
        chart_type = 'line';
        chart_height = 550;
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,"width": 1000}
        series = [ {"name": 'Lead '+str(lno), "data": L2}]
        title = {"text": 'ECG Signal of Lead '+str(lno)}
        xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
        yAxis = {"title": {"text": 'Amplitude'}}
        return render_template(
              'chart.html', 
               chartID=chartID, 
               fftChartID='fft',
               chart=chart, 
               series=series, 
               title=title, 
               xAxis=xAxis, 
               yAxis=yAxis,
               year=datetime.now().year,
               data=tab,
               app_name='ECG',
        )
       
import atexit
from time import time
from datetime import timedelta

def secondsToStr(t):
    return str(timedelta(seconds=t))

line = "="*40
def log(s, elapsed=None):
    print(line)
    print(secondsToStr(time()), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()

def endlog(start):
    end = time()
    elapsed = end-start
    return  secondsToStr(elapsed)

def now():
    return secondsToStr(time())



def hello():
    import matplotlib
    matplotlib.use('Agg')
    #matplotlib.pyplot.close("all")
    import time
    
    start = time.process_time()
    global lno
    global leads
    global tab
    global l2
    global L2
    global stat
    global Rdata
    global Tdata
    global Pdata
    global Qdata
    global Sdata
    global sr
    url=request.form['url']
    adu=int(request.form['adu'])
    lno=int(request.form['lno'])-1
    sr=int(request.form['sr'])#Sampling rate in Hz ( samples/sec)
    import pandas as pd;
    import matplotlib.pyplot as plt, mpld3
    import numpy as np
    
    df=pd.read_csv(url)
    tab='Analysis of Lead '+ str(lno+1) + ' of Signal:<br/>'+ url+'<hr/>'
    #tab=df.head().to_html();
    
    leads=list(df.columns.values)
    if lno > len(leads):
        tab='<p style = "color: blue">Invalid Lead No.+ Only '+str(len(leads))+ ' present</p>'
        
    na=np.array(df[leads[lno]].values)
    l2=np.around( na/adu,4)
    lno=lno+1;#asking user to enter between 1-12, lead is actually between 0-11
    L2=[];
    for index in range(len(l2)):
        L2.append(l2[index])
        

    # Entire ECg Signal Processing Calculation-------------
    
    
    N=len(l2)
    #ECG Signal is between .005Hz to 30Hz
    #N represents sr
    # Hence, sr Hz=N samples
    #        1  Hz= N/sr "
    #        .05 Hz= N*.05/ sr
    startS=int(.5*N/sr)+1
    endS=int(40*N/sr)
    l2s=l2[1:N]
    #Perform fft.............................
     
    yf = np.fft.fft(l2s,N)
    af=yf; #save the actual data
    yf=np.abs(yf)
    #Plot FFT.......................
    
    fig1=plt.figure(figsize=(12,5))
    plt.plot(yf)
    plt.grid()
    plt.title('fft of lead 2')
    fig1.tight_layout()
    #tab=tab+'<br/>'+mpld3.fig_to_html(fig1)+'<br/>'
    #find max of fft and then find the position of maxima...............
    
    mx=max(yf[startS:endS])
    p=np.where(yf[startS:endS]==mx)
    p=p[0][0]+startS;
    fig1=plt.figure(figsize=(12,5))
    plt.plot(yf)
    plt.hold(True)

    z=yf*0;
    z[p]=mx
    z[N-p]=mx
    plt.plot(z,color='red',linewidth=8)
    plt.grid()
    plt.title('R peak in FFT')
    fig1.tight_layout()
    #tab=tab+'<br/>'+mpld3.fig_to_html(fig1)+'<br/>'
    #Rectangular window.......................................
    #W=sr#N/10
    W=endS
    z=af*0;
    z[p-W:p+W]=af[p-W:p+W]
    z[N-p-1-W:N-p-1+W]=af[N-p-1-W:N-p-1+W]
    #z[0]=af[0]
    z[N-1]=af[N-1]

    #ifft................................................
    rs=np.fft.ifft(z,N)
    rs=np.real(rs[1:N])
    
    from matplotlib.ticker import AutoMinorLocator
    spacing=10
    minorLocator =AutoMinorLocator(spacing)

    fig1=plt.figure(figsize=(12,5))
    
   
    
    plt.plot(l2s);
    
    
    plt.grid();
    plt.ylabel('Amplitude in mV->')
    plt.xlabel('Samples->')  
    plt.title('Noisy signal(With Base line Wonder)')
    

    fig1.tight_layout();
    tab=tab+'<br/>'+mpld3.fig_to_html(fig1)+'<br/>'
     #putting the filtered signal in l2s
    l2s=rs.copy();
    fig1=plt.figure(figsize=(12,5))
    plt.plot(rs)
    plt.grid();
    plt.title('Filtered Signal With ZC Adjustment')

    plt.ylabel('Amplitude in mV->')
    plt.xlabel('Samples->')  
    fig1.tight_layout()
    tab=tab+'<br/>'+mpld3.fig_to_html(fig1)+'<br/>'
    # Detecting And Plotting R-Peak................................
    #using time domain analysis
    import pandas as pd
    mx=max(rs)
    ss=list(l2s)
    mx=mx*.5# find all points greater than 70% of the max
    #print(mx)
    
    rpos=np.where(rs>=mx)
    rpos=list(rpos[0])
    #MINRSP=int(len(l2s)*6/len(rpos))
    #MINRSP=150
    #40 bpm is min. which means min freq for R=.6Hz
    MINRSP=int(sr/3)
    zcl=np.abs(l2s)
    
    #print('R length='+str(len(rpos)))
    rloc=[];
    ramp=[]
    last=-300;
    z=l2s*0;
    Rdata=[]
    for index in range(len(l2s)):
        Rdata.append(0)
    for index in range(len(rpos)):
        n=rpos[index]
        if (n-last)>MINRSP:
        #find maxima in the range
           r=15
           try:
               m=max(l2s[n-r:n+r])
               p=np.where(l2s[n-r:n+r]==m)
               p=(p[0]+n-r)[0]
           #print(str(index)+'=>'+str(p))
               z[p]=m
               last=p
               rloc.append(p)
               ramp.append(m)
               Rdata[p]=m;
           except:
               p=n
               m=l2s[p]
           #print(str(index)+'=>'+str(p))
               z[p]=m
               last=p
               rloc.append(p)
               ramp.append(m)
               Rdata[p]=m;

    fig1=plt.figure(figsize=(12,5))
    
    plt.plot(zcl)
    #plt.hold(True)
    #plt.plot(Rdata,color='red',linewidth=1)
    plt.grid()
    plt.title('zcl')
    fig1.tight_layout()

    stat=pd.DataFrame(rloc)
    stat['ramp']=list(ramp)
    
    #tab=tab+'<br/>'+mpld3.fig_to_html(fig1)+'<br/>'
    
    stat1=stat.rename(columns={0:'rloc'})
    stat=stat1
    #Dynamically Calculate all the Windows-------------------------
    #determining all the windows:
    rpos=stat['rloc'].values
    avgR=int(len(l2s)/len(stat['rloc'].values))
    print (avgR)
    TWND=int(sr*.15)# t appears after r after about .2s . I am taking it only .15s
    TSWND=int(sr*.20)#T width is about .2 s so from center it is about 1 sec
   
    QWND=int(sr*.02)
    QSWND=int(sr*.25)
    
    PWND=int(sr*.08)#QRS Complex is about .08 sec. so p should appear  about .04sec before R
    PSWND=int(sr*.1)
    RWDTH=int(sr/18)
    #SWND=int(RWDTH/2)
    SWND=int(sr*.02)
    SSWND=int(sr*.1)
    MINSP=int(avgR/4)# Heart rate can't go beyond 200
    ra=list(stat['ramp'].values)
    ra1=np.mean(ra)
    zcln=zcl*10/ra1
    zcln=np.floor(zcln)
    #Now modify RS by eliminating all the R peaks....................
    rpos=stat['rloc'].values
    ts=rs
    w=RWDTH
    for index in range(len(rpos)):
         ts[rpos[index]-w:rpos[index]+w]=0
    fig1=plt.figure(figsize=(12,5))
    plt.plot(rs)
    plt.title('R-stripped envelope for T detection')
    plt.grid()
    plt.tight_layout()
    #tab=tab+'<br/>'+mpld3.fig_to_html(fig1)+'<br/>'
    
    #tab=tab+'<br/>'+mpld3.fig_to_html(fig1)+'<br/>'
   
    # P peak Detection........................................
    #Detect p Peaks:- loop through r peak and detect max in it's back
    rloc=stat['rloc'].values
    ploc=[];
    pamp=[]
    Pdata=[];
    
    last=-300;
    zp=l2s*0;
    #ss=list(l2s)
    for index in range(len(ss)):
        Pdata.append(0)
    for index in range(len(rloc)):
        n=rloc[index]-PWND
        if( (n-PSWND)<0):
           ploc.append(0)
           pamp.append(0)
        else:
            
           #find maxima in the range
           r=PSWND
           m=max(l2s[n-r:n])
           p=np.where(l2s[n-r:n]==m)
           p=(p[0][0]+n-r)
        
           m=(ss[p])
           zp[p]=m
           last=p
           ploc.append(p)
           pamp.append(m)
           Pdata[p]=m

    
    stat['ploc']=list(ploc)
    stat['pamp']=list(pamp)
    #tab=tab+'<br/>'+mpld3.fig_to_html(fig1)+'<br/>'

    #Q Peak Detection.......................................
    #Detect q Peaks:- loop through r peak and detect min in it's back
    rloc=stat['rloc'].values
    qloc=[];
    qamp=[]
    last=-300;
    zq=l2s*0;
    #ss=list(l2s)
    Qdata=[]
    for index in range(len(l2s)):
        Qdata.append(0)

    for index in range(len(rloc)):
        n=rloc[index]-QWND
        if((n-QSWND)<0):
            qamp.append(0)
            qloc.append(0)
        else:

        
            #find maxima in the range
            r=QSWND
            m=min(l2s[n-r:n])
            try:
               p=np.where(l2s[n-r:n]<=.7*m)
               p=(p[0][len(p[0])-1]+n-r)
            except:
               p=n
        
            m=(ss[p])
            zq[p]=m
            last=p
            qloc.append(p)
            qamp.append(m)
            Qdata[p]=m

    
    
    stat['qloc']=list(qloc)
    stat['qamp']=list(qamp)

    #tab=tab+'<br/>'+mpld3.fig_to_html(fig1)+'<br/>'
    #S Peak Detection--------------------------------------
    #Detect s Peaks:- loop through r peak and detect min in it's front
    rloc=stat['rloc'].values
    sloc=[];
    samp=[]
    last=-300;
    zs=l2s*0;
    #ss=list(l2s)
    Sdata=[];
    #SSWND=RWDTH
    for index in range(len(l2s)):
        Sdata.append(0);  
    for index in range(len(rloc)):
        n=rloc[index]+SWND
    
        if (n+SSWND)>=len(l2s):
            samp.append(0)
            sloc.append(0)
        else:

             
            #find maxima in the range
            r=SSWND
            try:
               m=min(l2s[n:n+r])*.85
               p=np.where(l2s[n:n+r]<=m)
               p=(p[0][0]+n)
            except:
               m=min(l2s[n:n+r])
               p=np.where(l2s[n:n+r]==m)
               p=(p[0][0]+n)
        
            m=(ss[p])
            zs[p]=m
            last=p
            sloc.append(p)
            samp.append(m)
            Sdata[p]=m;

    stat['sloc']=list(sloc)
    stat['samp']=list(samp)
    
    #----------------------------------- T Peak--------------------
    #Detect T Peaks in the right of s peak
    rpos=stat['rloc'].values #intentional.. we want T to be after S
    ts=l2s.copy()
    mx=max(ts)
    mx=mx*.7# find all points greater than 70% of the max
    #print(mx)
    #updated
    
    

    tloc=[];
    tamp=[]
    last=-300;
    zt=l2s*0;
    #ss=list(l2s)
    ts=np.abs(ss)
    
    Tdata=[]
    
    for index in range(len(ss)):
        Tdata.append(0)

    for index in range(len(rpos)):
        n=rpos[index]+TWND
        
        if((n+sr/2)>=len(l2s)):
            tloc.append(0)
            tamp.append(0)
        else:
            #find maxima in the range
            r=TSWND
            Tmin=np.abs(np.min(ss[n:n+r]))
            Tmax=np.max(ss[n:n+r])
            try:
                if Tmax >Tmin  :
                    m=np.max(ss[n:n+r])
                    p=np.where(ss[n:n+r]==m)
                else:
                    m=np.min(ss[n:n+r])
                    p=np.where(ss[n:n+r]==m)
            except:
                m=np.max(ss[n:n+r])
                p=np.where(ss[n:n+r]==m)
            p=p[0][0]+n
            #print(p)
            m=(ss[p])
            zt[p]=m
            last=p
            tloc.append(p)
            tamp.append(m)
            Tdata[p]=m

    # T detection ends here------
    stat['tloc']=list(tloc)
    stat['tamp']=list(tamp)
    fig1=plt.figure(figsize=(12,5))
    plt.plot(l2s,label='ECg')
    plt.hold(True)
    plt.plot(z,color='red',linewidth=1,label='R')
    plt.hold(True)
    plt.plot(zt,color='green',linewidth=1,label='T')
    plt.hold(True)
    plt.plot(zp,color='cyan',label='P')
    plt.hold(True)
    plt.plot(zq,color='magenta',label='q')
    plt.hold(True)
    plt.plot(zs,color='black',label='s')
    plt.grid()
    plt.ylabel('Amplitude in mV->')
    plt.xlabel('Samples->')  
    plt.title('All-peak marked In Filtered ECG')
    plt.legend()
    plt.tight_layout();
    
    tab=tab+'<br/>'+mpld3.fig_to_html(fig1)+'<br/>'
    #------------------ Detection of Onset and Offset----------------
    #Detect R O nset - Select a loca traverse left and check for 0 crossing
    #Detect R O nset - Select a loca traverse left and check for 0 crossing
    rloc=stat['rloc'].values
    ron=[];
    roff=[];
    qoff=[]
    last=-300;
    
    #ss=list(l2s)
    #RWDTH=int(len(l2s)/(len(rloc)*20))

    for index in range(len(rloc)):
        n=rloc[index]
        if(n-RWDTH<0):
           ron.append(0)
        else:
        
            #find maxima in the range
            r=int(RWDTH/2)
            
            m=min(zcl[n-r:n])#zero crossing
            p=np.where(zcl[n-r:n]==m)
            p=(p[0][0]+n-r)
            m=(ss[p])
            ron.append(p)
       
        n=rloc[index]
    
        if(n+RWDTH>=len(l2s)):
            roff.append(0)
        else:
            
            #find maxima in the range
            r=int(RWDTH/2)
            m=min(zcl[n:n+r])
            p=np.where(zcl[n:n+r]==m)
            p=(p[0][0]+n)
            m=(ss[p])
            roff.append(p)
        last=rloc[index]-RWDTH
    
    
    stat['ron']=list(ron)
    stat['roff']=list(roff)
    stat['qoff']=list(ron)
    stat['son']=list(roff)
    #Detect T Onset - Select a loca traverse left and check for 0 crossing
    tloc=stat['tloc'].values
    ton=[];
    toff=[];
    qoff=[]
    last=-300;
    #ss=list(l2s)
    TWDTH=RWDTH*2
    for index in range(len(tloc)):
        n=tloc[index]-int(sr*.02)
        
        if((n-sr*.1)<0):
             ton.append(0)
        else:
             
             #find maxima in the range
             r=int(sr*.05)
             m=np.min(zcl[n-r:n])
             #m=tamp[index]
             p=np.where(zcl[n-r:n]<=m)
             p=(p[0][len(p[0])-1]+n-r*2)
             m=(ss[p])
             ton.append(p)
             
       
        n=tloc[index]+int(sr*.02)
        
        if((n+RWDTH*2)>=len(l2s)):
             toff.append(0)
        else:
               
             #find maxima in the range
              r=int(sr*.06)
              
              try:
                  m=np.min(zcl[n:n+r])
                  #m1=m*.6
                  #m1=tamp[index]
                  p=np.where(zcl[n:n+r]<=m)
                  p=(p[0][0]+n)
              except:
                  m=min(zcl[n:n+r])
                  p=np.where(zcl[n:n+r]==m)
                  p=(p[0][0]+n)
                  m=(ss[p])
              toff.append(p)
                
        
        
        last=tloc[index]-TWDTH
    
    stat['ton']=list(ton)
    stat['toff']=list(toff)
    
    #Detect P Onset - Select a loca traverse left and check for 0 crossing
    ploc=stat['ploc'].values
    pon=[];
    poff=[];
    qoff=[]
    last=-300;
    #ss=list(l2s)
    for index in range(len(ploc)):
        n=ploc[index]-int(sr*.03)
    
        
        if(n-sr*.08)<0:
           pon.append(0)
        else:

           #find maxima in the range
           r=int(sr*.08)
           m=min(ss[n-r:n])
           p=np.where(ss[n-r:n]==m)
           p=(p[0][len(p[0])-1]+n-r)#closeset 0 crosssing
           m=(ss[p])
           pon.append(p)
       
        n=ploc[index]+int(sr*.03)
        
        if(n+sr*.1)>=len(l2s):
           poff.append(0)
        else:
           #find maxima in the range
           r=int(sr*.08)
           try:
               m=min(ss[n:n+r])
               p=np.where(ss[n:n+r]==m)
               p=(p[0][0]+n)
               m=(ss[p])
               poff.append(p)
           except:
               poff.append(0)
        
        n=ploc[index]-RWDTH
    
    stat['pon']=list(pon)
    stat['poff']=list(poff)
    
    #Detect q onset
    qon=[]
    qloc=stat['qloc'].values
    for index in range(len(qloc)):
        n=qloc[index]
    
        
        if(n-RWDTH/2)<0:
           qon.append(0)
        else:

           #find maxima in the range
           r=int(RWDTH/2)
           m=min(zcl[n-r:n])
           p=np.where(zcl[n-r:n]==m)
           p=(p[0][len(p[0])-1]+n-r)#closeset 0 crosssing
           try:
               if p < poff[index]:
                   p=poff[index]
           except:
               p=p-5;
               #do nothing

           m=(ss[p])
           qon.append(p)
      
    stat['qon']=list(qon)
    
    #Detect S offset - Select a loca traverse left and check for 0 crossing
    sloc=stat['sloc'].values
    SWDTH=int(sr*.02)
    SSWDTH=int(sr*.08)
    soff=[];

    last=-300;
    #ss=list(l2s)
    for index in range(len(sloc)):
        n=sloc[index]+SWDTH
    
        
        if ((n+SSWDTH)>=len(l2s)) or sloc[index]==0:
             soff.append(0)
        else:

             #find maxima in the range
             r=SSWDTH
             so=n
              
             m=min(zcln[n:n+r])
             
             
             p=np.where(zcln[n:n+r]<=m)
             try:
                p=(p[0][0]+n)
             except:
                m=np.min(zcl[n:n+r])
                p=np.where(zcl[n:n+r]<=m)
                p=(p[0][0]+n)
             #p=so
             m=(ss[p])
             soff.append(p)
       
        
    
    
    stat['soff']=list(soff)
    tab=tab+'<br/><h1>Statistical Data</h1><br/>All Amplitudes are in mV<br/>All locations are in Sample No.<hr/>'
    tab=tab+'<br/>'+stat.to_html()
    #--------------------- Analysis ---------------------------------------
    #BPM And Qrs Complex
    rloc=stat['rloc'].values
    last=-300
    diff=[]
    diffA=[];#R amplitude Difference for Apnea
    qrs=0;
    ploc=stat['ploc'].values
    rloc=stat['rloc'].values
    qloc=stat['qloc'].values
    tloc=stat['tloc'].values
    sloc=stat['sloc'].values
    qon=stat['qon'].values;
    soff=stat['soff'].values;
    son=stat['son'].values;
    ton=stat['ton'].values;
    toff=stat['toff'].values;
    pon=stat['pon'].values;
    ron=stat['ron'].values;
    qt=0
    st=0
    pr=0;
    qtMin=9999999;
    qtMax=-1;
    qrsMin=9999999;
    qrsMax=-1;
    rt=0;
    diff=[]
    for index in range(len(rloc)):
        if(ton[index]>0):
            rt=rt+ton[index]-ron[index]
        if soff[index]>0 and qon[index]>0:
            qrsval=soff[index]-qon[index]
            qrs=qrs+qrsval
            if qrsval < qrsMin:
                qrsMin=qrsval
            if qrsval > qrsMax:
                qrsMax=qrsval
        if tloc[index]>0 and sloc[index]>0:
            st=st+ton[index]-soff[index]
        if qloc[index]>0 and tloc[index]>0:
            qtval=toff[index]-qon[index]
            qt=qt+qtval
            if qtval <qtMin:
                qtMin=qtval
            if qtval > qtMax:
                qtMax=qtval
        if ploc[index]>0 and rloc[index]>0:
           pr=pr+qon[index]-pon[index]
        if last!=-300 :
            diff.append(rloc[index]-last)
            diffA.append(ramp[index]-ramp[index-1]);
            last=rloc[index]
            
        else :
            last=rloc[index]
    stdRloc=np.std(diff)
    diff=np.mean(diff)    
    qrs=qrs/len(rloc);
    st=st/len(rloc)
    qt=qt/len(rloc)
    pr=pr/len(rloc)
    rt=rt/len(rloc)
    rt=int(rt*1000/sr)
    qtDisp=(qtMax-qtMin)*1000/sr;
    qrsDisp=(qrsMax-qrsMin)*1000/sr;
    if qrsDisp > 95:
        qrsDisp=qrsDisp/2
    qrs_ms=np.abs(int(qrs*1000/sr));#milliseconds
    if qrs_ms > 130:
        qrs_ms=qrs_ms/2
    st=np.abs(int(st*1000/sr));#milliseconds
    qt=np.abs(int(qt*1000/sr));#milliseconds
    pr=np.abs(int(pr*1000/sr));#milliseconds
    rrint=int(diff*1000/sr)
    rrs=(diff/sr)#rr in seconds
    Qtc=int(qt/np.sqrt(rrs))
    #Bazetts formula: QTC = QT / sqrt( RR)
    
    #Ratio of R and S for Apnea
    avR=np.mean(ramp)
    stdRamp=np.mean(np.abs(diffA))*100/avR
    
    avS=(np.mean(samp))
    sr_slope=np.mean(np.array(ramp)-np.array(samp))/avR
    sr_slope=int(sr_slope*100)/100
    signed_avS=np.mean(samp)
    avT=np.mean(tamp)
    avP=(np.mean((pamp-l2s[pon])))
    sr_ratio=int(avS*100/avR)/100
    
    pr_ratio=int(avP*100/avR)/100
    jt=(qt-qrs_ms)
    Jtc=int(jt/np.sqrt(rrs))
    #Detection of Atrial Wave..
    avtp=0
    avtp_max=0
    avtp_min=0;
    succ_tp=0
    tpAll=0*ss;
    for index in range(1,len(tloc)-1):
        if ploc[index+1] > tloc[index] and ploc[index+1]!=0: 
           try:
                a=((ss[toff[index]:pon[index+1]]-ss[pon[index+1]]))
                if(len(a)>0):
                   tpAll[toff[index]:pon[index+1]]=ss[toff[index]:pon[index+1]]
                   avtp=avtp+np.mean(np.abs(a))
                  
                   avtp_max=avtp_max+np.max(a)
                   
                   avtp_min=avtp_min+np.min(a)
           except:
               a=0

        if index>0:
            if tloc[index-1] >0:
                succ_tp=succ_tp+ploc[index]-tloc[index-1]
    
    #Getting FFT of TP Segment for Artrial Wave Detection
    tpf = np.fft.fft(tpAll,N)
    
    tpf=np.abs(tpf);
    tpf=tpf/np.max(tpf)
    # Bandpassing between 3 HZ to 8 HZ
    #Artrial waves appear at about 300bpm
    #https://en.wikipedia.org/wiki/Atrial_fibrillation#Diagnosis
    startS=int(3*N/sr)+1
    last=8
    endS=int(last*N/sr)
    tpf=tpf[0:N/2-1]
    
    z=tpf[startS:endS]
    
    tpf=z
    tpfAv=np.around(np.mean(tpf),3)
    tpfMax=np.around(np.max(tpf),3)
    #Plot FFT.......................
    
    fig1=plt.figure(figsize=(6,3))
    plt.plot(tpf)
    plt.grid()
    plt.title('fft of lead TP Segment')
    fig1.tight_layout()
    tab=tab+'<br/>'+mpld3.fig_to_html(fig1)+'<br/>'            
    tab=tab+'<br/><b> Average Magnitude of TP Segment='+str(tpfAv)+'Max Mag='+str(tpfMax) +'</b><br/>'
    succ_tp=succ_tp/len(tloc)
    succ_tp=int(succ_tp*1000/sr)
    avtp=avtp/len(tloc)
    avtp_max=avtp_max/len(tloc)
    avtp_min=avtp_min/len(tloc)
    tp_slope=(avtp_max-avtp_min)/avR
    tp_slope=int(tp_slope*100)/100
    avtp=int(avtp*100/avR)/100
    #Cordant of T and R
    rsign=avR/np.abs(avR)
    tsign=avT/np.abs(avT)
    tampAvg=np.mean(tamp);
    #Detection of ST Segment Elevation and Depression
    avst=0
    for index in range(1,len(sloc)):
        if tloc[index] > sloc[index] and tloc[index]!=0: 
           a=l2s[soff[index]:ton[index]]
           if(len(a)>0):
               avst=avst+np.mean(a)
    avst=avst/len(sloc)
    avst=int(avst*100/tampAvg)/100
    stdRamp=int(stdRamp*100)/100 
    tab=tab+'<hr/>' 
    tab=tab+'<br/><b>Avg RR-Interval[Normal:600ms-1s]='+str(rrint) +'ms</b>'
    tab=tab+'<br/> Std Deviation of RR Interval[Normal~0]='+str(int(stdRloc*100)/100 )
    tab=tab+'<br/> % of R Amp Variation[Normal~0]='+str(stdRamp)
    t_btn_r= float(diff)/sr; #assuming sampling rate=500
    bpm=int(60.0/t_btn_r)
    tab=tab+'<br/><b> Average Heart Beat Rate[Normal at rest:60-100 bpm]='+str(bpm)+' bpm</b>'
    tab=tab+'<br/><b> Average QRS[Normal:60-100ms]='+str(qrs_ms)+' ms</b>'
    tab=tab+'<br/><b> Average ST Segment[Normal:50-150ms]='+str(st)+' ms</b>'
    tab=tab+'<br/><b> Average T  Amplitude='+str(tampAvg)+' ms</b>'
    if tsign==rsign:
        tab=tab+'<br/><b> ST is <u>CORDANT</u> to QRs </b>'
    else:
        tab=tab+'<br/><b> ST is <u>DISCORDANT</u> to QRs </b>'
    tab=tab+'<br/><b> Average S/R Amplitude[Normal <.5]='+str(sr_ratio)+' </b>'
    tab=tab+'<br/><b> Average S-R Slope[Normal ~1]='+str(sr_slope)+' </b><br/>S-R Slope=(RAMP-SAMP)/RAMP. In Ventricular Abnormalities, it should be near to 0'
    tab=tab+'<br/><b> Average RT Segment[Normal 150-220ms]='+str(rt)+' </b>'
    tab=tab+'<br/><b> Average P/R Amplitude[Normal >.02]='+str(pr_ratio)+' </b>'
    tab=tab+'<br/><b> Average QT interval[Normal: 350-440ms]='+str(qt)+' ms</b>'
    tab=tab+'<br/><b> Average PR interval[Normal:120-200ms]='+str(pr)+' ms</b>'
    tab=tab+'<br/><b> Average TP Segment Amplitude/R amp [Normal:~0]='+str(avtp)+'</b>'
    tab=tab+'<br/><b> Average TP Slope/R amp [Normal:~0]='+str(tp_slope)+'</b></br>TP slope is the difference between max and min in TP segment'
    tab=tab+'<br/><b> Average TP Segment Duration  [Normal:100-250ms]='+str(succ_tp)+' ms</b></br>TP duration is important for Ventricular Abnormality detection'
    tab=tab+'<br/><b> Average ST Segment Amplitude/T amp [Normal:~0]='+str(avst)+'</b>'
    tab=tab+'<br/><b> QRS Dispersion[Normal:<40ms]='+str(qrsDisp)+' ms </b>('+str(int(qrsMin*1000/sr))+','+str(int(qrsMax*1000/sr))+')'
    tab=tab+'<br/><b> Qt Dispersion[]='+str(qtDisp)+' ms</b>('+str(int(qtMin*1000/sr))+','+str(int(qtMax*1000/sr))+')'
    tab=tab+'<br/><b> Corrected Qt or Qtc[340-440]='+str(Qtc)+' ms</b><br/>Uuing Bazetts formula: QTC = QT / sqrt(RR) )'
    tab=tab+'<br/><b> JT[]='+str(jt)+' ms</b>'
    tab=tab+'<br/><b> JTc[]='+str(Jtc)+' </b>'
    signed_sr=np.mean(samp)/avgR
    
    totAlt=0
    diag='';
    abnormal=0
    #Partial Epillepsy. Analyze Hear rate in every 6 seconds
    #http://onlinelibrary.wiley.com/doi/10.1046/j.1528-1157.2002.37801.x/pdf
    #Only for data over 18 sec
    epochs=int(len(l2s)/(sr*6));
    beats=''
    epil=-1
    ref=-1
    bpmVar=[]
    timeRef=[]
    if epochs > 3:
        for index in range(0,epochs-1):
            start=index*6*sr
            end=(index+1)*sr*6
            rInEpochs=len(rloc[(rloc >= start) & (rloc <= end)])
            epochBpm=rInEpochs*10
            if ref <0:
                ref=epochBpm
            else:
                if abs(epochBpm-ref)>=10:
                   epil=index*6
            bpmVar.append(epochBpm)
            timeRef.append((index+1)*6)
            beats=beats+' '+str(epochBpm)
        if epil >=0 and succ_tp>420 and stdRloc<20:
           diag=diag+'<br/><p style="color:red"><b>Major Heart Beat Change Detected at '+str(epil) +' s:<br/>Strong case of Epillepsy</b><br/> </p>'
           #abnormal=1
           epil=5
           fig1=plt.figure(figsize=(6,4))
           plt.plot(timeRef,bpmVar)
           plt.ylabel('Beat in BPM')
           plt.title('Intermediate Heart Beats')
           fig1.tight_layout()
           tab=tab+'<br/>'+mpld3.fig_to_html(fig1)+'<br/>' 
          
        
    
    #T-Wave Alternan
    for index in range(0,len(tamp)-4,4):
        A1=tamp[index]
        A2=tamp[index+1]
        A3=tamp[index+2]
        A4=tamp[index+3]
        
        w1=abs(A1-A3);
        w2=abs(A1-A2);
        w3=abs(A2-A4);
        w4=abs(A3-A4);

        if( (w1<w2) and (w3<w4) and (w3<w1) and (w1<w4)):
            totAlt=totAlt+1
    tot=len(tloc)/4
    altPc=totAlt*100/tot
    twa=int(altPc*100)/100
    tab=tab+'<br/><b>T Wave Alternan (TWA) %='+str(altPc)+' </b>'
    #Detailed Diagnosis.......................................................
    tab=tab+'<hr/>'
    
    #Obstructive Sleep Apnea Conditions.....................
    #https://www.researchgate.net/publication/254039441_Detection_of_obstructive_sleep_apnea_through_ECG_signal_features    
    if st<170  and stdRamp>4 and succ_tp>420 and (abnormal==0) and  sr_ratio<0 and stdRloc <20 and pr_ratio>.02 :
        abnormal=1
        if avst>.1 and tampAvg<-.04:
            diag=diag+'<br/><p style="color:red"><b>Coronary Artery Disease CAD[T inversion] Detected</b></p>'
            abnormal=1
        else:
            diag=diag+'<br/><p style="color:red"><b>Obstructive Sleep Apnea[HIGH R Amp variation,PR>200, TP interval>250ms] Detected</b></p>'
            abnormal=1
    
    #1. Progonestics: CHF
    
   
    if(twa >2) and  stdRloc<20 and abnormal==0 and pr_ratio>.02 and (tpfMax<.1 or tpfAv>.2):
        abnormal=1
        diag=diag+'<br/><p style="color:red"><b>T Wave Alternan[Change in Subsequent T Peak Morphology] Detected</b></p>'
        diag=diag+'<br/> TWA amy lead to Ventricular Arrhythmia'
    #Coronary Artery Disease.......................
    if pr >=200 and sr_slope>=1.15 and succ_tp>=275 and pr_ratio>=.02   and tp_slope>.1 and abnormal==0 and stdRamp<7 and stdRloc <20:
        abnormal=1
        diag=diag+'<br/><p style="color:red"><b>Coronary Artery Disease[PR>200ms, TP Segment>250ms Prominant P,Normal Qtc ] Detected</b></p>'
        diag=diag+'<br/> Commonly CAD affects P. Therefore both P to Qrs and T to P is prolonged. Also ST segment is Elevated or Depressed'
        abnormal=1
        if Qtc >460:
            diag=diag+'<br/><p style="color:red"><b>Hypertension[Qtc>460ms] Detected</b></p>'
    if sr_slope<.5 or sr_ratio>.1 and (qrs_ms>100 and (tpfMax>.12)) and pr_ratio>=.02 and abnormal==0:
        #Ventricular Tachycardia
        abnormal=1
        diag=diag+'<br/><p style="color:red"><b>Ventricular Tachycardia[S R Slope<= .50 | Positive S Peak] Detected</b></p>'
        diag=diag+"<br/> This is due to Fat R-Reak. R and S forms a Notch or Side Rabit"
   
    if stdRloc>20 and  stdRloc<120 and(qrs_ms>100 or tpfMax>.12 or  rt>220 or Qtc>450 )and abnormal==0 and pr_ratio>=.02 :
        #Ventricular Tachycardia
        abnormal=1
        diag=diag+'<br/><p style="color:red"><b>Ventricular Tachycardia[Rloc Std >20] Detected</b></p>'
        diag=diag+'<br/>This is an indication of Fusion Beats(intermediate qrs like morphology) in TP segment'
    #Malignant Ventricular Ectopy:- P wave will be after Q
    qp=np.mean(qloc-ploc)
    if (rsign!=tsign) and (Qtc >460 ) and (abnormal==0) and (np.abs(avst)>.08):
        abnormal=1
        diag=diag+'<br/><p style="color:red"><b>Malignant Ventricular Ectopy(Premature Ventricular Complex) [Qtc>460, Discordant ST,ST Segment non isoelectric] Detected</b></p>'
    if (avst!=0) and (st >160) and (Qtc>460) and (abnormal==0) and (pr_ratio>=.02):
        abnormal=1
        diag='<br/><p style="color:red"><b>Malignant Ventricular Ectopy(Premature Ventricular Complex) [Qtc>440,ST>160>Non isoelectric ST] Detected</b></p>'
    if tp_slope>.3 and (qrs_ms<100 and (succ_tp<50 )) and abnormal==0:
        diag=diag+'<br/><p style="color:red"><b>Malignant Ventricular Ectopy(Premature Ventricular Complex) [TP Slope>.3 @ normal Qrs and Abnormal TP Segment] Detected</b></p>'
        diag=diag+'<br/>Suggests a possible valley between T and P'
        abnormal=1
   
   
    
    
   #Sleep Apnea Condition ends here............................................................
   #Atrial Fibrillation........................ ( Missing p Wave)
    if (abnormal==0) and (((tpfMax >=.4) or (tpfMax>.3 and tpfAv>.12)) and ((pr_ratio>.02) and signed_sr<0) ):
        abnormal=1
        diag=diag+'<br/><p style="color:red"><b>Atrial Fibrillation [Presence of Atrial Wave between T and P] Detected</b></p>'
        diag=diag+'Possible case of <u>Artrial Flutter[AFL]</u>'
    if  (abnormal==0) and (pr_ratio<=.02) and signed_sr<0:
        abnormal=1
        diag=diag+'<br/><p style="color:red"><b>Atrial Fibrillation [Presence of Atrial Wave between T and P, Missing P] Detected</b></p>'
    if pr_ratio<.02 and (abnormal==0) and(avtp<.1) and signed_sr<0:
        abnormal=1
        diag=diag+'<br/><p style="color:red"><b>Atrial Fibrillation [Missing P Wave] Detected</b></p>' 
    if qrs_ms >100 and Qtc > 440 and qrs_ms<120 and abnormal==0 and signed_sr<0:
        diag=diag+'<br/><p style="color:red"><b>CHF (Progonestics) [qrs>100 and qtc >.2 and qt dispersion > 42.7] Detected</b></p>'
        abnormal=1
    if Qtc > 460 and qrs_ms<100 and abnormal==0 and signed_sr<0:
          diag=diag+'<br/><p style="color:red"><b>Atrial tachycardia [QTc > 440 ms] Detected</b></p>'
          abnormal=1
    #..................................
    #finding notch::
    if signed_sr >=.5 and qrs_ms>120 and abnormal==0:
         diag=diag+'<br/><b><p style= "color: red">Ventricular Tachycardia[Notch in nadir of S]</b></p></h3>'
         abnormal=1
    if st < 30 and qrs_ms >120: #start of T immidiately after s
        abnormal=1
        diag=diag+'<br/><b><p style= "color: red">Ventricular Tachycardia[Very short st<30ms]</b></p></h3>'
    if qrs_ms >140 and Qtc > 460 and abnormal==0:
        #Ventricular Tachycardias
        if Qtc > 480 :
             diag=diag+'<br/><b><p style= "color: red"> Torsades de Pointes:-Ventricular Tachycardia[ Qtc >440 ms]</b></p></h3>'
             abnormal=1
        
        else:
            diag=diag+'<br/><b><p style= "color: red"> Ventricular Tachycardia[QRS>110ms and Qtc >460 ms]</b></p></h3>'
            abnormal=1
    if Qtc > 500 and abnormal==0:
          diag=diag+'<br/><b><p style= "color: red"> Torsades de Pointes:-Ventricular Tachycardia[ Qtc >500 ms]</b></p></h3>'
          abnormal=1

    if (qrs_ms>120 or  Qtc > 460 or pr>200 and tpfMax>.12) and avst<-.15 and abnormal==0 and pr_ratio>.02:
          diag=diag+'<br/><p style="color:red"><b>Coronary Artery Disease CAD [ST Segmented Elevated] Detected</b></p>'
          abnormal=1
    if (qrs_ms>120 or  Qtc > 460 or pr>210 or succ_tp>420) and avst>.15 and abnormal==0 and pr_ratio>.02:
          diag=diag+'<br/><p style="color:red"><b>Coronary Artery Disease CAD [ST Segmented Depression] Detected</b></p>'
          abnormal=1
    if (bpm >=60) and (bpm <=120)  and abnormal==0 and qrs_ms>50 and qrs_ms<100 and (pr<205 and tpfMax<.4)and st<150 and st >50 :
        diag=diag+'<br/><b><p style= "color: green"> Normal Synus Rhythm</b></p></h3>'
    else:
        if abnormal==0:
           diag=diag+'<br/><b><p style= "color: red"> Possible Case of Coronary Artery Disease CAD[Aggregated Conditions]</p></b><hr/>'
    
    
    tab=tab+diag
    tab=tab+'<hr/>'
    end=time.process_time();
    elapsed = end-start
    tab=tab+'<i>Total Processing time='+str(elapsed)+' s</i>'
    plt.close('all') 
    #Heart Beat Rate============================== 
    #matplotlib.pyplot.close("all")
    # ECG Processing Completed-----------------------------
    
    
@app.route('/factorial/', methods=['POST'])
def factorial():
    number=int(request.form['number'])
    fact1=1
    for i in range(number,1,-1):
        fact1=fact1*i
    return render_template('factorial_action.html',
                           number=str(number), 
                           factorial=fact1,
                            year=datetime.now().year,
                            app_name='Hrydyalysis',


                           )
@app.route('/chart')
def chart(chartID = 'chart_ID', chart_type = 'line', chart_height = 350):
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Series1', "data": [1.1,2.3,3.5]}, {"name": 'Series2', "data": [4, 5, 6]}]
	title = {"text": 'My Title'}
	xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
	yAxis = {"title": {"text": 'yAxis Label'}}
	return render_template(
        'chart.html', 
        chartID=chartID, 
        chart=chart, 
        series=series, 
        title=title, 
        xAxis=xAxis, 
        yAxis=yAxis,
        year=datetime.now().year,
        app_name='Hrydyalysis',
        )

#thins method is working.. displaying a simple chart with python-nvd3
@app.route("/data")
def data():
    #use this while sending a response
    #jdata=jsonify(get_data())
    import json;
    jdata=json.dumps(get_data())
   
    objects = json.loads(jdata)
    rows = list(objects['children'])
    #print(columns.ite)
    good_columns = [
    "symbol",
    "volume",
    "percent_change",
    "net_change" 
    ]
    mydata = []
    xdata=[]
    ydata=[]
    ydata2=[]
    for row in rows:
        selected_row = []
        for item in good_columns:
            selected_row.append(row[item])
        mydata.append(selected_row)
        xdata.append(selected_row[0])
        ydata.append(selected_row[2])
        ydata2.append(selected_row[3])
    import pandas as pd
    #stops = pd.DataFrame(data, columns=good_columns)
    from nvd3 import discreteBarChart
    chart=discreteBarChart(name='Stock Values',title='Stok Values' ,color_category='category20c', height=450, width=900)
    chart.add_serie(ydata,xdata,'Percent Change')
    chart.add_serie(ydata2,xdata,'Net Change')
    
    chart.buildcontent()

    #print (chart.htmlcontent)    
    return render_template(
        'stock.html', 
        html_part=chart.htmlcontent,
        scripts=chart.header_js,
        year=datetime.now().year,
        app_name='Hrydyalysis',
        )

#This method is for Creating Bubble chart
@app.route("/data2")
def data2():
   
    return render_template(
        'stock1.html', 
        year=datetime.now().year,
        app_name='Hrydyalysis',
        )

import csv
import requests
URL = "http://www.nasdaq.com/quotes/nasdaq-100-stocks.aspx?render=download"

def get_data():
    r = requests.get(URL)
    data = r.text
    RESULTS = {'children': []}
    for line in csv.DictReader(data.splitlines(), skipinitialspace=True):
        RESULTS['children'].append({
            'name': line['Name'],
            'symbol': line['Symbol'],
            'symbol': line['Symbol'],
            'price': line['lastsale'],
            'net_change': line['netchange'],
            'percent_change': line['pctchange'],
            'volume': line['share_volume'],
            'value': line['Nasdaq100_points']
        })
    return RESULTS

@app.route("/get_data2")
def get_data2():
    r = requests.get(URL)
    data = r.text
    RESULTS = {'children': []}
    for line in csv.DictReader(data.splitlines(), skipinitialspace=True):
        RESULTS['children'].append({
            'name': line['Name'],
            'symbol': line['Symbol'],
            'symbol': line['Symbol'],
            'price': line['lastsale'],
            'net_change': line['netchange'],
            'percent_change': line['pctchange'],
            'volume': line['share_volume'],
            'value': line['Nasdaq100_points']
        })
    return jsonify(RESULTS);

#------------we cam-------------
# Let's declare
centre=[];
@app.route("/get_data3")
def get_data3():
    print('I am here')
    return jsonify(centre);

@app.route('/cam')
def cam():
    return render_template(
        'cam.html',
        title='Web cam',
        
        year=datetime.now().year,
       
        app_name='Hrydyalysis',
    )
###############################
########## Face Tracking############
@app.route('/face_tracking')
def face_tracking():
    return render_template(
                           'track.html',
                           year=datetime.now().year,
                            app_name='Hrydyalysis',
                           )
#############################
@app.route('/face_stat', methods=['GET','POST'])
def face_stat():
    import json
    s=request.form
    str1=''
    
    #tags = request.form['tag_list']
    try:
        ar=json.loads(s['stat'])
        #### Some processing--- Lets calculate centre
        x=int(ar[0]['x'])
        y=int(ar[0]['y'])
        width=int(ar[0]['width'])
        height=int(ar[0]['height'])
        x=x+width/2
        y=y+height/2
        #str1='x:'+str(ar[0]['x'])+' y:'+str(ar[0]['y'])+' w:'+str(ar[0]['width'])+' h:'+str(ar[0]['height'])
        str1='{"xc":'+str(x)+',"yc":'+str(y)+'}'
        centre.append(json.dumps(str1));
        print(str1)
        
    except:
         str1='{"xc":'+str(-1)+',"yc":'+str(-1)+'}'
         
    resp=flask.Response(json.dumps(str1))

    return resp

@app.route('/favicon.ico')
def favicon():
    import flask
    import os
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
####### ECG#######
@app.route('/ECG')
def ECG():
    return render_template(
                           'ECG.html',
                           year=datetime.now().year,
                            app_name='Hrydyalysis',
                           )
######### Traffic accident data analysis
@app.route('/traffic')
def traffic():
    """Renders the about page."""
    import ijson
    import os
   
    
    filename = os.path.realpath('md_traffic.json')
    print(filename)
    with open(filename, 'r') as f:
        objects = ijson.items(f, 'meta.view.columns.item')
        columns = list(objects)
        print(columns[0])

    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='This is Rupams First Flask App.',
        app_name='Hrydyalysis',

    )