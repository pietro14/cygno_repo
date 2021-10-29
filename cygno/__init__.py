# Copyright 2021 dciangot
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Image analisys CYGNO Python Library
# G. Mazzitelli 2017 
# rev oct 2018 - swift direct access 
# rev Oct 2021 clean up and packege
# 

__version__ = '1.0.1'
__all__     = ["cmd", "his", "s3"]

import numpy as np
import glob, os
import re
import sys
from cygno import s3

class myError(Exception):
    pass

#
# CYGNO py ROOT Tools
#

def write2root(fname, img, id=0, option='update', verbose=False):
    import ROOT
    tf = ROOT.TFile.Open(fname+'.root', option)
    img=img.T
    (nx,ny) = img.shape
    h2 = ROOT.TH2D('pic_run',fname+'_'+str(id),nx,0,nx,ny,0,ny)
    h2.GetXaxis().SetTitle('x')
    h2.GetYaxis().SetTitle('y')
    [h2.SetBinContent(bx,by,img[bx,by]) for bx in range(nx) for by in range(ny)]
    h2.Write()
    tf.Close()
    
def TGraph2array(tgraph, verbose=False):
    import ctypes
    xl = []; yl = []
    for i in range(tgraph.GetN()):
        xi = ctypes.c_double(); yi = ctypes.c_double()
        tgraph.GetPoint(i,xi,yi)
        xl.append(xi.value)
        yl.append(yi.value)
    x = np.array(xl)
    y = np.array(yl)
    return x, y

def rootTH2byname(root_file, verbose=False):
    pic = []
    wfm = []
    for i,e in enumerate(root_file.GetListOfKeys()):
        che = e.GetName()
        if ('pic_run' in str(che)):
            pic.append(che)
        elif ('wfm_run' in str(che)):
            wfm.append(che)
    return pic, wfm
    
class cfile:
    def __init__(self, file, pic, wfm, max_pic, max_wfm, x_resolution, y_resolution):
        self.file         = file
        self.pic          = pic 
        self.wfm          = wfm
        self.max_pic      = max_pic
        self.max_wfm      = max_wfm
        self.x_resolution = x_resolution
        self.y_resolution = y_resolution
    
def open_(run, tag='LAB', posix=False, verbose=False):
    import ROOT
    import root_numpy as rtnp
    class cfile:
        def __init__(self, file, pic, wfm, max_pic, max_wfm, x_resolution, y_resolution):
            self.file         = file
            self.pic          = pic 
            self.wfm          = wfm
            self.max_pic      = max_pic
            self.max_wfm      = max_wfm
            self.x_resolution = x_resolution
            self.y_resolution = y_resolution
    try:
        f=ROOT.TFile.Open(s3.root_file(run, tag, posix=posix))
        pic, wfm = rootTH2byname(f)
        image = rtnp.hist2array(f.Get(pic[0])).T
        x_resolution = image.shape[1]
        y_resolution = image.shape[0]
        max_pic = len(pic)
        max_wfm = len(wfm)
    except:
        raise myError("openFileError: "+s3.root_file(run, tag, posix=posix))
    

    if verbose:
        print ('Open file: '+s3.root_file(run, tag, posix=posix))
        print ('Find Keys: '+str(len(f.GetListOfKeys())))
        print ("# of Images (TH2) Files: %d " % (max_pic))
        print ("# of Waveform (TH2) Files: %d " % (max_wfm))
        print ('Camera X, Y pixel: {:d} {:d} '.format(x_resolution, y_resolution))
    return cfile(f, pic, wfm, max_pic, max_wfm, x_resolution, y_resolution)

def pic_(cfile, iTr=0, verbose=False):
    import ROOT
    import root_numpy as rtnp
    pic, wfm = rootTH2byname(cfile.file)
    image = rtnp.hist2array(cfile.file.Get(pic[iTr])).T
    return image

