
from __future__ import print_function
from adaptationlogic import *
from dataprocessing import *
import time
from threading import Thread, Lock

from qmetric import *

import os

import csv


# the idea is the player stream the video based on the feedback from the adaptation logic
# the data should be streamed based on the dataset throughput
# the QoE class will evaluate the user QoE









# Resolution:
#240p (427x240)
#380p (676x380)
#480p (858x480)
#720p (1280x720)
#1080p (1920x1080)
#1080p (1920x1080)
#2160p (3840x2160)





class player:
    # trace_ds reffer to dataset which is the bandwith trace
    # device dspec  refer to device
    # al refer to the adaptation logic
    # stoptime refer to the sim stop time
    #bmax max buffer size




    trace_ds = None
    dspec= 1
    alid =1 # default adaptation logic bba
    stoptime=0.0
    sim_runtime=0 # the simulation  runtime  (time when the simulator start)


    buffer = []  # the player buffer

    bmax=float(120)  # max buffer size

    chunkduration =4.0  # the chunk duration in seconds  (the same used by netflix)
    lock = Lock() # lock for the program

    # chunk sizes
    #list of all chuncks with diffrent sizes

    #avilable bitrates
    available_bitrates =None
    #chunks file name
    chunks_filename=None


    streamed_bitrates=None

    streamed_bw=None

    player_end=None

    alname=None
    dsname=None


    def __init__(self,_trace_ds,_dspec,_alid,_stoptime,_bmax,_available_bitrates,_chunck_silename,alname,dsname):

        self.dspec =_dspec
        self.trace_ds =_trace_ds
        self.alid=_alid
        self.stoptime=float(_stoptime)
        self.bmax =float(_bmax)
        self.available_bitrates=_available_bitrates
        self.chunks_filename = _chunck_silename
        self.streamed_bitrates = []
        self.streamed_bw = []

        self.player_end=False

        self.buffer = []
        lock = Lock() # lock for the program

        self.alname=alname
        self.dsname=dsname



    #check the player status

    def isplayerfinished(self):
        return self.player_end

    # get the streamed time and bitrates
    def getstreamedbandwidth(self):

        return self.streamed_bw


    # get the streamed time and bitrates
    def getstreamedbitratesandtime(self):

        return self.streamed_bitrates

     # this method reffer to the start of the player
    def start_streaming(self):

        # use two methods one for download the video and the second forplay the video

        self.sim_runtime = time.time()

        # thos method will run chunckdownload and chucnkplay methods which are based on producer-consumer design pattern





        # global values for the threads
        # lock , buffer and stoptime
        #trace ds , the global trace dataset
        #device specification
        # adaptaipn logic
        #max buffer size
        #chunk duration
        #chunk list sizes

        lock = self.lock
        buffer = self.buffer
        sim_toptime= self.sim_runtime+self.stoptime
        trace_ds = self.trace_ds
        dspec= self.dspec
        alid=self.alid
        bmax=self.bmax
        chunkduration =self.chunkduration

        chunks_filename=self.chunks_filename
        sim_runtime = self.sim_runtime
        available_bitrates=self.available_bitrates
        streamed_bitrates=self.streamed_bitrates
        streamed_bw  = self.streamed_bw

        player_end = self.player_end

        alname=self.alname
        dsname=self.dsname


        class ChunckDownload(Thread):

            # lock for the program
            global lock
            global buffer
            global  sim_toptime
            global trace_ds
            global dspec
            global alid
            global bmax
            global chunkduration
            global available_bitrates
            global chunks_filename
            global sim_runtime


            def run(self):



                print("Start ChunckDownload")
                alogic = adaptationlogic()


                timetodownloadlastchunk= 0.0
                estimatedth =0.0


                extra_fromlastdownload =0.0
                time_form_extra_fromlastdownload=0.0
                tarce_pointer=0  # pointer to the current point in the trace
                chunkcount=0



                while True:
                    if(time.time()> sim_toptime):

                        print("Simulation Stop")
                        break




                    #this is used for thread sleep
                    timetowait=0.0

                    #start the application
                    lock.acquire()





                    # the bitrate pointer and value
                    j=0
                    next_bitrate=0
                    chunk_list_sizes = None



                    # read the chunks sizes

                    file = open(chunks_filename)

                    filecsv= csv.reader(file)


                    tmpcount =0 # temporarly variable
                    for row in filecsv:



                        chunk_list_sizes = [float(row[1])*1000.0*8,float(row[2])*1000.0*8,float(row[3])*1000.0*8,float(row[4])*1000.0*8,float(row[5])*1000.0*8,float(row[6])*1000.0*8,float(row[7])*1000.0*8,float(row[8])*1000.0*8,float(row[9])*1000.0*8,float(row[10])*1000.0*8]

                        if(tmpcount==chunkcount):
                            break
                        tmpcount = tmpcount+1




                    # the buffer is full wait for one second at least and try again
                    if(len(buffer)>(int(bmax)-int(chunkduration))):
                        timetowait = 1.0
                        tarce_pointer = tarce_pointer+1
                        print("buffer is full")


                    else:

                        #print("buffer is not full")

                        j,next_bitrate = alogic.alladaptationlogiccall(alid,bmax,len(buffer),chunkduration,timetodownloadlastchunk,estimatedth,dspec,available_bitrates,chunk_list_sizes,time.time()-sim_runtime,trace_ds)





                        # start the download procedure



                        needed_bw=0.0
                        chunk_size = chunk_list_sizes[j] * 1.3 # since c =0.3 and we need (1+c) *chunkesize as bandwidth
                        need_slots=0 # the extra slots neded to download next chunk

                        #  first we test if one slot is enough or note

                        # the start of the download


                        #


                        if(chunkcount==0):


                            tmptarce_pointer= tarce_pointer
                            while(needed_bw<chunk_size):
                                needed_bw = needed_bw + float(trace_ds[tmptarce_pointer])
                                tmptarce_pointer = tmptarce_pointer+1
                                need_slots = need_slots+1



                            extra_fromlastdownload = float(needed_bw-chunk_size)
                            time_form_extra_fromlastdownload = (extra_fromlastdownload/float(needed_bw))*float(need_slots)


                            estimatedth = (chunk_size)/float(need_slots-time_form_extra_fromlastdownload)
                            timetodownloadlastchunk = float(need_slots) -time_form_extra_fromlastdownload


                            timetowait= timetodownloadlastchunk+time_form_extra_fromlastdownload




                        else:

                            
                            needed_bw = needed_bw +extra_fromlastdownload
                            




                            tmptarce_pointer= tarce_pointer
                            while(needed_bw<chunk_size):
                                needed_bw = needed_bw + float(trace_ds[tmptarce_pointer])
                                tmptarce_pointer = tmptarce_pointer+1
                                need_slots = need_slots+1



                            tmp = time_form_extra_fromlastdownload  # save it temporarly
                            extra_fromlastdownload = float(needed_bw-chunk_size)
                            
                            
                            
                            

                        
                        
                        


                            if(need_slots==0):
                                
                                #print("condition 1")
                                time_form_extra_fromlastdownload = (extra_fromlastdownload/float(needed_bw))*float(tmp)
                                
                                
                                estimatedth = (chunk_size)/float(float(tmp)-time_form_extra_fromlastdownload)
                                timetodownloadlastchunk = float(tmp) -time_form_extra_fromlastdownload
                                
                                
                                timetowait=0.0

                            else:

                                time_form_extra_fromlastdownload = (extra_fromlastdownload/float(needed_bw))*float(need_slots)
                                
                                
                                estimatedth = (chunk_size)/float(need_slots-time_form_extra_fromlastdownload)
                                #estimatedth = (((float(needed_bw)-extra_fromlastdownload))/float(needed_bw))*float(need_slots)
                                timetodownloadlastchunk = float(need_slots) -time_form_extra_fromlastdownload
                                #print("condition 2",need_slots,needed_bw,chunk_size,extra_fromlastdownload,time_form_extra_fromlastdownload,estimatedth,timetodownloadlastchunk,timetowait)


                                timetowait= timetodownloadlastchunk+time_form_extra_fromlastdownload

                        chunkcount = chunkcount+1

                        tarce_pointer = tarce_pointer+need_slots


                        for i in range(0,int(chunkduration)):
                            buffer.append([next_bitrate,estimatedth])


                    lock.release()
                    time.sleep(timetowait)



                print("ChunckDownload finished")

        class ChunckPlay(Thread):

                    # lock for the program
                    global lock
                    global buffer
                    global  sim_toptime
                    global bmax
                    global sim_runtime
                    global streamed_bitrates
                    global streamed_bw

                    global alname
                    global  dsname
                    def run(self):


                        startup = True
                        printonce=True
                        sleptime=0.0
                        tmpplaylastbitrate=0 # the last bitrate
                        while True:



                            sleptime=0.1
                            if(time.time()> sim_toptime):
                                #print("ChunckPlay start1.................................")

                                break

                            lock.acquire()

                            # the play will start after filling the buffer 0.1 * bmax
                            if(len(buffer)>=3*4 and startup):   # cd * 3 segments

                                #print("ChunckPlay start2..............................")

                                startup = False
                                sleptime=0.1


                            elif(not startup ):

                                if printonce:
                                    print("Start ChunckPlay")
                                    printonce=False

                                #print("ChunckPlay start3.................................")

                                if(len(buffer)>0):
                                    #print("ChunckPlay start4...................................")


                                    datatmp=buffer.pop(0)
                                    tmpbitrate = int(datatmp[0])
                                    tmpebw = float(datatmp[1])



                                    tmptime= str(time.time()-sim_runtime)
                                    #file = open("log/alllog.txt","ab+")
                                    file = open("log/" + str(algname) + "-" + str(buffer_size) + ".log", "ab+")

                                    #for i in range(0,10):

                                    #    streamed_bitrates.append([tmptime,tmpbitrate])
                                    #    streamed_bw.append(tmpebw)

                                    #    output=str(dsname)+","+str(algname)+","+str(float(tmptime)+(0.1*i))+ ",client_stream_at_rate,"+str(tmpbitrate)+",buffer_occupancy,"+str(len(buffer))+",estimated_throughput,"+str(tmpebw)+ "\n"
                                    #    file.write(output)
                                        #print(output)
                                    

                                    streamed_bitrates.append([tmptime,tmpbitrate])
                                    streamed_bw.append(tmpebw)

                                    output=str(dsname)+","+str(algname)+","+str(float(tmptime)+(0.1*i))+ ",client_stream_at_rate,"+str(tmpbitrate)+",buffer_occupancy,"+str(len(buffer))+",estimated_throughput,"+str(tmpebw)+ "\n"
                                    file.write(output)

                                    file.close()
                                    sleptime=1.0
                                else:
                                    #print("ChunckPlay start5............................")
                                    tmpbitrate = 0
                                    tmpebw = float(0)
                                    tmptime= str(time.time()-sim_runtime)
                                    streamed_bitrates.append([tmptime,tmpbitrate])
                                    streamed_bw.append(tmpebw)
                                    file = open("log/"+str(algname) + "-" + str(buffer_size) + ".log", "ab+")
                                    #file = open("alllog.txt","ab+")
                                    output=str(dsname)+","+str(algname)+","+str(tmptime)+ ",client_stream_at_rate,"+str(tmpbitrate)+",buffer_occupancy,"+str(0)+",estimated_throughput,"+str(tmpebw)+ "\n"
                                    file.write(output)
                                    file.close()
                                    sleptime=1  # was 0.1
                                    #print(output)

                            lock.release()
                            time.sleep(sleptime)# the player will check every 100 ms

                        print("ChunckPlay finished................................")



        print("Simulation Start")
        cd = ChunckDownload()
        cd.start()



        cd = ChunckPlay()
        cd.start()








