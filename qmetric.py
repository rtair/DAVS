




class qoemetric:

    def __init__(self):
        pass




    # this method used to calculater player instability


    def calcinstability(self,ds):

        instability=0.0


        tmpvalue=0
        for i in range(0,len(ds)):

            if(i==0):
                tmpvalue = int(ds[i])

            else:

                if(int(ds[i])!=tmpvalue):
                    instability = instability+1

                    tmpvalue = int(ds[i])

                else:
                    tmpvalue = int(ds[i])


        return instability





    # this method used to calculate the avg bitrate
    def calcavgbitrate(self,ds):

        avgbitrate=0.0
        tmpcount=0

        for i in range(0,len(ds)):

                avgbitrate =  avgbitrate +float(ds[i])
                tmpcount=tmpcount+1



        avgbitrate = avgbitrate/float(tmpcount)
        return avgbitrate




    # this method used to calculate the number of rebuffering

    def calcrebuffering(self,ds):

        rebuffering=0

        totaltime=0.0


        for i in range(0,len(ds)):

           totaltime = totaltime+1.0

           if(int(ds[i])==0):
               rebuffering =rebuffering+1



        return float(rebuffering)/float(totaltime)



    # this method used to calculate the number of rebuffering

    def calcfairness(self,ds,streamed_bws):

        fairness=0.0


        n = len(ds)

        up=0.0
        down=0.0
        for i in range(0,len(ds)):


            tmpvalue= 0.0
            try:
                tmpvalue = float(ds[i])/float(streamed_bws[i])

            except:
                pass

            up=  up+float(tmpvalue)
            down = down+(float(tmpvalue)*float(tmpvalue))


            fairness =(up*up)/(float(n)*down)



        print(up,down)
        return fairness



    # calculate ssim
    def calculatessim(self,ds,devssim):

        ssim =0.0


        #version 1
        #tmpcount =0
        #for i in range(0,len(ds)):
        #
        #    for j in range(0,len(devssim)):
        #
        #
        #        if (int(ds[i])==int(devssim[j][1])):
        #
        #            ssim = ssim + float(devssim[j][0])
        #            tmpcount =tmpcount+1
        #
        #
        #ssim = float(float(ssim)/float(tmpcount))

        tmpcount=0

        for i in range(0,len(ds)):

            for j in range(0,len(devssim)):

                if (int(ds[i])==0):
                    ssim = ssim + 0.0
                    tmpcount=tmpcount+1

                elif (int(ds[i])==int(devssim[j][1])):

                    ssim = ssim + float(devssim[j][0])
                    tmpcount=tmpcount+1




        print(ssim,tmpcount)
        print(devssim)
        print(ds)
        ssim = float(ssim)/float(tmpcount)



        return ssim






    # this method used to calculate the QoE
    def calculateqoe(self,dataset,devssim,streamed_bws):


        # dataset contains  list of [time,bitrate]
        # devssim contains  list of [ssim,bitrate]




        #print(dataset,devssim,streamed_bws)
        # ds1 contains only the bitrates
        ds1=[]
        for i in range(0,len(dataset)):

            ds1.append(dataset[i][1])








        # now i have the bitrates dataset

        # we call diffent methods to evaluate QoE
        #print(dataset)
        startupdelay = dataset[0][0]
        instability = self.calcinstability(ds1)
        avgbitrate = self.calcavgbitrate(ds1)
        rebuffering = self.calcrebuffering(ds1)
        fairness=self.calcfairness(ds1,streamed_bws)
        ssim = self.calculatessim(ds1,devssim)


        return [startupdelay,instability,avgbitrate,rebuffering,ssim,fairness]












