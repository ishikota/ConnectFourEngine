import csv
'''
Utility class to use GA
'''
class Util:

    '''
    write down given data 'val' into csv file.
    @param
        f_name  : file name to save (without .csv)
        val     : array of values to save
    '''
    def writeCSV(self, f_name, val):
        f_name += '.csv'
        with open(f_name,'wb') as csvfile:
            w = csv.writer(csvfile, delimiter=',', quotechar='|',quoting=csv.QUOTE_MINIMAL)
            w.writerow(val)

    def readCSV(self, f_name):
        data = []
        f_name += '.csv'
        with open('f_name', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # do not read header
            for row in reader:
                data.append(row)
        return data

    '''
    display chromosome in suitable way for debug
    @param
        chromo : a chromosome to display.
        domain : domain knowledge instance.
    '''
    def displayGeneration(self, g, domain):
        for chromo in g:
            self.displayChromo(chromo, domain)
        ave = self.calcGenerationScore(g,domain)
        print '(AVERAGE,BEST) : '+str(ave)
        print ''

    def displayChromo(self, chromo, domain):
        s = ''
        for i in range(domain.CHROMO_LEN):
            s = str(chromo>>i&1)+s
        score = domain.fitnessFunction(chromo)
        domain_form = domain.chromoToDomainForm(chromo)
        print 'score = '+str(score)+' , '+s+' <=> '+str(domain_form)
        return score

    '''
    @return
        ave  : average fitness value in the group
        best : best fitness value in the group
    '''
    def calcGenerationScore(self, g, domain):
        ave = 0
        best = 0
        for chromo in g:
            temp = domain.fitnessFunction(chromo)
            ave += temp
            best = max(temp, best)

        ave = 1.0*ave/domain.N
        return ave, best