def wfm_(cfile, iTr=0, iWf=0, verbose=False):
    import ROOT
    import root_numpy as rtnp
    wfm_module=int(cfile.max_wfm/cfile.max_pic)
    if (iTr > cfile.max_pic) or (iWf > wfm_module):
        raise myError("track or wawform out of ragne {:d} {:d}".format(cfile.max_pic, wfm_module))
    i = iTr*wfm_module+iWf
    pic, wfm = rootTH2byname(cfile.file)
    t,a = TGraph2array(cfile.file.Get(wfm[i]))
    return t,a

def read_(f, iTr=0, verbose=False):
    import ROOT
    import root_numpy as rtnp
    pic, wfm = rootTH2byname(f)
    image = rtnp.hist2array(f.Get(pic[iTr])).T
    return image

def ped_(run, path='./ped/', tag = 'LAB', posix=False, min_image_to_read = 0, max_image_to_read = 0, verbose=False):
    #
    # run numero del run
    # path path lettura/scrittura piedistalli
    # tag subdirectory dei dati
    # min_image_to_read , max_image_to_read  range di imagine sul quale fare i piedistalli 
    # max_image_to_read = 0 EQUIVALE A TUTTE LE IMMAGINI
    #
    import ROOT
    import root_numpy as rtnp
    import numpy as np
    import tqdm
    # funzione per fare i piedistalli se gia' non esistino nella diretory

    fileoutm = (path+"mean_Run{:05d}".format(run))
    fileouts = (path+"sigma_Run{:05d}".format(run))

    if os.path.exists(fileoutm+".root") and os.path.exists(fileouts+".root"): 
        # i file gia' esistono
        m_image = read_(ROOT.TFile.Open(fileoutm+".root"))
        s_image = read_(ROOT.TFile.Open(fileouts+".root"))
        print("RELOAD maen file: {:s} sigma file: {:s}".format(fileoutm, fileouts))
        return m_image, s_image
    else:
        # i file non esistono crea il file delle medie e delle sigma per ogni pixel dell'immagine
        if verbose: print (">>> Pedestal Maker! <<<")
        try:
            cfile = open_(run, tag='LAB', posix=posix, verbose=verbose)
        except:
            raise myError("openRunError: "+str(run))
        if max_image_to_read == 0:
            max_image_to_read=cfile.max_pic
        print ("WARNING: pdestal from %d to %d" % (min_image_to_read, max_image_to_read))

        m_image = np.zeros((cfile.x_resolution, cfile.y_resolution), dtype=np.float64)
        s_image = np.zeros((cfile.x_resolution, cfile.y_resolution), dtype=np.float64)

        n0 = 0
        for iTr in tqdm.tqdm(range(min_image_to_read, max_image_to_read)):
            image = rtnp.hist2array(cfile.file.Get(cfile.pic[iTr])).T
            image[image<0]=99 #pach per aclune imagini
            m_image += image
            s_image += image**2 
            if verbose and n0 > 0 and n0 % 10==0:  # print progress and debung info for poit 200, 200...
                print ("Debug Image[200,200]: %d => %.2f %.2f %.2f " % (iTr,
                                                image[200,200],
                                                np.sqrt((s_image[200,200] - 
                                                        m_image[200,200]**2 
                                                          / (n0+1)) / n0),
                                                m_image[200,200]/(n0+1),
                                                ))
            n0 += 1
        m_image = m_image/n0
        
        s_image = np.sqrt((s_image - m_image**2 * n0) / (n0 - 1))
        m_image[np.isnan(s_image)==True]=m_image.mean() # pach per i valori insani di sigma e media
        s_image[np.isnan(s_image)==True]=1024
        
       
        ###### print Info and Save OutPut ######################################
        print("WRITING ...")
        write2root(fileoutm, m_image, id=0, option='recreate')
        write2root(fileouts, s_image, id=0, option='recreate')
        print("DONE OUTPUT maen file: {:s} sigma file: {:s}".format(fileoutm, fileouts))
        return m_image, s_image    

