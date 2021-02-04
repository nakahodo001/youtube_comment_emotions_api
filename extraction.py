import re
import csv

def getCSV(filepath):
    with open(filepath) as f:
        reader = csv.reader(f)
        data = [row[1] for row in reader]

    return data[1:]

def data_split(data):
    split_data = []
    for comment in data:
        # "1:12:13 or 12:13" を抽出
        reg = r'(\d+:\d+:\d+|\d+:\d+)'
        times = re.findall(reg, comment)
        if times == []: 
            continue

        # 抽出した時間でコメントを分割
        reg2 = '|'.join(times)
        split_comment = re.split(reg2, comment)

        # なぜか先頭に空文字が入ることがある？？
        # 除去しておく
        split_comment = [data for data in split_comment if data != '']
        split_comment = list(map(lambda x : ''.join(x.split()), split_comment))

        # 数字の後の文字と対応付ける
        index = 0 if comment.find(times[0]) == 0 else 1
        for time in times:
            # 参照先がないとき
            if len(split_comment) <= index :
                break

            if split_comment[index] != '' :
                res = []
                text = split_comment[index]
                res.extend((time, text))
                split_data.append(res)

            index += 1

    return split_data

def store_csv(file_path, data):
    with open(file_path, 'w', newline="", errors="ignore") as f:
        writer = csv.writer(f)
        writer.writerows(data)

filename = '4obg8rf3nnQ'
filepath = './comment/' + filename + '.csv'
out_filepath = './comment/' + filename + '-split.csv'

data = getCSV(filepath)
split_data = data_split(data)
store_csv(out_filepath, split_data)