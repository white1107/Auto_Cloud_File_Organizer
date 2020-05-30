def main():

    import os
    import  re
    import io
    import csv
    import urllib.request
    import subprocess
    from subprocess import PIPE
    from collections import defaultdict

    remote = ''
    folder = ''

    F = os.listdir('./')
    D = defaultdict(str)

    #DICT_MAP.csvがあるか否かで操作を分ける。
    if 'DICT_MAP.csv' not in F:
        list_cloud = subprocess.run(["rclone", "lsf", f""+remote+":"+folder],capture_output=True,text=True,)
        cloud_directories = list_cloud.stdout.split("\n")[0:-1]
        D[folder] = folder+'/'


        #DFSでディレクトリ構造を辞書に登録する。
        def DFS(bef):
            list_cloud = subprocess.run(["rclone", "lsf", f""+remote+":"+D[bef]],capture_output=True,text=True,)
            cloud_directories = list_cloud.stdout.split("\n")[0:-1]
            for i in cloud_directories:
                if '/' in i:
                    i = i[:-1]
                    D[i]=D[bef]+i+'/'
                    print(i)
                    DFS(i)

        #DFSのスタート
        DFS(folder)
        with open('DICT_MAP.csv', 'w') as f:
            for key in D.keys():
                f.write("%s,%s\n"%(key,D[key]))

    #ある場合は前回の履歴から取ってくる。
    else:
        with open('DICT_MAP.csv', newline='') as myFile:
            reader = csv.reader(myFile)
            for row in reader:
                D[row[0]] = row[1]
    list_cloud = subprocess.run(["rclone", "lsf", f""+remote+":"],capture_output=True,text=True,)
    cloud_directories = list_cloud.stdout.split("\n")[0:-1]
    for i in cloud_directories:
        if '.pdf' in i:
            for key in D:
                if key in i:
                    subprocess.run(['rclone','move',remote+':'+i,remote+':'+D[key]])
                    print(i+'　is moved!!')

if __name__ == "__main__":
    main()
    print('FINISHED')