def read_cygno_logbook(sql=True, verbose=False):
    import pandas as pd
    import numpy as np
    import requests
    if sql:
        url = "http://lnf.infn.it/~mazzitel/php/cygno_sql_query.php"
        r = requests.get(url, verify=False)
        df = pd.read_json(url)
        columns = ["varible", "value"]       
    else:
        key="1y7KhjmAxXEgcvzMv9v3c0u9ivZVylWp7Z_pY3zyL9F8" # Log Book
        url_csv_file = "https://docs.google.com/spreadsheet/ccc?key="+key+"&output=csv"
        df = pd.read_csv(url_csv_file)
        df = df[df.File_Number.isnull() == False]
        for name in df.columns:
            if name.startswith('Unnamed:'):
                df=df.drop([name], axis=1)
        isacomment = False
        runp = df.File_Number[0]
        for run in df.File_Number:

            if not run.isnumeric():
                if isacomment == False and verbose: print("To Run {}".format(runp)) 
                isacomment = True
                if verbose: print ("--> General comment: {}".format(run))
                index = df[df.File_Number==run].index[0]
                df=df.drop([index], axis=0)
            else:
                if isacomment and verbose: print("From Run {}".format(run)); isacomment = False
            runp = run
        if verbose: print ('Variables: ', df.columns.values)
    return df

def run_info_logbook(run, sql=True, verbose=False):
    dataInfo=read_cygno_logbook(sql=sql,verbose=verbose)
    if sql:
        out = dataInfo[dataInfo['Run number']==run]
    else:
        out =  dataInfo[dataInfo.File_Number==str(run)]
    if verbose: print(out.values)
    if len(out.values)==0:
        print("NO RUN "+str(run)+" found in history")
    return out

#
# ROOT cygno tool and image tool
#

def cluster_par(xc, yc, image):
    ph = 0.
    dim = xc.shape[0]
    for j in range(0, dim):
        x = int(xc[j])
        y = int(yc[j])
        ph += (image[y,x]) # waring Y prima di X non e' un errore!
    return ph, dim

def n_std_rectangle(x, y, ax, image = np.array([]), n_std=3.0, facecolor='none', **kwargs):
    from matplotlib.patches import Rectangle
    mean_x = x.mean()
    mean_y = y.mean()
    std_x = x.std()
    std_y = y.std()
    half_width = n_std * std_x
    half_height = n_std * std_y
    if image.any():
        rimage = image*0
        xs = int(mean_x - half_width)+1
        xe = int(mean_x + half_width)+1
        ys = int(mean_y - half_height)+1
        ye = int(mean_y + half_height)+1
        # print(ys,ye, xs,xe)
        rimage[ys:ye, xs:xe]=image[ys:ye, xs:xe]
        # print (rimage)
        # print(rimage.sum())
    else:
        rimage = np.array([])
        
    rectangle = Rectangle(
        (mean_x - half_width, mean_y - half_height),
        2 * half_width, 2 * half_height, facecolor=facecolor, **kwargs)
    return ax.add_patch(rectangle), rimage  

def confidence_ellipse(x, y, ax, image = np.array([]), n_std=3.0, facecolor='none', **kwargs):
    from matplotlib.patches import Ellipse
    import matplotlib.transforms as transforms
    import numpy as np

    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0),
        width=ell_radius_x * 2,
        height=ell_radius_y * 2,
        facecolor=facecolor,
        **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)
    if image.any():
        # ellsisse e' (x-x0)**2/a**2 + (y-y0)**2/b**2 < 1
        # print (mean_x, mean_y, ell_radius_x*scale_x, ell_radius_y*scale_y)
        rimage = image*0
        ar = abs(pearson)
        for x in range(image.shape[1]):
            for y in range(image.shape[0]):
                xr = (y-mean_y)*np.sin(ar)+(x-mean_x)*np.cos(ar)
                yr = (y-mean_y)*np.cos(ar)-(x-mean_x)*np.sin(ar)
                if (xr)**2/(ell_radius_x*scale_x)**2 + (yr)**2/(ell_radius_y*scale_y)**2 < 1:
                    rimage[y,x]=image[y, x]
        # print (rimage)
        # print(rimage.sum())
    else:
        rimage = np.array([])
    
    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)

    return ax.add_patch(ellipse), rimage 

