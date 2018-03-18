from __future__ import print_function
import statistics
import csv


class dataprocessing:
    def __init__(self):
        pass


    # this method used to process data
    # data return in Kbps
    def processdata(self,filename):

        #print(filename)

        data = []
        file = open(filename)
        for row in file:



            value = str(row).split("Bytes")[1].split("bits")[0]

            if(value.__contains__("K")):

                #print(float(value.split("K")[0]))
                data.append(float(value.split("K")[0]))
            elif(value.__contains__("M")):
                data.append(float(value.split("M")[0])*1000)

            else:


                x = float(value.split("bits")[0])/1000
                data.append(x)


                #print(float(value.split("M")[0])*1000)

        return data






if __name__=="__main__":



    dsname="ds"

    for i in range(0,30):
        a = dataprocessing()
        y = a.processdata("ds"+str(i+1)+".txt")

        avg =0.0
        for j in range(0,len(y)):
            avg = avg +y [j]
        #print("ds"+str(i+1)+".txt",avg/float(len(y)))

        print(str("y"+str(i+1)+"=")+str(y)+";")


    x ="x= ["
    for i in range(1,601):
        x = x + " "+str(i) + ","

    x =x +"]"
    print(x)

    """
    x = []
    for i in range(0,len(y)):
        x.append(i+1)


    plot = plotdata()

    plot.plotdata(x,y,"Time (Seconds)","Throughput (Kbps)","Channel Capacity")
    y = a.processdata("ds2.txt")
    x = []
    for i in range(0,len(y)):
        x.append(i+1)


    plot = plotdata()

    plot.plotdata(x,y,"Time (Seconds)","Throughput (Kbps)","Channel Capacity")
    """


    data = []
    for x in range(0,30):
        a = dataprocessing()
        y = a.processdata("ds"+str(x+1)+".txt")

        data.append(statistics.mean(y))

    print(data)
    print(statistics.mean(data))
    print(sorted(data))


