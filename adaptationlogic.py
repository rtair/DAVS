from __future__ import print_function
import math
import random
import time



# this is the base class for all adaptation logics
class adaptationlogic:



    bba_chunkcount=0
    bba_lastj=0
    bba_startup= True # 0 means bandwidth estimation,1 buffer based

    bba_lastchunksize=0

    festive_eth = []# festive list of throughput
    festive_w = 5  # festive window
    festive_j =[] # festive lasst bw

    sa_alpha = 0.8  # festive window
    sa_eth=0.0

    osmf_lastrate=0.0

    sara_lastrate=0
    sara_w=5 # sara window
    sara_eth= [] # sara rates
    sara_chunksize= [] # sara rates


    rabeealg1_dth = 4.0


    #dashjs_b =0.0
    #dashjs_w1=1.3
    #dashjs_w2=0.7
    dashjs_eth = []
    ####

    decesiontobreak=False
    #####
    rabee_alg1_w =5
    rabee_alg1_eth=[]
    rabee_alg1_dtime=[]
    rabee_alg1_lastbitrate=0
    rabeealg1_chunkcount=0
    rabeealg1_leth=0
    rabeealg1_lastchunksize=0
    rabeealg1_lastj=0
    rabeealg1_dth = 16.0 # delay threshould
    rabeealg1_startup =True
    rabeealg1_delay = 0.0
    rabeealg1_numberupdatedecision = 0
    rabeealg1_windowupdatedecision = 3
    rabeealg1_updatedecisionhappend = False
    psqa2_lastj=0
    psqa2_chunkcount=0
    psqa2_lasttime=0.0
    def __init__(self):


        self.festive_eth = []
        self.festive_j= []

        self.sara_eth= [] # sara rates
        self.sara_chunksize= [] # sara rates

        self.dashjs_eth = []
        self.rabee_alg1_eth=[]
        self.rabee_alg1_lastbitrate=0
        self.bba_chunkcount=0
        self.bba_lastj=0
        self.decesiontobreak=False
        self.bba_startup=True
        self.rabeealg1_chunkcount=0
        self.rabeealg1_leth=0
        self.rabeealg1_lastchunksize=0
        self.rabeealg1_lastj=0
        self.rabee_alg1_dtime=[]
        self.bba_lastchunksize=0

        self.rabeealg1_startup =True
        self.rabeealg1_delay = 16.0

        self.rabeealg1_numberupdatedecision = 0
        self.rabeealg1_windowupdatedecision = 3
        self.rabeealg1_updatedecisionhappend = False
        self.psqa2_chunkcount=0
        self.psqa2_lastj=0
        self.psqa2_lasttime=0.0

    def bbapsqa(self,buffersize, bufferocupancy,available_bitrates,chunkduration,available_bitrates_sizes,estimatedth):

        # this algorithm is based on BBA


        bs = float(buffersize)
        bo = float(bufferocupancy)

        cd = chunkduration
        ebw=estimatedth
        rates = available_bitrates
        chunksizes=available_bitrates_sizes


        # next bitrate
        next_bitrate=0
        j=0  # map the rate



        # defaulr parameters from the paper
        r = 0.375 * 0.1
        c = 0.90-r




        # BBA is based on chunk size







        # Condition 1 the chunk count is zero
        if(self.bba_chunkcount<1):# the buffer is just start

             next_bitrate=rates[0]


        # Condition 2 the chunk count more than zero
        else:

            # BBA use the chunk size as signal


            db =  float(cd) - float(self.bba_lastchunksize)/float(estimatedth)



            if(db<0.0 or bo>float(r+c)*float(bs)):  # stop start up if buffer is decreassing

                self.bba_startup=False


            # Case 1 calculate startup
            # condition 1



            tmpj1=0  # j from start app algorithm
            tmpj2=0  # j from bba1


            slope=0.0
            if(self.bba_startup): #


                try:
                    slope =  float(6.0 * float(float(float(bs)*float(r+c))-float(bo)) )/float(float(bs)*float(r+c))

                except:

                     slope=2.0



                if(float(db)>float(float(1)-float(1.0/slope))*float(cd)):
                    tmpj1 = self.bba_lastj+1
                else:
                    tmpj1 = self.bba_lastj





            # find the BBA algorithm
            if(bo<float(r*bs)):

                #print("case1")

                # case1
                tmpj2=0

            # condition 2

            elif(bo>=(r*bs) and bo<=((r+c)*bs) )   :
                #print("case2")

                x= float(rates[0])
                y= (float(bo/bs)-r)/c
                z= float(rates[len(rates)-1]-rates[0])
                #estimated rate
                rk = x + (y*z)


                for i in range(0 , len(rates)):
                    if(rk>float(rates[i])):
                            tmpj2=i
                    else:
                        break

            # condition 3

            else:
                #print("case3")

               tmpj2=len(rates)-1






            if(self.bba_startup):
                j=max(tmpj1,tmpj2)

                if(tmpj2>tmpj1):
                    self.bba_startup=False

            else:
                j=tmpj2



        try:
            pass
            #print(tmpj1,tmpj2,j)
        except:
            pass


        if(j>len(rates)-1):
            j = len(rates)-1
        if(j<0):
            j=0
        next_bitrate = rates[j]
        self.bba_chunkcount = self.bba_chunkcount+1
        self.bba_lastj=j
        self.bba_lastchunksize=available_bitrates_sizes[j]


        #print(j,bo,bs)

        return j,next_bitrate
    def psqa2(self,buffersize, bufferocupancy,available_bitrates,chunkduration,available_bitrates_sizes,estimatedth,simtime):

        # this algorithm is based on BBA


        bs = float(buffersize)
        bo = float(bufferocupancy)



        print("bo",bo)

        cd = chunkduration
        ebw=estimatedth
        rates = available_bitrates
        chunksizes=available_bitrates_sizes

        t=10.0
        # next bitrate

        l=2
        next_bitrate=0
        j=0  # map the rate


        if(self.psqa2_chunkcount==0):
            j=0
            self.psqa2_lasttime=simtime
        else:

            if(simtime>self.psqa2_lasttime+t):
                self.psqa2_lasttime = simtime
                a= float(float(float(bo)+float(t))/float(t))
                f = 0.5*float(ebw) * a
                tmpj=0
                for i in range(0,len(rates)):
                    if(f>=float(rates[i])):
                        tmpj=i




                if(tmpj>self.psqa2_lastj):
                    if(tmpj>=self.psqa2_lastj+l):

                        j=self.psqa2_lastj+l
                    else:
                        j=self.psqa2_lastj

                else:
                    if(tmpj<=self.psqa2_lastj-l):

                        j=self.psqa2_lastj-l
                    else:
                        j=self.psqa2_lastj

            else:

                j=self.psqa2_lastj


            if(j<0):
                j=0

        next_bitrate=rates[j]
        self.psqa2_chunkcount =self.psqa2_chunkcount+1
        self.psqa2_lastj=j
        print(simtime,j,next_bitrate,bo)
        return j,next_bitrate

    # bba use the occupation as function to request the next bitrate
    # inputs are buffersize, bufferocupancy and available_bitrates
    # outputs the next chunk bitrate and map ex: rate and [0-6]



    #Refrence
    #@inproceedings{yin2014toward,
    #title={Toward a principled framework to design dynamic adaptive streaming algorithms over http},
    #author={Yin, Xiaoqi and Sekar, Vyas and Sinopoli, Bruno},
    #booktitle={Proceedings of the 13th ACM Workshop on Hot Topics in Networks},
    #pages={9},
    #year={2014},
    #organization={ACM}
    #}

    def bba(self,buffersize, bufferocupancy,available_bitrates,chunkduration,available_bitrates_sizes,estimatedth):

        # this algorithm is based on BBA


        bs = float(buffersize)
        bo = float(bufferocupancy)

        cd = chunkduration
        ebw=estimatedth
        rates = available_bitrates
        chunksizes=available_bitrates_sizes


        # next bitrate
        next_bitrate=0
        j=0  # map the rate



        # defaulr parameters from the paper
        r = 0.375
        c = 0.90-r




        # BBA is based on chunk size







        # Condition 1 the chunk count is zero
        if(self.bba_chunkcount<1):# the buffer is just start

             next_bitrate=rates[0]


        # Condition 2 the chunk count more than zero
        else:

            # BBA use the chunk size as signal


            db =  float(cd) - float(self.bba_lastchunksize)/float(estimatedth)



            if(db<0.0 or bo>float(r+c)*float(bs)):  # stop start up if buffer is decreassing

                self.bba_startup=False


            # Case 1 calculate startup
            # condition 1



            tmpj1=0  # j from start app algorithm
            tmpj2=0  # j from bba1


            slope=0.0
            if(self.bba_startup): #


                try:
                    slope =  float(6.0 * float(float(float(bs)*float(r+c))-float(bo)) )/float(float(bs)*float(r+c))

                except:

                     slope=2.0



                if(float(db)>float(float(1)-float(1.0/slope))*float(cd)):
                    tmpj1 = self.bba_lastj+1
                else:
                    tmpj1 = self.bba_lastj





            # find the BBA algorithm
            if(bo<float(r*bs)):

                #print("case1")

                # case1
                tmpj2=0

            # condition 2

            elif(bo>=(r*bs) and bo<=((r+c)*bs) )   :
                #print("case2")

                x= float(rates[0])
                y= (float(bo/bs)-r)/c
                z= float(rates[len(rates)-1]-rates[0])
                #estimated rate
                rk = x + (y*z)


                for i in range(0 , len(rates)):
                    if(rk>float(rates[i])):
                            tmpj2=i
                    else:
                        break

            # condition 3

            else:
                #print("case3")

               tmpj2=len(rates)-1






            if(self.bba_startup):
                j=max(tmpj1,tmpj2)

                if(tmpj2>tmpj1):
                    self.bba_startup=False

            else:
                j=tmpj2



        try:
            pass
            #print(tmpj1,tmpj2,j)
        except:
            pass


        if(j>len(rates)-1):
            j = len(rates)-1
        if(j<0):
            j=0
        next_bitrate = rates[j]
        self.bba_chunkcount = self.bba_chunkcount+1
        self.bba_lastj=j
        self.bba_lastchunksize=available_bitrates_sizes[j]


        #print(j,bo,bs)

        return j,next_bitrate

    # festive adaptaion logic uses harmonic mean as base
    # input are last estimatedth and available_bitrates
    # outputs the next chunk bitrate and map ex: rate and [0-6]


    #Refrence
    #@inproceedings{jiang2012improving,
    #title={Improving fairness, efficiency, and stability in http-based adaptive video streaming with festive},
    # author={Jiang, Junchen and Sekar, Vyas and Zhang, Hui},
    #booktitle={Proceedings of the 8th international conference on Emerging networking experiments and technologies},
    #pages={97--108},
    #year={2012},
    #organization={ACM}
    #}
    def festive(self,estimatedth,available_bitrates):


        # next bitrate
        next_bitrate=0
        j=0  # map the rate
        rates = available_bitrates
        hm =0.0 # harmonic mean



        # consition 1 the first request
        if(len(self.festive_eth)==0):

            j=0
            next_bitrate = rates[0]
            self.festive_eth.append(next_bitrate)
            hm = next_bitrate
        # consition 2 number of avilable estimated th less the festive window

        elif(len(self.festive_eth)<self.festive_w):


            self.festive_eth.append(float(estimatedth))

            for i in range(0,len(self.festive_eth)):




                hm = hm + 1.0/float(self.festive_eth[i])

            hm = float(len(self.festive_eth))/hm


            for i in range(0 , len(rates)-1):
                if(hm>float(rates[i])):

                    next_bitrate = rates[i]
                    j=i
                else:
                    break
        # consition 2 number of avilable estimated th  more the festive window

        else:


            self.festive_eth.append(float(estimatedth))

            for i in range(0,self.festive_w):

                hm = hm + 1.0/float(self.festive_eth[len(self.festive_eth)-1-i])


            hm = float(self.festive_w)/hm


            for i in range(0 , len(rates)-1):
                if(hm>float(rates[i])):

                    next_bitrate = rates[i]
                    j=i
                else:
                    break

       


        # calculate score 20 seconds = 5chunks

        if(len(self.festive_j)<=5):
            pass # do nothing
        else:

            bref = self.festive_j[len(self.festive_j)-1]
            bcur = j

            nswitch =0 # number of switches

            tmpfv = bref
            for l in range(0,5):

                if(tmpfv == self.festive_j[len(self.festive_j)-1-l]):
                    pass
                else:
                   nswitch = nswitch+1 

                tmpfv =self.festive_j[len(self.festive_j)-1-l ]

            score1 = abs(((float(bref))/(min(float(hm),float(bref))))-1.0) + (12.0*float(float(math.pow(2,nswitch))+1.0))
            score2 = abs(((float(bcur))/(min(float(hm),float(bref))))-1.0) + (12.0*float(float(math.pow(2,nswitch))))


            if score1> score2:
                j=bcur
            else:
                j=bref

            #print("score",score1,score2)


        self.festive_j.append(j)
        return j,next_bitrate



    # sa adaptaion logic uses smoth function
    # input are last estimatedth and available_bitrates
    # outputs the next chunk bitrate and map ex: rate and [0-6]

    # Refrence
    # @inproceedings{akhshabi2012happens,
    #title={What happens when HTTP adaptive streaming players compete for bandwidth?},
    #author={Akhshabi, Saamer and Anantakrishnan, Lakshmi and Begen, Ali C and Dovrolis, Constantine},
    #booktitle={Proceedings of the 22nd international workshop on Network and Operating System Support for Digital Audio and Video},
    #pages={9--14},
    #year={2012},
    #organization={ACM}
    #}
    def sa(self,estimatedth,available_bitrates):


        # next bitrate
        next_bitrate=0
        j=0  # map the rate
        rates = available_bitrates

        next_bitrate = rates[0]



        if self.sa_eth==0.0:
            self.sa_eth=float(next_bitrate)
        else:

            self.sa_eth = (self.sa_alpha*self.sa_eth )+ ((1.0-self.sa_alpha)*estimatedth)

            for i in range(0 , len(rates)-1):
                if(self.sa_eth>float(rates[i])):
                    next_bitrate = rates[i]
                    j=i
                else:
                    break

        return  j, next_bitrate



    # OSMF adaptaion logic uses chunck fetch time
    # input are chunkduration,timetodownloadlastchunk,available_bitrates
    # outputs the next chunk bitrate and map ex: rate and [0-6]

    # Refrence
    # @inproceedings{riad2015channel,
    #title={A channel variation-aware algorithm for enhanced video streaming quality},
    #author={Riad, Mary and Abu-Zeid, Hatem and Hassanein, Hossam S and Tayel, Mazhar and Taha, Ashraf A},
    #booktitle={Local Computer Networks Conference Workshops (LCN Workshops), 2015 IEEE 40th},
    #pages={893--898},
    #year={2015},
    #organization={IEEE}
    #}
    def osmf(self,chunkduration,timetodownloadlastchunk,available_bitrates):

        # next bitrate
        next_bitrate=0
        j=0  # map the rate
        rates = available_bitrates




        if(self.osmf_lastrate==0.0):

            j=0
            next_bitrate = rates[0]
            self.osmf_lastrate=next_bitrate
        else:


            sd = float(chunkduration)
            t=   float(timetodownloadlastchunk)


            beta = sd/t
            r = self.osmf_lastrate


            for i in range(0,len(rates)-1):

                if (r==rates[i]):
                    j=i


            next_bitrate = rates[0]

            r0=rates[0]
            rh=rates[len(rates)-1]

            rd=0
            jd=0
            for i in range(0,len(rates)-1):

                if (r==rates[i]):
                    break
                rd=rates[i]
                jd=i

            if(beta<1):
                if(r>r0):
                    if(beta<((rd/r))):
                        next_bitrate = rates[0]
                        j=0
                    else:
                        next_bitrate=rd
                        j=jd
            else:
                if(r<rh):
                    rp =rates[j]
                    while(rp<rh):
                        j =j+1
                        rp=rates[j]
                        if(beta< float(float(rp)/float(r))):
                            break

        next_bitrate = rates[j]

        self.osmf_lastrate=next_bitrate
        return  j,next_bitrate



    # SARA adaptaion logic uses chunck fetch time
    # input are chunkduration,timetodownloadlastchunk,available_bitrates
    # outputs the next chunk bitrate and map ex: rate and [0-6]

    # Refrence
    # @inproceedings{juluri2015sara,
    #title={SARA: Segment aware rate adaptation algorithm for dynamic adaptive streaming over HTTP},
    #author={Juluri, Parikshit and Tamarapalli, Venkatesh and Medhi, Deep},
    #booktitle={2015 IEEE International Conference on Communication Workshop (ICCW)},
    #pages={1765--1770},
    #year={2015},
    #organization={IEEE}
    #}

    def sara(self,buffersize, bufferocupancy,chunkduration,estimatedth,available_bitrates,available_bitrates_sizes):


        bs = float(buffersize)
        bo = float(bufferocupancy)
        cd = float(chunkduration)
        rates = available_bitrates
        eth = float(estimatedth)
        csizes=available_bitrates_sizes

        w= available_bitrates_sizes




        # this is the default values from the paper
        #bi= (2.0/17.0)*bs
        #balpha= (10.0/17.0)*bs
        #bbeta=(15.0/17.0)*bs
        #bmax=bs
        bi= (3.0/12.0)*bs
        balpha= (6.0/12.0)*bs
        bbeta=(10.0/12.0)*bs
        bmax=bs

        j=0  # the bit  rate index
        next_bitrate = rates[0] # the next bitrate


        # condition 1
        # Fast start

        if(bo<bi):
            next_bitrate = rates[0]
            j=0

            if(estimatedth==0.0):
                self.sara_eth.append(float( rates[0]))
                self.sara_chunksize.append(float(csizes[0]))

            else:
                self.sara_eth.append(float( eth))
                self.sara_chunksize.append(float(csizes[0]))

            self.sara_lastrate=next_bitrate


        else:

            # calculate hn
            hn=0.0

            if(len(self.sara_eth)<self.sara_w):



               print(self.sara_eth,self.sara_w)
               tmp1=0.0
               tmp2=0.0
               for i in range(0,len(self.sara_eth)-1) :
                    tmp1=tmp1+float(self.sara_chunksize[i])
                    tmp2=tmp2+float(float(self.sara_chunksize[i])/float(self.sara_eth[i]))


                    print(self.sara_chunksize[i],self.sara_eth[i])




               print(tmp1,tmp2)
               hn = tmp1/tmp2

            else:

               tmp1=0.0
               tmp2=0.0
               for i in range(0,self.sara_w) :
                    tmp1=tmp1+float(self.sara_chunksize[len(self.sara_eth)-1-i])
                    tmp2=tmp2+float(float(self.sara_chunksize[len(self.sara_chunksize)-i-1])/float(self.sara_eth[len(self.sara_chunksize)-i-1]))

               hn = tmp1/tmp2

            jcurent =0

            for i in range(0,len(rates)):
                if self.sara_lastrate==rates[i]:
                    jcurent=i


            # condition 2


            if (float(csizes[jcurent])/float(hn)) > bo-bi:

                next_bitrate =rates[0]


                j=0

                while(float(csizes[j])/hn< bo-bi  and j < jcurent):
                    j =j+1


                next_bitrate =rates[j]
                self.sara_lastrate=next_bitrate
                self.sara_eth.append(float( eth))
                self.sara_chunksize.append(float(csizes[j]))
            # condition 3

            elif (bo<=balpha):


                if(jcurent>=len(rates)-1):
                    jcurent = jcurent-1

                if(float(csizes[jcurent+1])/hn< bo-bi):
                    jcurent=jcurent+1
                else:
                    pass


                j=jcurent
                next_bitrate =rates[j]
                self.sara_lastrate=next_bitrate
                self.sara_eth.append(float( eth))
                self.sara_chunksize.append(float(csizes[j]))

            # condition 4
            elif(bo<=bbeta):

                if(jcurent>=len(rates)-1):
                    jcurent = jcurent-1
                next_bitrate =rates[jcurent]
                j=jcurent
                while((float(csizes[j])/hn)< bo-bi and j >= jcurent and j< len(rates)-1):
                    j =j+1




                next_bitrate =rates[j]
                self.sara_lastrate=next_bitrate
                self.sara_eth.append(float( eth))
                self.sara_chunksize.append(float(csizes[j]))
            # condition 5

            elif(bo>=bbeta):

                next_bitrate =rates[jcurent]
                j=jcurent

                while(float(csizes[j])/hn< bo-balpha and j >= jcurent  and j< len(rates)-1):
                    j =j+1



                time.sleep(bo-bbeta)
                next_bitrate =rates[j]
                self.sara_lastrate=next_bitrate
                self.sara_eth.append(float( eth))
                self.sara_chunksize.append(float(csizes[j]))
            # condition 6

            else:
                j =jcurent
                next_bitrate=rates[j]
                self.sara_lastrate=next_bitrate
                self.sara_eth.append(float( eth))
                self.sara_chunksize.append(float(csizes[j]))

        return  j,next_bitrate



    def alladaptationlogiccall(self,alid,buffersize, bufferocupancy,chunkduration,timetodownloadlastchunk,estimatedth,dspec,available_bitrates,available_bitrates_sizes,simtime,ds):


        #alid is the adaptation logic id
        #parameters for bba :  buffersize, bufferocupancy,available_bitrates
        #parameters for festive: estimatedth,available_bitrates
        #parameters for sara: buffersize, bufferocupancy,chunkduration,estimatedth,available_bitrates,available_bitrates_sizes
        #parameters of omsf: chunkduration,timetodownloadlastchunk,available_bitrates
        #parameters for sa : estimatedth,available_bitrates
        #dspec device specification


        #print("alooooooooooooooooooooooooic values",alid,buffersize, bufferocupancy,chunkduration,timetodownloadlastchunk,estimatedth,dspec,available_bitrates,available_bitrates_sizes)


        if(alid==1):
            return self.bba(buffersize, bufferocupancy,available_bitrates,chunkduration,available_bitrates_sizes,estimatedth)

        elif(alid==2):
            return self.festive(estimatedth,available_bitrates)


        elif(alid==3):
            return self.sara(buffersize, bufferocupancy,chunkduration,estimatedth,available_bitrates,available_bitrates_sizes)


        elif(alid==4):
            return self.osmf(chunkduration,timetodownloadlastchunk,available_bitrates)
        elif(alid==5):
            return self.sa( estimatedth,available_bitrates)

        elif(alid==6):
            return self.dashjs( estimatedth,buffersize, bufferocupancy,chunkduration,available_bitrates,available_bitrates_sizes)


        elif(alid==8):
                    return self.vlc(buffersize, bufferocupancy,available_bitrates,estimatedth)

        elif(alid==9):
                    return self.bbapsqa(buffersize, bufferocupancy,available_bitrates,chunkduration,available_bitrates_sizes,estimatedth)
        elif(alid==10):
            return self.psqa2(buffersize, bufferocupancy,available_bitrates,chunkduration,available_bitrates_sizes,estimatedth,simtime)
    # DASH-JS adaptaion logic uses smoth function
    # input are last estimatedth and available_bitrates
    # outputs the next chunk bitrate and map ex: rate and [0-6]

    # Refrence
    #@article{timmerer2016adaptation,
    #title={Which Adaptation Logic? An Objective and Subjective Performance Evaluation of HTTP-based Adaptive Media Streaming Systems},
    #author={Timmerer, Christian and Maiero, Matteo and Rainer, Benjamin},
    #journal={arXiv preprint arXiv:1606.00341},
    #year={2016}
    #}


    def dashjs(self,estimatedth,buffersize, bufferocupancy,chunkduration,available_bitrates,available_bitrates_sizes):


        # next bitrate
        next_bitrate=0
        j=0  # map the rate
        rates = available_bitrates

        next_bitrate = rates[0]



        # version 1
        """
        if self.dashjs_b==0.0:
            self.dashjs_b=float(next_bitrate)
        else:



            self.dashjs_b = ((self.dashjs_b*self.dashjs_w1)+(estimatedth*self.dashjs_w2))/(self.dashjs_w1+self.dashjs_w2)


            for i in range(0 , len(rates)-1):
                if(self.dashjs_b>float(rates[i])):
                    next_bitrate = rates[i]
                    j=i
                else:
                    break


        """

        # version 2


        # rule 1  InsufficientBufferRule
        if(int(bufferocupancy)<2):


            if(len(self.dashjs_eth)==0):
                self.dashjs_eth.append(rates[0])  # this if hold only for the first chunk

            self.dashjs_eth.append(estimatedth)
            j=0
            next_bitrate=rates[j]

        # rule 2  BufferOccupancyRule
        elif (float(bufferocupancy)>float(0.75*buffersize)):
            self.dashjs_eth.append(estimatedth)
            j=len(available_bitrates)-1
            next_bitrate=rates[j]

        else:

            self.dashjs_eth.append(estimatedth)



            tmpbw =0.0
            #rule 3 ThroughputRule



            tmpcount = len(self.dashjs_eth)

            if(tmpcount>2):  # this conition to make sure i have more than three lasb bw
                tmpcount = 3
            for i in range(0,int(tmpcount)):
                tmpbw = tmpbw + self.dashjs_eth[len(self.dashjs_eth)-i-1]

            tmpbw = float(tmpbw/float(tmpcount))  # the last three  values average

            j=0

            next_bitrate=rates[j]

            for i in range(0,len(available_bitrates)):

                if(tmpbw>float(rates[i])):
                    next_bitrate = rates[i]
                    j=i
                else:
                    break





            #rule 4 AbandonRequestsRule

            # keep or leave

            if((float(available_bitrates_sizes[j])/float(tmpbw))>float(chunkduration)*1.5):

                # I should reduce  one rate
                j = j-1
                next_bitrate= rates[j]





        return  j, next_bitrate
    def vlc(self,buffersize, bufferocupancy,available_bitrates,estimatedth):


        j =0

        if(float(bufferocupancy)<float(buffersize*0.6)):
            j=0

        else:

            for i in range(0,len(available_bitrates)):

                if(estimatedth>available_bitrates[i]):
                    j = i
                else:
                    break



        return j,available_bitrates[j]






if __name__=="__main__":

    al = adaptationlogic()
    for i in range(0,30):

        #print(i,al.bba(120,i*4,[300,500,900,2200,4000,8000]))


        #x =random.randint(300,10000)
        #print(i,x,al.festive(x,[300,500,900,2200,4000,8000]))



        #x =random.randint(300,10000)
        #print(i,x,al.sa(x,[300,500,900,2200,4000,8000]))


        #x =random.random()*10
        #print(i,x,al.osmf(4,x,[300,500,900,2200,4000,8000]))


        #x =random.randint(10,10000)
        #print(i,x,al.sara(240,i*4,4,i*500,[300,500,900,2200,4000,8000],[x,2*x,3*x,4*x,5*x,6*x]))

        x =random.randint(6000,10000)
        print(i,x,al.dashjs(x,[300,500,900,2200,4000,8000]))