def confidence_ellipse_par(x, y, image = np.array([]), n_std=3.0, facecolor='none', **kwargs):
    import numpy as np

    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])

    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
                           
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)
                           
    width=scale_x*ell_radius_x * 2 
    height=scale_y*ell_radius_y * 2              
    if image.any():
        # ellsisse e' (x-x0)**2/a**2 + (y-y0)**2/b**2 < 1
        # print (mean_x, mean_y, ell_radius_x*scale_x, ell_radius_y*scale_y)
        rimage = image*0
        ar = abs(pearson)
        for x in range(image.shape[1]):
            for y in range(image.shape[0]):
                xr = (y-mean_y)*np.sin(ar)+(x-mean_x)*np.cos(ar)
                yr = (y-mean_y)*np.cos(ar)-(x-mean_x)*np.sin(ar)
                if (xr)**2/(ell_radius_x*scale_x)**2 + (yr)**2/(ell_radius_y*scale_y)**2 < 1:
                    rimage[y,x]=image[y, x]
        # print (rimage)
        # print(rimage.sum())
    else:
        rimage = np.array([])

    
    return width, height, pearson, rimage.sum(), np.size(rimage[rimage>0])

def cluster_elips(points):
    import numpy as np
    x0i= np.argmin(points[:,1])
    a0 = points[x0i][1]
    x1i= np.argmax(points[:,1])
    a1 = points[x1i][1]
    y0i= np.argmin(points[:,0])
    b0 = points[y0i][0]
    y1i= np.argmax(points[:,0])
    b1 = points[y1i][0]
    #print (a0, a1, b0, b1, x0i, points[x0i])
    a  = (a1 - a0)/2.
    b  = (b1 - b0)/2.
    x0 = (a1 + a0)/2.
    y0 = (b1 + b0)/2.
    theta = np.arctan((points[x1i][0]-points[x0i][0])/(points[x1i][1]-points[x0i][1]))
    return x0, y0, a , b, theta

def poit_3d(points, image):
    ########### if 3D #############
    points_3d = []
    for j in range(len(points)):
        y = points[j,0]
        x = points[j,1]
        z = image[int(y),int(x)] # non è un errore Y al posto di X causa asse invertito in python delle imagine
        points_3d.append([y,x,z]) 

    return points_3d

def rebin(a, shape):
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    return a.reshape(sh).mean(-1).mean(1)

def smooth(y, box_pts):
    import numpy as np
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def img_proj(img, vmin, vmax, log=False):
    import matplotlib.pyplot as plt
    import numpy as np
    print('INFO: mean: {:.2f}, sigma: {:.2f}, N out of range: {} < vmin={}, {} > vmax={}, insane: {}'.format(
        img.mean(), img.std(), len(img[img<vmin]), vmin, len(img[img>vmax]),vmax, 
        len(img[np.isnan(img)==True])))
    fig, ax = plt.subplots(2,2, figsize=(10,10))
    ax[0,0].imshow(img,  cmap="jet", vmin=vmin,vmax=vmax, aspect="auto")
    x = np.linspace(img.shape[1], 1, img.shape[1])
    #x = np.linspace(1, img.shape[0], img.shape[0])
    ax[0,1].plot(np.sum(img, axis=1),x , 'b-')
    
    x = np.linspace(1, img.shape[0], img.shape[0])
    ax[1,0].plot(x, np.sum(img, axis=0), 'r-')
    ax[1,1].hist(img.ravel(), bins=vmax-vmin, range=(vmin,vmax))
    if log: ax[1,1].set_yscale('log')
    plt.show()