if __name__=="__main__":
    # run example


    try:
        #os.system("rm  -Rf 30/*")
        #os.system("rm  -Rf 60/*")
        #os.system("rm  -Rf 90/*")
        #os.system("rm  -Rf 120/*")
        #os.system("rm  -Rf 240/*")
        #os.system("rm  -Rf log/*")
        pass

    except:
        pass


    simtime = 370
    #bitrates=[400,750,1250,2200,4000,8000]
    bitrates = [235, 375, 560, 750,1050, 1750, 2350,3000,4300,5000]

    chunksfilename = "nf-chunks.csv"
    dspec_id=1


    devssim1 = [[0.830, 235], [0.862, 375], [0.897, 560], [0.906, 750], [ 0.931, 1050],[0.946, 1750],[ 0.971, 2350], [0.974, 3000], [0.986, 4300], [1.0, 5000]]
    for y in [120]:  # 60,90,120,240
        buffer_size= int(y)





        output=""




        # QoE evaluation method
        qoe_eva = qoemetric()

        #print("dsname","alg","startupdelay,instability,avgbitrate,rebuffering,ssim")
        for j in [1,2,3]: # number of adaptation logics 0,1,2,3,4,5,6,7,8


            for i in range (0,3): # number of data sets


                dsname="ds"+str(i+1)+".txt"








                dp = dataprocessing()
                ds1 = dp.processdata(dsname)


                #parameters for bba :  buffersize, bufferocupancy,available_bitrates
                #parameters for festive: estimatedth,available_bitrates
                #parameters for sara: buffersize, bufferocupancy,chunkduration,estimatedth,available_bitrates,available_bitrates_sizes
                #parameters of omsf: chunkduration,timetodownloadlastchunk,available_bitrates
                #parameters for sa : estimatedth,available_bitrates


                alid=j


                algname = ""
                if j==0:
                        algname="bba"
                elif j==1:
                        algname="festive"


                elif j==2:
                        algname="sara"


                elif j==3:
                        algname="omsf"
                elif j==4:
                        algname="sa"

                elif j==5:
                        algname="dashjs"

                elif j==7:
                        algname="vlc"
                elif j==8:
                        algname="bbapsqa"
                elif j==9:
                        algname="psqa2"
                print("play",dsname,algname)
                a = player(ds1,dspec_id,alid+1,simtime,buffer_size,bitrates,chunksfilename,algname,dsname) # dataset,device specification, adaptation logic and stoptime
                a.start_streaming()



                # dataset contains  list of [time,bitrate]
                # devssim contains  list of [ssim,bitrate]



                # the devices that we used to evaluate the QoE are
                # 1080 x 1920  ---Samsung Galaxy A7   --dev1
                # 1080 x 1920  ---Apple iPhone 6s Plus --dev1
                # 768 x 1280    ---LG Nexus 4 --dev2
                # 768 x 1024   ---Samsung Galaxy Tab A 9.7



                #wait for simtime+1 before get the data
                time.sleep(10+simtime)


                streamed_bitrates=a.getstreamedbitratesandtime()

                streamed_bws=a.getstreamedbandwidth()









                results = qoe_eva.calculateqoe(streamed_bitrates,devssim1,streamed_bws)
                output = dsname + ","+algname+","+ str(results[0]) +","+str(results[1]) +","+str(results[2]) +","+str(results[3]) +","+str(results[4]) + ","+str(results[5]) +"\n"



                file = open(str(buffer_size)+"/"+str(algname)+".csv","ab+")
                file.write(output)


                print(output)
                file.close()







                # Resolution:
                #240p (427x240)
                #380p (676x380)
                #480p (858x480)
                #720p (1280x720)
                #1080p (1920x1080)
                #1080p (1920x1080)
                #2160p (3840x2160)

                #Bitrate
                #400 Kbps
                #750 Kbps
                #1250 Kbps
                #2500 Kbps
                #4000 Kbps
                #8000 Kbps




        print("Done.....")





