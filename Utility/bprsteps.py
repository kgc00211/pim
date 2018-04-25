# coding: utf-8
import argparse as argp
import datetime as dtm
import sys

def bprcsv(ifile, ofile, year):
    """血圧測定記録CSV出力."""
    f = open(ifile, 'r')
    o = open(ofile, 'w')
    o.write("日付,時刻,最高血圧(mmHg),最低血圧(mmHg),脈拍(拍/分),服薬,手帳メモ\n")
    for d in f.readlines():
        ld = d.strip('\n')
        #print(ld)
        if ld == '':
            pass
        elif '日付' in ld:
            break
        else:
            mn = ld[0:2]
            dy = ld[2:4]
            hr = ld[4:6].strip()
            mt = ld[6:8]
            hi = ld[8:12]
            lo = ld[12:15]
            rh = ld[15:18]
            memo = ld[18:]
            #print("/".join([mn,dy,hr,mt,hi,lo,rh,memo]))
            
            month = int(mn) if mn != '  ' else month
            day   = int(dy) if dy != '  ' else day
            if dy.strip() != '':
                if memo == '':
                    use = "飲まなかった"
                elif memo[0:1] in "ab":
                    use = "飲んだ"
                memo = "," + use + "," + memo
            dt = dtm.date(year, month, day)
            hm = hr + ":" + mt if hr.strip() != '' else ' '
            ms = dt.strftime("%Y/%m/%d")+","+hm+","+hi+","+lo+","+rh+memo
            o.write(ms + "\n")
    o.close()
    f.close()
 
 
def WalkSteps(ifile, ofile):
    """歩数記録CSV出力."""
    #
    def GetData(Lbl, txt):
        """日付:2012/10/20
           歩数:9674歩
           カロリー:408kcal
           累積歩数:8959106歩
           いきいき歩数:6074歩
           いきいき累積歩数:117470歩
           脂肪燃焼量:58グラム"""
        d = []
        ss = txt.split("\n")
        tg = Lbl[0]
        for i in range(len(ss)):
            s = ss[i]
            if tg+':' in s:
                ymd  = s.replace(tg+':',"")
                hosu = ss[i+1].replace(Lbl[1]+':','').replace('歩','')
                calo = ss[i+2].strip(Lbl[3]+':').strip('kcal')
                iki  = ss[i+4].replace(Lbl[2]+':','').strip('歩')
                sibo = ss[i+6].strip(Lbl[4]+':').replace('グラム','')
                d.append( [ ymd, hosu, iki, calo, sibo ] )
        return  d

    Lbl=[ '日付','歩数','いきいき歩数','カロリー','脂肪燃焼量']
    fl = open(ifile,"r")
    txt = fl.read()
    fl.close()
    d = GetData(Lbl, txt)
    label = ''.join( "%10s" % s for s in Lbl )
    print("\n"+label)
    print('  --------------------------------------------------------------')
    for t in d:
        txt= ''.join('%12s' % s for s in t)
        print(txt)

    o = open(ofile, 'w')
    tl  = "日付,歩数(歩),しっかり歩数(歩),Ex歩数(歩),歩行距離(km),歩行時間(分),"
    tl += "しっかり歩行時間(分),Ex量(Ex),消費カロリー(kcal),脂肪燃焼量(g)"
    o.write(tl + "\n")
    for t in d:
        txt = ','.join([t[0], t[1], t[2], ",,,,", t[3], t[4]])
        o.write(txt + "\n")
    o.close()


if __name__ == '__main__':

    parser = argp.ArgumentParser()
    parser.add_argument("what", help="血圧: p | 歩数: w | 血圧＋歩数: b")
    parser.add_argument("file", help="ファイル名")
    args = parser.parse_args()
    print(args)

    ifile = args.file
    if args.what in "pbPB":
        ofile = './血圧記録.csv'
        year = 2018
        bprcsv(ifile, ofile, year)
    if args.what in "wbWB":
        ofile = "./歩数記録.csv"
        WalkSteps(ifile, ofile)
    if not args.what in "pwbPWB":
        print("\n意味のない指示です：%s" % args.what)
    pass
